
import os, re
import pandas as pd

df = pd.read_excel('comparison.xlsx')

# list of folders
folders = []
for dr in os.scandir():
    if dr.is_dir() and 'structure' in dr.name and 'imaginary' not in dr.name:
        folders.append(dr.name)


pattern_xyz = 'struc_[0-9]+_r2scan_opt\.xyz'


with open('ensemble_after_orca_with_duplicates.xyz', 'a', encoding='utf-8') as f:
    for folder in folders:
        xyz_name = [file for file in os.listdir(folder) if re.search(pattern=pattern_xyz, string=file)][0]
        with open(f'{folder}/{xyz_name}', 'r', encoding='utf-8') as xyz:
            lines = xyz.readlines()
            num_atoms = lines[0]
            coords = lines[2:]
            energy = str(df[df['name'] == folder].iloc[0,5])
            f.write(f'{num_atoms}\n{energy}\n')
            f.write(''.join(coords))
    



