"""
This python script accepts ensemble file after crest crest_ensemble.xyz and creates input files for orca calculation in the same folder
"""


import shutil, os

# Read the original file
with open('crest_ensemble.xyz', 'r') as file:
    lines = file.readlines()

# Calculate the number of lines per chunk. This is number of atoms + 2
lines_per_chunk = int(lines[0]) + 2

# Split the lines into chunks
chunks = [lines[i:i + lines_per_chunk] for i in range(0, len(lines), lines_per_chunk)]

n_procs = 30 # number of nodes
memory = 2048 # memory in MB per one node
charge = 0 # total charge of the molecule
mult = 1 # multiplicity

# Write each chunk into separate files
for i, chunk in enumerate(chunks):
    with open(f'structure_{i + 1}.xyz', 'w') as file:
        file.writelines(chunk)
    file.close()
    header_for_b97 = [f'# b97 optimization of strucutre_{i+1}', '#', '! RIJCOSX B97-D4 def2-SV(P) GCP(DFT/SV(P)) OPT',
                      '%basis', 'auxJK "def2/JK"', 'auxJ "def2/J"', 'auxC "def2-svp/C"', 'end',
                        f'%maxcore {memory}', f'%PAL NPROCS {n_procs} END', '',
                 f'* xyzfile {charge} {mult} structure_{i+1}/structure_{i+1}.xyz', '', '']
    with open(f'struc_{i+1}_b97_opt.inp', 'w') as inp:
        inp.write('\n'.join(header_for_b97))
    inp.close()
    os.mkdir(f'structure_{i + 1}')
    shutil.move(f'structure_{i + 1}.xyz', f'structure_{i + 1}\structure_{i + 1}.xyz')
    shutil.move(f'struc_{i+1}_b97_opt.inp', f'structure_{i + 1}\struc_{i+1}_b97_opt.inp')

print("Splitting completed. Inputs created.")