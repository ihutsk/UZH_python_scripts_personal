"""
This file deletes the unnecessary files from orca calculations
"""

import os, shutil, re

def delete_temp(folder):
    files_b97 = os.scandir(f'{folder}/b97_normopt')
    for file in files_b97:
        if file.is_file() and not file.name.endswith(('xyz','out','inp')):
            os.remove(file)
    files_rscan = os.scandir(folder)
    for file in files_rscan:
        if file.is_file() and not file.name.endswith(('xyz','out','inp')):
            os.remove(file)
    print(f'Removed te-mp file in the {folder}\n')


for i in os.scandir():
    if i.is_dir() and 'structure' in i.name:
        delete_temp(i.name)

