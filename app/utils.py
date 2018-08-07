from subprocess import call

def boot(interface, mac):
    return call(["wake",interface,mac])
