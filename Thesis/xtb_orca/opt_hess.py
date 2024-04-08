#!/usr/bin/env python
# coding: utf-8

"""
This script executes the workflow of optimization in orca:
1) OPT with B97-D4/def2-SV(P) with GCP. If OPT finished with error - this will be shown in log file
2) OPT with R2SCAN-3c
3) Calculation of hessian in xtb
4) If no imaginary frequencies are found: SP with R2SCAN-3c in C6H6, DCM and water
5) If there are imaginary freqs - report this in the log file and proceed with the next structure
6) delete temp files (gbw etc)
"""

import os, shutil, time, psutil, re
from datetime import datetime

n_procs = 30 # number of nodes
memory = 2048 # memory in MB per one node
charge = 0 # total charge of the molecule
mult = 1 # multiplicity

path_to_orca = shutil.which('orca')
solvents = ['benzene', 'CH2Cl2', 'water']

# function to check if process is running
def is_process_running_with_file(process_name, file_path):
    for process in psutil.process_iter(['pid', 'name', 'cmdline']):
        if process.info['name'] == process_name and file_path in process.info['cmdline']:
            return True
    return False


# check if files are in the dir
def check(dir_name):
    
    files = [f.name for f in os.scandir(dir_name) if f.is_file()]
    pattern_xyz = re.compile(r'.+\.xyz$')
    pattern_inp = re.compile(r'.+\.inp$')
    if len(files) <=1:
        return False
    for file in files:
        if pattern_inp.match(file) or pattern_xyz.match(file):
            return True
        else:
            return False

# check for imaginary frequencies
def xtb_hess_reader(path_to_hess):
    with open(path_to_hess, 'r', encoding='utf-8') as hess:
        lines = hess.readlines()
        for line in lines:
            if 'imaginary frequency' in line:
                return True
        hess.close()
    return False


# check for errors in optimizations
def opt_error(path_to_out):
    with open(path_to_out, 'r', encoding='utf-8') as out:
        lines = out.readlines()
        for line in lines:
            if 'ORCA finished by error termination' in line:
                return True
    return False

# first optimization
def b97_opt(dir_name):
    
    # cheking files with function check
    if check(dir_name):
        pass
    else:
        with open('logfile.log', 'a') as log:
            log.write(f'B97 optimization of {dir_name} could not start at {datetime.now().strftime("%a %d %b %Y, %H:%M")}. Check input files. \n')
            log.close()
        return
    
    # getting input file name
    inp_file = [f for f in os.listdir(dir_name) if f.endswith('.inp')][0]
        
    # start optimization
    
    os.system(f'{path_to_orca} {dir_name}/{inp_file} > {dir_name}/{inp_file[:-4]}.out &')
        
    time.sleep(20)
    
    with open('logfile.log', 'a') as log:
        log.write(f'B97 optimization of {dir_name} started at {datetime.now().strftime("%a %d %b %Y, %H:%M")} \n')
        log.close()
    
    resources = [] 
    
    # initialize while loop to monitor process
    while is_process_running_with_file('orca', f'{dir_name}/{inp_file}'):
        resources.append(datetime.now().strftime('%H:%S')+','
                         +str(psutil.virtual_memory().percent)+','
                         +str(psutil.disk_usage("/mnt")[3])+','
                         +str(psutil.cpu_percent()))
        time.sleep(120)
    # check for errors
    if opt_error(f'{dir_name}/{inp_file[:-4]}.out'):
        with open('logfile.log', 'a') as log:
            log.write(f'B97 optimization of {dir_name} finished with ERROR at {datetime.now().strftime("%a %d %b %Y, %H:%M")} \n')
            log.close()
    else:
    
        with open('logfile.log', 'a') as log:
            log.write(f'B97 optimization of {dir_name} finished at {datetime.now().strftime("%a %d %b %Y, %H:%M")} \n')
            log.close()
    
    with open('resources_monitor.txt', 'a') as res:
        res.write('\n'.join(resources))
        res.close()
                   
# second optimization with R2SCAN

