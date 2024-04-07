# How to use automated psi4

We need `.gjf` files from Gaussian scan and this python script.

The use is:
`python auto_psi_from_gauss_v3.py --ch1 charge_of_first_monomer --ch2 charge_of_second_monomer --pos label_of_the_FIRST_atom_in_the_second_monomer --mem memory_in_GB --n number_of_threads &`

The result will be written to the file `result.csv`
