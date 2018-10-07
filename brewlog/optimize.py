import numpy as np
import pandas as pd

from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import WhiteKernel, RBF

from brewlog import app


# TODO: make this dimension stuff more easily configurable,
# eg to make it possible to switch between brewing methods

# set the initial scale for the different axes
scale_time = 30
scale_ratio = 1
scale_grind = 1
scale_cool = 15

# set the bounds for the fitted scale parameter for each axis
bounds_time = [30, 60]
bounds_ratio = [1, 3]
bounds_grind = [1, 5]
bounds_cool = [5, 60]


def make_gp_model(wide):
    """Instantiate and fit a Gaussian process model."""

    wide = wide.dropna()

    train_Xs = wide[['immersion_time', 'ratio', 'grind', 'water_cooldown']]
    train_ys = wide[['composite_score']]

    kernel = (WhiteKernel(noise_level=10) +
              RBF(length_scale=[scale_time, scale_ratio, scale_grind, scale_cool],
              length_scale_bounds=[bounds_time, bounds_ratio, bounds_grind, bounds_cool]))

    gpr = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=5, normalize_y=True)

    gpr.fit(train_Xs, train_ys)

    app.logger.info('fitted model with: ', gpr.kernel_)
    app.logger.info('log marginal likelihood: ', gpr.log_marginal_likelihood_value_)

    return gpr


def make_prediction_grid():
    """Create a numpy array of points to make predictions for."""

    N_PTS = 50
    N_DIMS = 4

    grid_time = [60, 300]
    grid_ratio = [9, 19]
    grid_grind = [1, 10]
    grid_cool = [0, 90]

    itimes = np.linspace(*grid_time, N_PTS, dtype=np.float16)
    ratios = np.linspace(*grid_ratio, N_PTS, dtype=np.float16)
    grinds = np.linspace(*grid_grind, 10, dtype=np.float16)
    cools = np.linspace(*grid_cool, 10, dtype=np.float16)

    grid = np.meshgrid(itimes, ratios, grinds, cools)

    coords = np.stack(grid, axis=N_DIMS).reshape(-1, N_DIMS)

    return coords


def make_predictions(model, coords):
    """Make predictions for a set of potential brew parameters."""

    y_pred, sigma_pred = model.predict(coords, return_std=True)

    pred = pd.DataFrame({'itime': coords[:, 0],
                         'ratio': coords[:, 1],
                         'grind': coords[:, 2],
                         'cool': coords[:, 3],
                         'score': y_pred.flatten(),
                         'sigma': sigma_pred.flatten()})

    return pred
