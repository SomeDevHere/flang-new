from subprocess import Popen, PIPE, run
from sys import exit as ex

class Spawn_Manager:
    atExit = {}
    process_chains = []
    verbose = False
    def run_verbose():
        Spawn_Manager.verbose = True
    def create(args):
        if Spawn_Manager.verbose:
            print(args)
        cid = len(Spawn_Manager.process_chains)
        Spawn_Manager.process_chains.append(Spawn(args))
        return cid
    def append(cid, args):
        if Spawn_Manager.verbose:
            print(args)
        Spawn_Manager.process_chains[cid].pipe(args)
    def ondone(cid, call):
        Spawn_Manager.atExit[cid] = call
    def execv(args):
        if Spawn_Manager.verbose:
            print(args)
        ex(run(args).returncode)
    def call(args):
        if Spawn_Manager.verbose:
            print(args)
        res = run(args)
        if res.returncode:
            ex(res.returncode)
    def stdout(args):
        if Spawn_Manager.verbose:
            print(args)
        res = run(args, stdout=PIPE)
        if res.returncode:
            ex(res.returncode)
        return res.stdout.decode("utf-8")
    def onExit(callback):
        Spawn_Manager.atExit[-1] = callback
    def cleanup():
        if -1 in Spawn_Manager.atExit:
            Spawn_Manager.atExit[-1]()
    def exit(code):
        for x in Spawn_Manager.process_chains:
            x.run()
        for i in range(0, len(Spawn_Manager.process_chains)):
            proc = Spawn_Manager.process_chains[i]
            proc.wait()
            if proc.returncode():
                Spawn_Manager.cleanup()
                ex(proc.returncode())
            if i in Spawn_Manager.atExit:
                Spawn_Manager.atExit[i]()
        Spawn_Manager.cleanup()
        ex(code)


class Spawn:
    def __init__(self, args):
        self.prgms = [args]
        self.base = None
    def returncode(self):
        return self.base.returncode
    def pipe(self, args):
        self.prgms.append(args)
    def wait(self):
        if self.base is None:
            return None
        self.base.wait()
        return self.base 
    def poll(self):
        if self.base is None:
            return None
        result = self.base.poll()
        return result 
    def run(self, stdout=False):
        nprgm = len(self.prgms)
        for i in range(0, nprgm):
            pin = None if self.base is None else self.base.stdout
            pout = PIPE if stdout or i != nprgm - 1 else None
            self.base = Popen(self.prgms[i], stdin=pin, stdout=pout)
