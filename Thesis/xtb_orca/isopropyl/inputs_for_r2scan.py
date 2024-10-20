# Quick creation of input files for SPE r2scan


import os, re, shutil


# list of folders
folders = []
for dr in os.scandir():
    if dr.is_dir() and 'structure' in dr.name:
        folders.append(dr.name)


os.mkdir('spe_inputs')


pattern_xyz = 'struc_[0-9]+_r2scan_opt\.xyz'

for fol in folders:
    os.mkdir(f'spe_inputs/{fol}')
    file_name = [i for i in os.listdir(f'{fol}/') if re.findall(pattern_xyz, i)][0]
    shutil.copyfile(f'{fol}/{file_name}', f'spe_inputs/{fol}/{file_name}')


