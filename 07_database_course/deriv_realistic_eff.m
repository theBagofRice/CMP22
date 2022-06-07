function  [grad] = deriv_realistic_eff(layers,qbts, noise_strength,seed)
    path(pathdef)
    addpath('./noisy_simulator_4_eff')
    addpath('./code_QAOA_eff')

    global Q
    pl = layers;  % number of QAOA layers
    Q = length(qbts);  % number of qubits
    rng(seed) % Setting a seed
    set_errormodel_realistic(qbts,noise_strength) %create noisy process matrices
    % qbts is a vector of Q (number of qubits) ones and zeros
    % qbts(i) == 1 means that qubit number i is noisy
    % qbts(i) == 0 means that qubit number i is noiseless
    % operations in between noisy and noiseless qubits are noiseless
    % noise_strength is the noise rate divided by the realistic noise rate for   the noisy qubits
    % noise rate of all the noise channels is scaled the same
    % e. g. qbts = [1 1 0 1 0] and noise_strength=0.5 means 5 qubits,
    % qubits nb 1, 2 and 4 noisy, qubits nb 3, 5 noiseless
    %total noise rate = 0.5*(total realistic noise rate)

    param = rand([2*pl 1])*2*pi; %random QAOA angles
    alg = QAOA_QIs1D_PBC_ion(pl); %  paramertrized QAOA circuit (see comments in  QAOA_QIs1D_PBC_ion)
    H= H_QIs();

        grad = cf_deriv_back(alg,param,H); %compute gradient of QAOA Hamiltonian EV w.r.t.  QAOA angles (see  comments in  cf_deriv and fcost_QIs)
	grad = reshape(grad, [length(grad) 1]);
