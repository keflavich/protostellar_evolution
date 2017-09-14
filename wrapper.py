import numpy as np
import os
import shutil

def write_params(mdot=1e-4, timestep=100):

    with open('Driver.F90', 'r') as fh:
        lines = fh.readlines()

    with open('Driver.F90', 'w') as fh:

        for line in lines:
            if line[4:10] == 'mdot =':
                fh.write("    mdot = {0:E} * Msun / secyr\n".format(mdot))
            elif line[4:8] == 'dt =':
                fh.write("    dt = {0:f} * secyr\n".format(timestep))
            else:
                fh.write(line)

def compile_code():
    os.system('make')

def run_code():
    os.system('./protostellar_evolution')


if __name__ == "__main__":

    for mdot in np.logspace(-6, -2, 12):
        os.system('git checkout 8cb810f -- Driver.F90')
        write_params(mdot=mdot)
        compile_code()
        run_code()
        shutil.move("protostellar_evolution.txt",
                    "protostellar_evolution_mdot={0}.txt".format(mdot))
