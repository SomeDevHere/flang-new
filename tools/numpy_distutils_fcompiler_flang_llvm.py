from numpy.distutils.fcompiler import FCompiler

compilers = ['FlangLLVMCompiler']

class FlangLLVMCompiler(FCompiler):
    compiler_type = 'flang-llvm'
    description = ''
    version_pattern = r'\s*flang-new version (?P<version>[\d.-]+).*'

    possible_executables = ['flang']

    executables = {
        'version_cmd': ["flang", "--version"],
        'compiler_f77': ["flang"],
        'compiler_fix': ["flang"],
        'compiler_f90': ["flang"],
        'linker_so': ["flang"],
        'archiver': ["llvm-ar"],
        'ranlib': ["llvm-ranlib"]
    }
    pic_flags = ['-fpic']

    def get_libraries(self):
        return ['FortranRuntime', 'FortranDecimal', 'pgmath']

    def get_flags(self):
        return []

    def get_flags_free(self):
        return []

    def get_flags_debug(self):
        return ['-g']

    def get_flags_opt(self):
        return ['-O3']

    def get_flags_arch(self):
        return []

    def runtime_library_dir_option(self, dir):
        raise NotImplementedError


if __name__ == '__main__':
    from distutils import log
    log.set_verbosity(2)
    from numpy.distutils import customized_fcompiler
    print(customized_fcompiler(compiler='flang-llvm').get_version())
