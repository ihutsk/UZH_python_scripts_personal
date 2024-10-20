# Python scripts for ion pair P6

This is the link to the actual ORCA files (input/output). The password is in the thesis.
https://drive.switch.ch/index.php/s/YIuaDQKVLCefTkA

Read the corresponding SI part in the thesis first.
The workflow is don in the following steps:

1. Geometries of cation and anion are submitted to the xTB aISS module.
2. The obtained optimized_structures.xyz file with geometries was then submitted to CREST.
3. The xyz file from the CREST job, `crest_ensemble.xyz`, is then used to create inputs for ORCA. This is done by executing 