def r2scan_opt(dir_name):
    
    # getting input file for b97
    inp_file = [f for f in os.listdir(dir_name) if f.endswith('.inp')][0]
    
    # copying all files to the b97opt folder
    
    if os.path.exists(f'{dir_name}/b97_normopt'):
        shutil.rmtree(f'{dir_name}/b97_normopt')
    os.mkdir(f'{dir_name}/b97_normopt')
    
    for i in os.scandir(dir_name):
        if i.is_file():
            if i.name != f'{inp_file[:-4]}.xyz':
                shutil.move(f'{dir_name}/{i.name}', f'{dir_name}/b97_normopt/{i.name}')

    # create input file, rename xyz file to avoid confusion
    os.rename(f'{dir_name}/{inp_file[:-4]}.xyz', f'{dir_name}/{dir_name}.xyz')
    
    header_for_r2scan = [f'# r2scan optimization of {dir_name}', '#', '! RIJCOSX R2SCAN-3c OPT',
                     '%basis', 'auxJ "def2-mTZVPP/J"', 'end', f'%maxcore {memory}', f'%PAL NPROCS {n_procs} END', '',
                     f'* xyzfile {charge} {mult} {dir_name}/{dir_name}.xyz', '', '']
    with open(f'{dir_name}/{inp_file[:-12]}_r2scan_opt.inp', 'w') as inp:
        inp.write('\n'.join(header_for_r2scan))
     
    # cheking files with function check
    if check(dir_name):
        pass
    else:
        with open('logfile.log', 'a') as log:
            log.write(f'R2SCAN-3c optimization of {dir_name} could not start at {datetime.now().strftime("%a %d %b %Y, %H:%M")}. Check input files. \n')
            log.close()
        return
    
    inp_file = [f for f in os.listdir(dir_name) if f.endswith('.inp')][0] # rewrite variable to make code simpler
    
    # start optimization
    
    os.system(f'{path_to_orca} {dir_name}/{inp_file} > {dir_name}/{inp_file[:-4]}.out &')
        
    time.sleep(20)
    
    with open('logfile.log', 'a') as log:
        log.write(f'R2SCAN-3c optimization of {dir_name} started at {datetime.now().strftime("%a %d %b %Y, %H:%M")} \n')
        log.close()
    
    resources = [] 
    
    # initialize while loop to monitor process
    while is_process_running_with_file('orca', f'{dir_name}/{inp_file}'):
        resources.append(datetime.now().strftime('%H:%S')+','
                         +str(psutil.virtual_memory().percent)+','
                         +str(psutil.disk_usage("/mnt")[3])+','
                         +str(psutil.cpu_percent()))
        time.sleep(120)
    
    # check for errors
    if opt_error(f'{dir_name}/{inp_file[:-4]}.out'):
        with open('logfile.log', 'a') as log:
            log.write(f'R2SCAN-3c optimization of {dir_name} finished with ERROR at {datetime.now().strftime("%a %d %b %Y, %H:%M")} \n')
            log.close()
    else:
        with open('logfile.log', 'a') as log:
            log.write(f'R2SCAN-3c optimization of {dir_name} finished at {datetime.now().strftime("%a %d %b %Y, %H:%M")} \n')
            log.close()
    
    with open('resources_monitor.txt', 'a') as res:
        res.write('\n'.join(resources))
        res.close()

# calculation of hessian in xtb

def hessian(dir_name):
    
    # check if folder is there
    if os.path.exists(f'{dir_name}/SPH'):
        shutil.rmtree(f'{dir_name}/SPH')
    os.mkdir(f'{dir_name}/SPH')
    
    inp_file = [f for f in os.listdir(dir_name) if f.endswith('.inp')][0] 
    
    shutil.copyfile(f'{dir_name}/{inp_file[:-4]}.xyz', f'{dir_name}/SPH/{inp_file[:-4]}.xyz')
    
    os.system(f'xtb {dir_name}/SPH/{inp_file[:-4]}.xyz --bhess > {dir_name}/SPH/{inp_file[:-4]}_bhess.out &')
    time.sleep(20)
    
    with open('logfile.log', 'a') as log:
        log.write(f'Hessian calculation of {dir_name} started at {datetime.now().strftime("%a %d %b %Y, %H:%M")} \n')
        log.close()
    
    while is_process_running_with_file('xtb', f'{dir_name}/SPH/{inp_file[:-4]}.xyz'):
        
        time.sleep(120)
    
    with open('logfile.log', 'a') as log:
        log.write(f'Hessian calculation of {dir_name} finished at {datetime.now().strftime("%a %d %b %Y, %H:%M")} \n')
        log.close()
    
    # check if there are no imaginary freq
      
    if xtb_hess_reader(f'{dir_name}/SPH/{inp_file[:-4]}_bhess.out'):
                
        with open('logfile.log', 'a') as log:
            log.write(f'Imaginary frequncy in {dir_name} optimization was found as of {datetime.now().strftime("%a %d %b %Y, %H:%M")}. \n')
            log.close()
        return

# SP calculation in different solvents

def r2scan_spe(dir_name):
    
    #get the name of xyz file for output
    inp_file = [f for f in os.listdir(f'{dir_name}/SPH') if f.endswith('.xyz')][0]

    # check that there are no imaginary freqs
    if xtb_hess_reader(f'{dir_name}/SPH/{inp_file[:-4]}_bhess.out'):
        return
        
    #create dirs for each solvent
    
    for sol in solvents:
        os.mkdir(f'{dir_name}/{sol}')
        shutil.copyfile(f'{dir_name}/{inp_file}', f'{dir_name}/{sol}/{inp_file}') # copy xyz file with optimized geometry
        header_for_r2scan = [f'# r2scan energy calculation of {dir_name}', '#', f'! R2SCAN-3c CPCMC({sol})', 
                             f'%maxcore {memory}', f'%PAL NPROCS {n_procs} END', '', 
                             f'* xyzfile {charge} {mult} {dir_name}/{sol}/{inp_file}', '', '']
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
            

# deletes temp files

def delete_temp(folder):
    list_of_folders = [fol.name for fol in os.scandir(folder) if fol.is_dir()]
    for fol in list_of_folders:
        files_to_delete = [file.name for file in os.scandir(f'{folder}/{fol}') if file.is_file() and not file.name.endswith(('xyz','out','inp'))]
        for file in files_to_delete:
            os.remove(f'{folder}/{fol}/{file}')
    for file in os.scandir(folder):
        if file.is_file() and not file.name.endswith(('xyz','out','inp')):
            os.remove(f'{folder}/{file.name}')


# actual executions
opt_list = []
for i in os.scandir():
    if i.is_dir() and 'structure' in i.name:
        opt_list.append(i.name)

opt_list = sorted(opt_list) # sort in order to do optimization one after another

for folder in opt_list:
    b97_opt(folder)
    r2scan_opt(folder)
    hessian(folder)
    r2scan_spe(folder)
    delete_temp(folder)

