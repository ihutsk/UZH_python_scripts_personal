#!/usr/bin/env python
# coding: utf-8


import os, shutil, time, psutil, re
from datetime import datetime





def opt_error(path_to_out):
    with open(path_to_out, 'r', encoding='utf-8') as out:
        lines = out.readlines()
        for line in lines:
            if 'ORCA finished by error termination' in line:
                return True
    return False


def is_process_running_with_file(process_name, file_path):
    for process in psutil.process_iter(['pid', 'name', 'cmdline']):
        if process.info['name'] == process_name and file_path in process.info['cmdline']:
            return True
    return False



def progress_bar(count, total, suffix=''):
    
    percent = 100 * count / float(total)
    bar = '*'*int(percent) + '-'*(100-int(percent))
    return f'\r|{bar}| {percent:.2f}%\n'


def r2scan(dir_name):
    
    path_to_orca = shutil.which('orca')
    solvents = ['benzene', 'CH2Cl2', 'water']
    
    #get the name of xyz file for output
    inp_file = [f for f in os.listdir(dir_name) if f.endswith('.xyz')][0]
    
    #create dirs for each solvent
    
    for sol in solvents:
        os.mkdir(f'{dir_name}/{sol}')
        shutil.copyfile(f'{dir_name}/{inp_file}', f'{dir_name}/{sol}/{inp_file}')
        header_for_r2scan = [f'# r2scan energy calculation of {dir_name}', '#', f'! R2SCAN-3c CPCMC({sol})', 
                             '%maxcore 2048', '%PAL NPROCS 30 END', '', 
                             f'* xyzfile 0 1 {dir_name}/{sol}/{inp_file}', '', '']
        with open(f'{dir_name}/{sol}/{dir_name}_r2scan_{sol}.inp', 'w') as inp:
            inp.write('\n'.join(header_for_r2scan))
            inp.close()
        # start r2scan
        
        os.system(f'{path_to_orca} {dir_name}/{sol}/{dir_name}_r2scan_{sol}.inp > {dir_name}/{sol}/{dir_name}_r2scan_{sol}.out &')
        time.sleep(20)
        
        with open('logfile.log', 'a') as log:
            log.write(f'R2SCAN calculation of SPE of {dir_name} in {sol} started at {datetime.now().strftime("%a %d %b %Y, %H:%M")} \n')
            
        # initialize while loop to monitor process
        while is_process_running_with_file('orca', f'{dir_name}/{sol}/{dir_name}_r2scan_{sol}.inp'):
            
            time.sleep(20)
        
        if opt_error(f'{dir_name}/{sol}/{dir_name}_r2scan_{sol}.out'):
            with open('logfile.log', 'a') as log:
                log.write(f'R2SCAN calculation of SPE of {dir_name} in {sol} finished with ERROR at {datetime.now().strftime("%a %d %b %Y, %H:%M")} \n')
        else:    
            with open('logfile.log', 'a') as log:
                log.write(f'R2SCAN calculation of SPE of {dir_name} in {sol} finished at {datetime.now().strftime("%a %d %b %Y, %H:%M")} \n')
            
    
    
        


opt_list = []
for i in os.scandir():
    if i.is_dir() and 'structure' in i.name:
        opt_list.append(i.name) 
for i, folder in enumerate(opt_list):
    r2scan(folder)
    with open('logfile.log', 'a') as log:
        log.write(progress_bar(i, len(opt_list)))

