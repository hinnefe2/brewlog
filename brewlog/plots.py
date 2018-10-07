import urllib
import matplotlib.pyplot as plt
import seaborn as sns

from base64 import b64encode
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


# TODO: make this a decorator
def _convert_fig_to_html(fig):
    """Convert a figure into an <img> tag for HTML using base64 encoding."""

    buff = BytesIO()
    fig.savefig(buff, format='png')
    buff.seek(0)

    data = b64encode(buff.getvalue())

    return 'data:image/png;base64,{}'.format(data.decode('utf-8'))


def plot_time_vs_ratio(wide):
    """Plot a scatterplot of brew time vs ratio."""

    fig, ax = plt.subplots(1, 1)

    sc = ax.scatter(wide.immersion_time.values,
                    wide.ratio.values,
                    c=wide.composite_score.values.flatten())

    fig.colorbar(sc)

    return _convert_fig_to_html(fig)


def plot_predictions(pred, grind_slice=4, cool_slice=30):
    """Plot 2D heatmaps of predicted score and uncertainty."""

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12,5))

    # slice data down to two dimensions for plotting by picking a particular
    # grind size and cooldown time
    pred_slice = pred.loc[(pred.grind == grind_slice) &
                          (pred.cool == cool_slice)]

    # plot 2D heatmaps of predicted score and uncertainty
    sc1 = ax1.tricontourf(pred_slice.itime.values, pred_slice.ratio.values,
                          pred_slice.score.values, 20, cmap='magma')
    sc2 = ax2.tricontourf(pred_slice.itime.values, pred_slice.ratio.values,
                          pred_slice.sigma.values, 20, cmap='gray')

    plt.colorbar(sc1, ax=ax1)
    plt.colorbar(sc2, ax=ax2)

    for ax in (ax1, ax2):
        ax.set_xlabel('steep time (s)')
        ax.set_ylabel('water:coffee ratio')
        # ax.scatter(train_Xs.immersion_time.values,
        #              train_Xs.ratio.values,
        #              c=train_ys.values.flatten(),
        #              cmap='magma',
        #              marker='x')

    ax1.set_title('Predicted taste score');
    ax2.set_title('Prediction uncertainty');

    return _convert_fig_to_html(fig)
