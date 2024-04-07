# Short Readme
You should have two files: `xtb.xyz` with trajectories (if it has a different name - change it below), and
the md input file (in my case it's `md_input.inp`). You need `***.inp` file to read the total time 
and the time dump (not step - these are different times).
In case you want to set it manually, just comment that part and create a numpy array time as following:

`time = np.arrange(dump, total_time+dump, dump)`

where `dump` - is how often the coordinates get dumped to the trajectory file, in fs
`total_time` - is for how long your simulation runs in fs


