# %%
# import matlab.engine
import numpy as np
import pandas as pd
from typing import List
from helper import dummy_matlab
# engine = matlab.engine.start_matlab()

# %%
# Functions for organization


def noise_vector_generator(
    total_qubits: int,
    num_clean_qubits: int,
    order_type: str,
    noise_type: str = "realistic",
    seed: int = 0,
    seed_error: int = 0,
    seed_iter: int = 0,
    err_rate: float = 0.01,
) -> List[List[float]]:
    """function to generate a list of noisy vectors qubits in various interesting
    orders.

    Args:
        total_qubits (int): Total number of qubits in system
        num_clean_qubits (int): Number of clean qubits you want
                                (equal or less than total_qubits)
        order_type (str or list): Distribution of clean qubits:
                        'normal'  ordered ints from 1 to num_clean_qubits,
                        'equal' as equally spaced as possible,
                        'random' random selection.
                        '0' all dirty.
                        A list of lists of ints specifically calculates
                        those orders
                        Anything else returns all clean qubits
        model_type (str): Noise model - choice: 'random', 'x','y','z','depol'.
                        'random' uses a dirichlet distribution.
        seed (int, optional): Seed for RN. Defaults to 0.
        seed_iter (int, optional): Change of seed for noise model. 0 and
                                "random" will have consistent random noise
                                model, otherwise will change for each qubit.

    Returns:
        array[float]: Returns an array of floats representing the noise model.
                    with one row per channel and a column per qubit.
    """
    if num_clean_qubits == 0 or order_type == "0":
        clean_qubits = []
    elif order_type == "normal" or order_type == "Normal":
        clean_qubits = [i + 1 for i in range(num_clean_qubits)]
    elif order_type == "equal":
        clean_qubits = list(
            np.linspace(1, total_qubits, num_clean_qubits, dtype=np.int64).to_list()
        )
    elif order_type == "random":
        np.random.seed(seed)
        clean_qubits = list(
            np.sort(
                np.random.choice(
                    [i + 1 for i in range(total_qubits)],
                    num_clean_qubits,
                    replace=False,
                )
            )
        )
    elif type(order_type) == list:
        clean_qubits = order_type
    else:
        clean_qubits = [i + 1 for i in range(total_qubits)]

    noise_model = np.zeros((total_qubits))
    for i in range(total_qubits):
        j = i + 1
        if j in clean_qubits:  # leave error rate as zero if clean
            pass
        else:
            noise_model[i] = 1
    # clean_qubits = matlab.int64(clean_qubits)

    return noise_model.T, clean_qubits


# %%
def run_parameters(
    seed_order_list: List[int],
    err_rate_list: List[float],
    seed_sim_list: List[int],
    order_type_list: List[str],
    qubits_list: List[int],
    layers_list: List[int],
    noise_type_list: List[str],
    seed_error_list: List[int],
    seed_iter_list: List[int],
) -> List[dict]:
    """Generates a list of dictionaries of all run parameters for the clean
    and dirty qubit simulation.

    Args:
        seed_order_list (List[int]): List of seeds for the order permutation
        err_rate_list (List[float]): List of error rates wanted
        seed_sim_list (List[int]): List of seeds for the simulation
        order_type_list (List[str]): List of orders to analyize.
        qubits_list (List[int]): list of qubit system size you want to run.
        layers_list (List[int]): list of layer depths wanted.

    Returns:
        List[dict]: List of dictionaries containing run parameters.
    """
    run_params = []  # Holding list for run parameters
    for seed_order in seed_order_list:
        for err_rate in err_rate_list:
            for seed_sim in seed_sim_list:
                for order_type in order_type_list:
                    for qubits in qubits_list:
                        for noise_type in noise_type_list:
                            for seed_error in seed_error_list:
                                for seed_iter in seed_iter_list:
                                    if order_type != "0":
                                        clean_qubit_iterator = range(qubits + 1)

                                    else:
                                        clean_qubit_iterator = [0]

                                    for num_clean_qubits in clean_qubit_iterator:
                                        for layers in layers_list:
                                            # this loop generates all combinaitons
                                            # needed for the simulations so that
                                            # one can restart the simulation easily
                                            run_params_single = {
                                                "seed_sim": seed_sim,
                                                "order_type": order_type,
                                                "layers": layers,
                                                "qubits": qubits,
                                                "err_rate": err_rate,
                                                "num_clean_qubits": num_clean_qubits,
                                                "seed_order": seed_order,
                                                "noise_type": noise_type,
                                                "seed_error": seed_error,
                                                "seed_iter": seed_iter,
                                            }
                                            run_params.append(run_params_single)
    return run_params


