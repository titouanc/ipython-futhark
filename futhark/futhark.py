from IPython.core.magic import magics_class, Magics, cell_magic
from IPython.display import display_javascript
from tempfile import NamedTemporaryFile
from importlib import import_module
from subprocess import Popen, PIPE
from os import path
from sys import stdout, stderr


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


@magics_class
class FutharkMagics(Magics):
    def __init__(self, *args, **kwargs):
        super(FutharkMagics, self).__init__(*args, **kwargs)
        find_executable("futhark")
        find_executable("futhark-py")
        find_executable("futhark-pyopencl")

    @cell_magic
    def futhark(self, line, cell):
        # Create temp .fut file
        code_file = NamedTemporaryFile(suffix='.fut')
        code_file.write(cell.encode('utf-8'))
        code_file.flush()

        # Determine file paths and compiler
        gpu = 'gpu' in line
        futhark = 'futhark-pyopencl' if gpu else 'futhark-py'
        dirname = path.dirname(code_file.name)
        filename = path.basename(code_file.name)
        name = filename.replace('.fut', '')
        lib_path = code_file.name.replace('.fut', '.py')

        # Compile to python lib with futhark executable
        r, out, err = run_cmd(futhark, "--library", filename, cwd=dirname)
        if err:
            stderr.write(err)
        if out:
            stdout.write(out)
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
