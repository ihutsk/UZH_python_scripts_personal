# Python scripts for ion pair P6

This is the link to the actual ORCA files (input/output). The password is in the thesis.
https://drive.switch.ch/index.php/s/YIuaDQKVLCefTkA

Read the corresponding SI part in the thesis first.
The workflow is don in the following steps:

1. Geometries of cation and anion are submitted to the xTB aISS module.
2. The obtained optimized_structures.xyz file with geometries was then submitted to CREST.
3. The xyz file from the CREST job, `crest_ensemble.xyz`, is then used to create inputs for ORCA. This is done by executing `input_for_orca_from_crest.py` script. Make sure to provide an appropriate number of CPUs (`n_procs` variable) and memory (`memory` variable).
4. When the folders are created, copy them to the cluster and start calculations by executing `opt_hess.py` script in the same folder. Note that `logfile.log` will be created. Make sure to check occasionally this log, as it indicates if some optimization was failed or ended up with imaginary frequencies.
5. 
