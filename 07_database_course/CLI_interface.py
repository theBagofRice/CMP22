import argparse
from matlab_caller import clean_and_dirty_sim

CLI = argparse.ArgumentParser()
CLI.add_argument("-n", dest="name", type=str)
CLI.add_argument("-q", dest="qubits_list", type=int, nargs="*") # * allows for any number of arguments
CLI.add_argument("-l", dest="layers_list", type=int, nargs="*")
CLI.add_argument("-e", dest="err_rate_list", type=float, nargs="*")
CLI.add_argument("-o", dest="order_type_list", type=str, nargs="*", default=["normal"])
CLI.add_argument("-ss", dest="seed_sim_list", type=int, nargs="*", default=[0])
CLI.add_argument("-so", dest="seed_order_list", type=int, nargs="*", default=[0])
CLI.add_argument("-nt", dest="noise_type_list", type=str, nargs="*", default=["depol"])
CLI.add_argument("-se", dest="seed_error_list", type=int, nargs="*", default=[0])
CLI.add_argument("-si", dest="seed_iter_list", type=int, nargs="*", default=[0])
CLI.add_argument("-st", dest="start_step", type=int, default=0)
CLI.add_argument("-fn", dest="friendly_name", type=str)

args = vars(CLI.parse_args())
print(args)
clean_and_dirty_sim(**args)

#Now you can call the simulation by 
# python CLI_interface.py OPTIONS
# eg 
# python CLI_interface.py -n S_3_00e_DepolVar -q 4 -p 0.3 -o 0 -ss 3 -st 0 -si 0 -se 0 -nt Depolarizing -fn CleanDirtyDepolPauli_4Q"