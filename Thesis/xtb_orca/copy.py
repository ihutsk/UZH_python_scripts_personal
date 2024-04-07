import os, shutil
os.mkdir('spe_out')

solvents = ['benzene', 'CH2Cl2', 'water']
for i in os.listdir():
    if 'structure' in i:
        os.mkdir(f'spe_out/{i}')
        for sol in solvents:
            os.mkdir(f'spe_out/{i}/{sol}')
            shutil.copyfile(f'{i}/{sol}/{i}_r2scan_{sol}.inp', f'spe_out/{i}/{sol}/{i}_r2scan_{sol}.inp')
            shutil.copyfile(f'{i}/{sol}/{i}_r2scan_{sol}.out', f'spe_out/{i}/{sol}/{i}_r2scan_{sol}.out')

        