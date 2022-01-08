def writeEdits(syms, output, us=True):
    def str_sym(sym, underscore):
        if underscore:
        	return sym + " " + sym[3:] + "_"
        else:
                return sym + " " + sym[3:]
    def is_sym(sym):
        if sym.startswith('_QB') or sym.startswith('_QP'):
            return True
        return False
    for x in syms:
        if is_sym(x):
            output.write(str_sym(x, us) + '\n')
    output.close()

def isFortranMain(syms):
    return "_QQmain" in syms
