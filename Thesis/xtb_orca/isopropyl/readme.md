# Python scripts for ion pair P6

This is the link to the actual ORCA files (input/output). The password is in the thesis.
https://drive.switch.ch/index.php/s/YIuaDQKVLCefTkA

Read the corresponding SI part in the thesis first.
The workflow is done in the following steps:

1. Geometries of cation and anion are submitted to the xTB aISS module.
2. The obtained optimized_structures.xyz file with geometries was then submitted to CREST.
3. The xyz file from the CREST job, `crest_ensemble.xyz`, is then used to create inputs for ORCA. This is done by executing `input_for_orca_from_crest.py` script. Make sure to provide an appropriate number of CPUs (`n_procs` variable) and memory (`memory` variable).
4. When the folders are created, copy them to the cluster and start calculations by executing `opt_hess.py` script in the same folder. Note that `logfile.log` will be created. Make sure to check occasionally this log, as it indicates if some optimization was failed or ended up with imaginary frequencies.
5. When this job is finished, create inputs for SP energies by executing `inputs_for_r2scan.py` script in the same folder. It will create `spe_inputs` folder with inputs. Go there and start the SPE calculations with `r2scan_spe.py`. It will also create log file.
6. Once everything is done, run `copy_spe.py` to copy only the needed files. It will create folder `spe_out`, copy then all folders from the SPE job folder into the main folder to combine them. Clean up the files to remove the temp files by running `delete_temp.py`.
7. Now you should be able to run `Output analysis.ipynb` until the part where file `comparison.xlsx` is created.
8. Execute `orca_output_to_crest.py` to generate an ensemble file for CREST to remove the duplicates. The file is called `ensemble_after_orca_with_duplicates.xyz`.
9. Remove the duplicates with CREST (see `cregen` command in documentation).
10. Rename the ensemble file without duplicates to `crest_ensemble_orca.xyz`, copy to the folder where `Output analysis.ipynb` is and continue.


