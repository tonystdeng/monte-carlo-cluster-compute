from SIRGrid import *


def compute(parameters):
    # all computation done externally
    pendemic = SIRGrid(*parameters)
    history = pendemic.runUntilDie()
    return history
