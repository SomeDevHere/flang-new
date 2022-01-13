
C_ENDINGS = ('.c', '.i', )
CXX_ENDINGS = ('.cpp', '.cxx', '.cc', '.c++', '.CPP', '.CXX', '.C', '.CC', '.C++', '.ii', )
OBJC_ENDINGS = ('.m', '.mi', )
OBJCXX_ENDINGS = ('.mm', '.mii', )
FORTRAN_ENDINGS = ('.f', '.for', '.ftn', '.f77', '.f90', '.f95', '.f03', '.f08',
        '.F', '.FOR', '.FTN', '.F77', '.F90', '.F95', '.F03', '.F08', )

SOURCE_ENDINGS = C_ENDINGS + CXX_ENDINGS + OBJC_ENDINGS + OBJCXX_ENDINGS + FORTRAN_ENDINGS

OBJ_ENDINGS = ('.o', )
BITCODE_ENDINGS = ('.bc', )
AR_ENDINGS = ('.a', )
SHARED_ENDINGS = ('.so', )

INPUT_ENDINGS = SOURCE_ENDINGS + OBJ_ENDINGS + BITCODE_ENDINGS + AR_ENDINGS + SHARED_ENDINGS


FORTRAN_COMPILE_FLAGS = ('-fall-intrinsics', '-fallow-argument-mismatch', '-fallow-invalid-boz', 
    '-fbackslash', '-fcray-pointer', '-fd-lines-as-code', '-fd-lines-as-comments',
    '-fdec', '-fdec-char-conversions', '-fdec-structure', '-fdec-intrinsic-ints',
    '-fdec-static', '-fdec-math', '-fdec-include', '-fdec-format-defaults',
    '-fdec-blank-format-item', '-fdefault-double-8', '-fdefault-integer-8', 
    '-fdefault-real-8', '-fdefault-real-10', '-fdefault-real-16', '-fdollar-ok', 
    '-ffixed-line-length-n', '-ffixed-line-length-none', '-fpad-source',
    '-ffree-form', '-ffree-line-length-n', '-ffree-line-length-none',
    '-fimplicit-none', '-finteger-4-integer-8', '-fmax-identifier-length',
    '-fmodule-private', '-ffixed-form', '-fno-range-check', '-fopenacc',
    '-freal-4-real-10', '-freal-4-real-16', '-freal-4-real-8', '-freal-8-real-10',
    '-freal-8-real-16', '-freal-8-real-4', '-std=', '-ftest-forall-temp', '-flarge-sizes',
    '-flogical-abbreviations', '-fxor-operator','-fno-leading-underscore', '-funderscoring',
    '-fno-underscoring', '-fsecond-underscore')

COMPILE_FLAGS = FORTRAN_COMPILE_FLAGS

LINK_FLAGS = ('-static', '-static-flang-libs', '-fno-fortran-main', '-noFlangLibs')

ALIAS = {'-openmp':'-fopenmp', '-static-libgfortran':'-static-flang-libs',
        '-Mbackslash': '-fbackslash', '-Mfixed':'-ffixed-form', 
        '-Mfreeform':'-ffree-form', '-Mrecursive':'-frecursive'}

class ParseArg:
    def __init__(self, args):
        self.args = []
        for x in args[1:]:
            if x in ALIAS:
                self.args.append(ALIAS[x])
            else:
                self.args.append(x)
    def hasFlag(self, flag, remove=False):
        if flag in self.args:
            if remove:
                self.args.remove(flag)
            return True
        return False
    def getOpt(self, flag, remove=False):
        for i in range(0, len(self.args)):
            if self.args[i].startswith(flag):
                value = self.args[i+1]
                if remove:
                    self.args.remove(value)
                    del self.args[i]
                return value
        return None
    def getDef(self, flag, remove=False):
        for i in range(0, len(self.args)):
            if self.args[i].startswith(flag+"="):
                value = self.args[i]
                if remove:
                    self.args.remove(value)
                return value[len(flag)+1:]
        return None
    def getInputFiles(self, endings, remove=False):
        inputFiles = []
        skip = False
        for x in self.args:
            if skip:
                skip = False
                continue
            if not x.startswith('-'):
                if x.endswith(endings):
                    inputFiles.append(x)
            elif '=' in x:
                skip = True
        if remove:
            for x in inputFiles:
                self.args.remove(x)
        return inputFiles
    def get(self):
        return self.args
    def getCompile(self, warn=False):
        argv = []
        for x in self.args:
            if x.startswith('-l') or x.startswith('-fuse-ld='):
                if warn:
                    print(sys.argv[0]+": warning: argument unused during compilation: \""+x+"\"", file=sys.stderr)
            elif x in LINK_FLAGS:
                if warn:
                    print(sys.argv[0]+": warning: argument unused during compilation: \""+x+"\"", file=sys.stderr)
            else:
                argv.append(x)
        return argv
    def getLink(self, warn=False):
        argv = []
        for x in self.args:
            if x in COMPILE_FLAGS:
                if warn:
                    print(sys.argv[0]+": warning: argument unused during linking: \""+x+"\"", file=sys.stderr)
            else:
                argv.append(x)
        return argv
