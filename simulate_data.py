from setup_matlab import setup_matlab
import numpy as np

eng = setup_matlab()


def simulate_data(n_trials, n_obs, sfreq, adj_net, p, rho, wvar, rmi, demean,
                  py=False):
    """Generates data from a random VAR model for a given network.

    Args:
        n_trials (int): number of trials or epochs
        n_obs (int): number of observations (sampled time points) per trial
        sfreq (int): sampling frequency (Hz)
        adj_net: adjacency matrix of a network/graph
        p (int): VAR model order (number of time lags)
        rho (float): spectral radius
        wvar (float): VAR coefficients decay weighting factor
        rmi (float): residuals log-generalised correlation (multi-information)
        demean (bool): whether to remove temporal mean and normalise by temporal
            variance.
        py (bool): whether to convert returned matlab array into a numpy
            array for Python. False by default.

    Returns:
        data (array): 3D matrix containing number of network nodes, number of
            observations or samples and number of trials or epochs.
    """

    # generate random VAR coefficients for test network
    AA = eng.var_rand(adj_net, p, rho, wvar)
    n_vars = eng.size(AA, 1)

    # generate random residuals covariance (in fact correlation) matrix
    VV = eng.corr_rand(n_vars, rmi)

    # report information on the generated VAR model
    info = eng.var_info(AA, VV)

    # generate multi-trial VAR time series data with normally distributed residuals
    # for generated VAR coefficients and residuals covariance matrix
    data = eng.varfima_to_tsdata(AA, [], [], VV, n_obs, n_trials)

    if demean:
        data = eng.demean(data, true)

    if py:
        data = np.array(data)

    return data
