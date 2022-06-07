# %%
header = """#! /bin/bash
#SBATCH --job-name=iClDi_Q{}
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=2-00:00:00
#SBATCH --no-requeue
#SBATCH --output=out
#SBATCH --error=err
#SBATCH --qos=long
# #SBATCH -p shared
#SBATCH --nodelist=cn450
set -x                          # Output commands
set -e                          # Abort o-14n errors
echo "Checking:"
pwd
hostname
date
env | sort < /dev/null > outfiles/ENVIRONMENT
echo "Starting:"
module load matlab
source activate base\n
"""
ending = """
wait
echo "Stopping:"
date
"""


# Set up simulation parameters
seeds = list(range(0, 28))
qubits = [8]
errors = [0, 1 / 8, 2 / 8, 3 / 8, 4 / 8, 5 / 8, 6 / 8, 7 / 8, 1]
errors_name = map("{:0.0e}".format, errors)
errors_name = "_".join(map(str, errors_name))
errors = " ".join(map(str, errors))
step = 0
layers = [1, 2, 3, 4, 5, 6, 8, 10, 15, 20, 40, 70, 100, 200, 300, 400, 500, 600]
order = "0"
order_seed = 0
error_seeds = [0]
seed_iter = 0
error_type = ["variable error"]
friendly_name = "realistic_alter_rate_8Q_"
qubits_str = " ".join(map(str, qubits))
layers_str = " ".join(map(str, layers))
error_type_str = " ".join(map(str, error_type))
error_seed_str = "-".join(map(str, error_seeds))
error_type_name = "-".join(map(str, error_type))
error_seed = " ".join(map(str, error_seeds))
batch_name = (
            f"S_{min(seeds)}-{max(seeds)}_L_{min(layers)}-{max(layers)}_Q_"
            + f"{min(qubits)}-{max(qubits)}_O_{order}{order_seed}"
            + f"_{error_type_name}-{error_seed_str}-{seed_iter}"
            )
filename = f"./batch_scripts/{friendly_name}{batch_name}.sh"

# Write bash script
with open(filename, "w") as f:
    f.write(header.format(f"S_{min(seeds)}-{max(seeds)}"))
    for taskno, simseed in enumerate(seeds):
        name = (
            f"S_{simseed}_L_{min(layers)}-{max(layers)}_Q_{min(qubits)}"
            + f"-{max(qubits)}_O_{order}{order_seed}e_{error_type_name}"
            + f"-{error_seed_str}-{seed_iter}"
        )
        task_line = (
            f"nohup taskset -c {taskno} python LANL_realistic_dirtyclean.py"
            + f" -n {name} -q {qubits_str} -l {layers_str} -e {errors} -o"
            + f" {order} -ss {simseed} -st {step} -si {seed_iter} -se"
            + f' {error_seed} -nt {error_type_str} -fn {friendly_name}"'
            + f" < /dev/null > outfiles/o{taskno}.out0 2> outfiles/o{taskno}.err0&\n"
        )
        f.write(task_line)
    f.write(ending)
# %%
