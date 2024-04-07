#!/usr/bin/env python
# coding: utf-8

import os, shutil, time, psutil, re
from datetime import datetime


def is_process_running_with_file(process_name, file_path):
    for process in psutil.process_iter(['pid', 'name', 'cmdline']):
        if process.info['name'] == process_name and file_path in process.info['cmdline']:
            return True
    return False



def check(dir_name):
    # check if files are in the dir
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



def xtb_hess_reader(path_to_hess):
    with open(path_to_hess, 'r', encoding='utf-8') as hess:
        lines = hess.readlines()
        for line in lines:
            if 'imaginary frequency' in line:
                return True
        hess.close()
    return False



def opt_error(path_to_out):
    with open(path_to_out, 'r', encoding='utf-8') as out:
        lines = out.readlines()
        for line in lines:
            if 'ORCA finished by error termination' in line:
                return True
    return False



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
    path_to_orca = shutil.which('orca')
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
                     '%basis', 'auxJ "def2-mTZVPP/J"', 'end', '%maxcore 2048', '%PAL NPROCS 30 END', '',
                     f'* xyzfile 0 1 {dir_name}/{dir_name}.xyz', '', '']
    with open(f'{dir_name}/{inp_file[:8]}_r2scan_opt.inp', 'w') as inp:
        inp.write('\n'.join(header_for_r2scan))
     
    # cheking files with function check
    if check(dir_name):
        pass
    else:
        with open('logfile.log', 'a') as log:
            log.write(f'R2SCAN-3c optimization of {dir_name} could not start at {datetime.now().strftime("%a %d %b %Y, %H:%M")}. Check input files. \n')
            log.close()
        return
    
    inp_file = [f for f in os.listdir(dir_name) if f.endswith('.inp')][0] # to make code simpler
    
    # start optimization
    path_to_orca = shutil.which('orca')
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


opt_list = []
for i in os.scandir():
    if i.is_dir() and 'structure' in i.name:
        opt_list.append(i.name)  
for folder in opt_list:
    b97_opt(folder)
    r2scan_opt(folder)
    hessian(folder)

