from IPython.core.magic import magics_class, Magics, cell_magic
from tempfile import NamedTemporaryFile
from importlib import import_module
from subprocess import Popen, PIPE
from os import path
from sys import stdout, stderr
import re


def unload_ipython_extension(ipython):
    # If you want your extension to be unloadable, put that logic here.
    pass


def load_ipython_extension(ipython):
    ipython.register_magics(FutharkMagics)


def run_cmd(*cmd, **kwargs):
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE, **kwargs)
    out, err = proc.communicate("\n")
    return proc.returncode, out, err


def find_executable(name):
    if run_cmd("which", name)[0] != 0 or run_cmd(name, "--version")[0] != 0:
        raise Exception("Cannot find executable {}".format(name))


def extract_text(fut_source, from_line, from_col, to_line, to_col):
    lines = fut_source.split('\n')
    selected = lines[from_line-1:to_line]
    selected[0] = selected[0][from_col-1:]
    if from_line != to_line:
        selected[-1] = selected[-1][:to_col]
    return '\n'.join(selected)


def extract_error(filename, fut_source, err_output):
    location_regexp = r'%s:(\d+):(\d+)-(\d+):(\d+)' % path.basename(filename)
    m = re.search(location_regexp, err_output.decode('utf-8'))
    if m:
        captures = [int(m.group(i)) for i in range(1, 5)]
        stderr.write(
            "\033[1mIn: " +
            extract_text(fut_source, *captures) +
            "\033[0m\n"
        )


def show_output(fut_file, out, err):
    if err:
        extract_error(fut_file, open(fut_file).read(), err)
        stderr.write(err)
    if out:
        stdout.write(out)


futhark_variable = re.compile(r'[\w_]+_\d+')


@magics_class
class FutharkMagics(Magics):
    def __init__(self, *args, **kwargs):
        super(FutharkMagics, self).__init__(*args, **kwargs)
        find_executable("futhark")
        find_executable("futhark-py")
        find_executable("futhark-pyopencl")

    def compile_futhark(self, line, fut_file):
        # Determine file paths and compiler
        gpu = 'gpu' in line
        futhark = 'futhark-pyopencl' if gpu else 'futhark-py'
        dirname = path.dirname(fut_file)
        filename = path.basename(fut_file)
        name = filename.replace('.fut', '')
        lib_path = fut_file.replace('.fut', '.py')

        # Compile to python lib with futhark executable
        r, out, err = run_cmd(futhark, "--library", filename, cwd=dirname)
        show_output(fut_file, out, err)

        if r == 0:
            # Move here (cannot import from arbitrary directory)
            run_cmd("mv", lib_path, "./")

            # Import module, get main class and instantiate one
            mod = import_module(name)
            cls = getattr(mod, name)
            obj = cls()

            # Inject entry points into namespace
            for method in dir(cls):
                if method.startswith('__') or method.startswith('futhark'):
                    continue
                self.shell.user_ns[method] = getattr(obj, method)
            run_cmd("rm", "{}.py".format(name))

    def inspect_futhark(self, line, fut_file):
        dirname = path.dirname(fut_file)
        filename = path.basename(fut_file)
        cmd = [
            'futhark',
            '--gpu' if 'gpu' in line else '--cpu',
            filename
        ]
        r, out, err = run_cmd(*cmd, cwd=dirname)

        # fucolor
        out = out.decode('utf-8')
        all_vars = futhark_variable.findall(out)
        all_vars = sorted(set(all_vars), key=all_vars.index)
        for i, v in enumerate(all_vars):
            color = (7*i) % 256
            colored_v = "\033[1;38;5;{}m{}\033[0m".format(color, v)
            out = out.replace(v, colored_v)
        out = out.encode('utf-8')
        show_output(fut_file, out, err)

    @cell_magic
    def futhark(self, line, cell):
        # Create temp .fut file
        code_file = NamedTemporaryFile(suffix='.fut')
        code_file.write(cell.encode('utf-8'))
        code_file.flush()

        m = self.inspect_futhark if 'inspect' in line else self.compile_futhark
        m(line, code_file.name)
