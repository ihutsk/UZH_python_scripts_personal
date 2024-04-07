#!/usr/bin/env python
# coding: utf-8


import glob, re, argparse
import psi4
import pandas as pd



parser = argparse.ArgumentParser()
parser.add_argument('--ch1', type=int, required=True, help='Charge of the first monomer')
parser.add_argument('--ch2', type=int, required=True, help='Charge of the second monomer')
parser.add_argument('--pos', type=int, required=True, help='Number (label) of the FIRST atom in the second monomer')
parser.add_argument('--mem', type=int, help='memory to allocate, in GB, default 1')
parser.add_argument('--n', type=int, help='Number of threads to use, default 1')

args = parser.parse_args()
memory = 1
cpu = 1
if args.mem:
    memory = args.mem
if args.n:
    cpu = args.n
charge1, charge2, split = args.ch1, args.ch2, args.pos

files = glob.glob('*.gjf')
table = []

for file in files:
    with open(file, 'r') as fl:
        lines = fl.readlines()
        pattern = r'^\W?\d\s\d'
        ln = 0
        start = 0
    
        dimer_list = []
        while ln < len(lines):
            if re.search(pattern, lines[ln]):
                start = ln
                break
            else:
                ln+=1
        for line in lines[start+1:]:
        
            if re.search(r'^\n', line):
                break
            else:
                dimer_list.append(line.strip())
        fl.close()
    coordinates = [f'{charge1} 1']
    for line in dimer_list[:split-1]:
        coordinates.append(line)
    coordinates.append('--')
    coordinates.append(f'{charge2} 1')

    for line in dimer_list[split-1:]:
        coordinates.append(line)
    coordinates.append('units angstrom')
    coord='\n'.join(coordinates)
    psi4.core.set_output_file(f'{file[:-4]}_out.dat', False)
    psi4.set_memory(f'{memory} GB')
    psi4.core.set_num_threads(cpu)

    dimer = psi4.geometry(coord)
    

    psi4.set_options({'basis': 'jun-cc-pvdz'})

    psi4.energy('sapt0', molecule=dimer)
    electr = psi4.variable('SAPT ELST ENERGY')*627.5
    exch = psi4.variable('SAPT EXCH ENERGY')*627.5
    disp = psi4.variable('SAPT DISP ENERGY')*627.5
    ind = psi4.variable('SAPT IND ENERGY')*627.5
    total = psi4.variable('SAPT TOTAL ENERGY')*627.5
    name = file[:-4]
    table.append([name, electr, exch, disp, ind, total])
df = pd.DataFrame(table, columns=['Name', 'Elst', 'Exch', 'Disp', 'Ind', 'Total'])
df.to_csv('result.csv')

    
        