def clean_and_dirty_sim(
    name: str,
    qubits_list: List[int],
    layers_list: List[int],
    err_rate_list: List[float],
    order_type_list: List[str],
    seed_sim_list: List[int],
    seed_order_list: List[int] = [0],
    noise_type_list: List[str] = ["realistic"],
    seed_error_list: List[int] = [0],
    seed_iter_list: List[int] = [0],
    start_step: int = 0,
    friendly_name: str = "",
) -> pd.DataFrame:
    """Creates a giant loop that calculates the QAOA gradient derivatives at
    all relevant combinations of listed parameters.

    Args:
        name (str): Filename of saved dataframe (can add path as well).
        qubits_list (List[int]): List of number of qubits you want to study.
        layers_list (List[int]): List of number of layers you want to simulate.
        err_rate_list (List[float]): List of error rates you want to calculate.
        order_type_list (List[str]): list of clean qubit ordering types.
        seed_order_list (List[str]): List of seeds for random order.
        noise_type_list (List[str]): List of noise model types (x,y,z,depol,random)
        seed_iter_list (List[int]): Seed iterator for noise type (0 is constant)
        start_step (int): step to start simulation in case of crash/walltime, saved
                        in the resulting dataframe.

    Returns:
        Pandas.DataFrame: Returns an 'organized' dataframe with all
                        caluclated gradients as a file.
    """
    log_file = open(name + "_step-" + str(start_step) + "_log.txt", "w")
    log_file.write("Run parameters:\n")
    log_file.write(str(locals()))

    step_saver = 0
    total_cycles = 0

    run_params = run_parameters(
        seed_order_list,
        err_rate_list,
        seed_sim_list,
        order_type_list,
        qubits_list,
        layers_list,
        noise_type_list,
        seed_error_list,
        seed_iter_list,
    )

    log_file.write(str(run_params) + "\n\n")
    df = pd.DataFrame(
        columns=[
            "layers",
            "qubits",
            "NumCleanQubits",
            "Err",
            "GradNum",
            "Grad",
            "QubitOrder",
            "SimSeed",
            "OrderSeed",
            "RunID",
            "noise_type",
            "seed_error",
            "seed_iter",
            "name",
        ]
    )

    for step, params in enumerate(run_params[start_step:]):

        step = step + start_step
        noise_vector, clean_qubits = noise_vector_generator(
            params["qubits"],
            params["num_clean_qubits"],
            order_type=params["order_type"],
            noise_type=params["noise_type"],
            seed=params["seed_order"],
            seed_error=params["seed_error"],
            seed_iter=params["seed_iter"],
            err_rate=params["err_rate"],
        )
        log_file.write("num_clean_qubits: " + str(params["num_clean_qubits"]) + "\n ")
        log_file.write(
            " noise_vector: "
            + str(noise_vector)
            + "\n clean_qubits: "
            + str(clean_qubits)
            + " \n "
        )
        if params["num_clean_qubits"] != 0:
            clean_qubits_list = [i for i in clean_qubits[0]]
        else:
            clean_qubits_list = []
            clean_qubits = [0]

        run_ID = (
            str(params["qubits"])
            + str(clean_qubits_list)
            + str(params["num_clean_qubits"])
            + str(params["seed_sim"])
            + str(params["seed_order"])
            + str(params["err_rate"])
            + str(params["seed_iter"])
            + str(params["seed_error"])
            + str(params["noise_type"])
        )

        # error_array = matlab.single(list(noise_vector))[0]
        # grad_array = np.array(
        #     engine.deriv_realistic_eff(
        #         params["layers"], error_array, params["err_rate"], params["seed_sim"]
        #     )
        # ).flatten()
        # a = engine.clear_func(1)
        grad_array = dummy_matlab(params["layers"], params["err_rate"], params["seed_sim"])
        
        for num, gradient in enumerate(grad_array):
            temporary_pandas_dict = {
                "layers": params["layers"],
                "qubits": params["qubits"],
                "NumCleanQubits": params["num_clean_qubits"],
                "Err": params["err_rate"],
                "GradNum": num,
                "Grad": gradient,
                "QubitOrder": clean_qubits_list,
                "SimSeed": params["seed_sim"],
                "OrderSeed": params["seed_order"],
                "seed_error": params["seed_error"],
                "seed_iter": params["seed_iter"],
                "noise_type": params["noise_type"],
                "RunID": run_ID,
                "name": friendly_name,
                "step": step,
            }
            log_file.write("row: " + str(temporary_pandas_dict) + "\n")
            df = df.append(temporary_pandas_dict, ignore_index=True)
        df.to_pickle(name + "_step-" + str(start_step) + ".pkl")
    df.to_pickle(name + "_step-" + str(start_step) + ".pkl")
    log_file.close()
# %%