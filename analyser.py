import os
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np
from scipy import interpolate
import pandas as pd


class MetricData:
    def __init__(self, path: str):
        self.data_frame: pd.DataFrame = pd.read_csv(path)
        self.data_frame = self.data_frame.loc[:, (self.data_frame != 0).any(axis=0)]
        self.name = path

    def __str__(self):
        head, tail = os.path.split(self.name)
        return tail


def process_csv(path: str) -> MetricData:
    return MetricData(path)


def plot(y_values: [], time_stamps: [], axis, ylabel: str, smooth: bool, colors: list[str]):
    ax_x = axis
    minimum = min(min(x) for x in y_values)
    maximum = max(max(x) for x in y_values)
    ax_x.set_ylim([minimum * 0.75, maximum * 1.25])
    ax_x.set_ylabel(ylabel, loc='center')

    for iteration, y in enumerate(y_values):
        ax = ax_x.twinx()
        ax.set_ylim([minimum * 0.75, maximum * 1.25])
        x_new = time_stamps[iteration]
        new_y = y
        if smooth:
            x_new = np.linspace(0, int(time_stamps[iteration][len(time_stamps[iteration]) - 1]), 40)
            bspline = interpolate.make_interp_spline(time_stamps[iteration], new_y)
            new_y = bspline(x_new)

        color = "black"
        if len(colors) > iteration:
            color = colors[iteration]
        ax.plot(x_new, new_y, color=color)
        ax.get_yaxis().set_visible(False)


def plot_metrics(metric_data: list[MetricData], selected_data: list[str], colors: list[str], smooth = False):
    lines = [(mlines.Line2D([], [], color=colors[iteration], label=str(x))) for iteration, x in enumerate(metric_data)]

    axes_count = len(selected_data)
    fig, axes = plt.subplots(axes_count)

    if axes_count > 1:
        for it, s in enumerate(selected_data):
            plot([x.data_frame[s] for x in metric_data], [x.data_frame["Time Stamp"] for x in metric_data], axes[it], s, smooth, colors)
    else:
        plot([x.data_frame[selected_data[0]] for x in metric_data], [x.data_frame["Time Stamp"] for x in metric_data], axes, selected_data[0],
             smooth, colors)

    plt.legend(handles=lines, loc='center left', bbox_to_anchor=(1, 0.5), ncol=1, fancybox=True, shadow=True)
    fig.subplots_adjust(left=0.05, right=0.9, top=0.95, bottom=0.05)
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')
