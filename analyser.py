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
        base = os.path.splitext(tail)[0]
        return base


def process_csv(path: str) -> MetricData:
    return MetricData(path)


def plot_metrics_multiple(metric_data: list[MetricData], selected_data_y: list[str], selected_data_x: str, colors: list[str], smooth=-1):
    fig, axes = plt.subplots(1)
    all_y = []
    all_x = []
    lines = []
    line_count = 0
    for it, y in enumerate(selected_data_y):
        all_y += [md.data_frame[y] for md in metric_data]
        names = [str(md) + y for md in metric_data]
        all_x += [md.data_frame[selected_data_x] for md in metric_data]

        lines += [(mlines.Line2D([], [], color=colors[line_count + it], label=str(name))) for it, name in enumerate(names)]
        line_count += len(names)

    plot_multiple(all_y,
                  all_x,
                  axes,
                  smooth,
                  colors)

    plt.legend(handles=lines, loc='center left', bbox_to_anchor=(1, 0.5), ncol=1, fancybox=True, shadow=True)
    fig.subplots_adjust(left=0.05, right=0.82, top=0.95, bottom=0.05)


def plot_multiple(y_values: [], x_values: [], axis, smooth: int, colors: list[str]):
    ax_x = axis
    ax_x.get_yaxis().set_visible(False)
    for iteration, y in enumerate(y_values):
        ax = ax_x.twinx()
        minimum = min(x for x in y)
        maximum = max(x for x in y)
        ax.set_ylim([minimum * 0.75, maximum * 1.25])
        x_new = x_values[iteration]
        new_y = y
        if smooth != -1:
            last_timevalue = int(x_values[iteration].iloc[-1])
            amount_of_points = smooth
            x_new = np.linspace(0, last_timevalue, amount_of_points)
            bspline = interpolate.make_interp_spline(x_values[iteration], new_y)
            new_y = bspline(x_new)

        color = "black"
        if len(colors) > iteration:
            color = colors[iteration]
        ax.plot(x_new, new_y, color=color)
        ax.get_yaxis().set_visible(False)


def plot_metrics_single(metric_data: list[MetricData], selected_data_y: list[str], selected_data_x: str, colors: list[str], smooth=-1):
    lines = [(mlines.Line2D([], [], color=colors[iteration], label=str(md))) for iteration, md in enumerate(metric_data)]

    axes_count = len(selected_data_y)
    fig, axes = plt.subplots(axes_count)

    if axes_count > 1:
        for it, s in enumerate(selected_data_y):
            plot_single([md.data_frame[s] for md in metric_data],
                        [md.data_frame[selected_data_x] for md in metric_data],
                        axes[it],
                        s,
                        smooth,
                        colors)
    else:
        plot_single([md.data_frame[selected_data_y[0]] for md in metric_data],
                    [md.data_frame[selected_data_x] for md in metric_data],
                    axes,
                    selected_data_y[0],
                    smooth,
                    colors)

    plt.legend(handles=lines, loc='center left', bbox_to_anchor=(1, 0.5), ncol=1, fancybox=True, shadow=True)
    fig.subplots_adjust(left=0.05, right=0.9, top=0.95, bottom=0.05)


def plot_single(y_values: [], x_values: [], axis, ylabel: str, smooth: int, colors: list[str]):
    ax_x = axis
    minimum = min(min(x) for x in y_values)
    maximum = max(max(x) for x in y_values)
    ax_x.set_ylim([minimum * 0.75, maximum * 1.25])
    ax_x.set_ylabel(ylabel, loc='center')

    for iteration, y in enumerate(y_values):
        ax = ax_x.twinx()
        ax.set_ylim([minimum * 0.75, maximum * 1.25])
        x_new = x_values[iteration]
        new_y = y
        if smooth != -1:
            last_timevalue = int(x_values[iteration].iloc[-1])
            amount_of_points = smooth
            x_new = np.linspace(0, last_timevalue, amount_of_points)
            bspline = interpolate.make_interp_spline(x_values[iteration], new_y)
            new_y = bspline(x_new)

        color = "black"
        if len(colors) > iteration:
            color = colors[iteration]
        ax.plot(x_new, new_y, color=color)
        ax.get_yaxis().set_visible(False)
