import os
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np
import pandas
from scipy import interpolate
import csv
import pandas as pd

#
# Rows:
# 0 = TimeStamp
# 1 = avaliable_MB
# 10 = cpu_level
# 11 = gpu_level
# 17 = average_frame_rate
# 30 = cpu_utilisation
# 39 = gpu_utilisation
# 41 = app_rss_MB

class MetricData:
    def __init__(self, path: str):
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            current_row = -1
            self.data_frame = pandas.read_csv(path)
            self.name = path
            self.time_stamp: list[float] = []
            self.available_mb = []
            self.cpu_level = []
            self.gpu_level = []
            self.ave_fps = []
            self.cpu_utilisation = []
            self.gpu_utilisation = []
            self.app_rss_mb = []
            print (self.data_frame)
            for row in csv_reader:
                current_row += 1
                if current_row == 0:
                    continue
                self.time_stamp.append(float(row[0]))
                self.available_mb.append(float(row[1]))
                self.cpu_level.append(float(row[10]))
                self.gpu_level.append(float(row[11]))
                self.ave_fps.append(float(row[17]))
                self.cpu_utilisation.append(float(row[30]))
                self.gpu_utilisation.append(float(row[39]))
                self.app_rss_mb.append(float(row[41]))

    def __str__(self):
        head, tail = os.path.split(self.name)
        return tail


def process_csv(path: str) -> MetricData:
    return MetricData(path)


def plot(y_values: [], time_stamps: [], axis, ylabel: str, ylim: [], smooth: bool, colors: list[str]):
    ax_x = axis
    ax_x.set_ylim(ylim)
    ax_x.set_ylabel(ylabel, loc='center')

    for iteration, y in enumerate(y_values):
        ax = ax_x.twinx()
        ax.set_ylim(ylim)
        xnew = time_stamps[iteration]
        new_y = y
        if smooth:
            xnew = np.linspace(0, int(time_stamps[iteration][len(time_stamps[iteration]) - 1]), 40)
            bspline = interpolate.make_interp_spline(time_stamps[iteration], new_y)
            new_y = bspline(xnew)

        color = "black"
        if len(colors) > iteration:
            color = colors[iteration]
        ax.plot(xnew, new_y, color=color)
        ax.get_yaxis().set_visible(False)


def plot_metrics(metric_data: list[MetricData], colors: list[str]):
    lines = [(mlines.Line2D([], [], color=colors[iteration], label=str(x))) for iteration, x in enumerate(metric_data)]

    fig, axes = plt.subplots(4)

    available_mb = [x.available_mb for x in metric_data]
    cpu_uti = [x.cpu_utilisation for x in metric_data]
    gpu_uti = [x.gpu_utilisation for x in metric_data]
    fps = [x.ave_fps for x in metric_data]
    time_stamps = [x.time_stamp for x in metric_data]

    plot(available_mb, time_stamps, axes[0], "AMB", [1000, 4000], False,colors)

    plot(cpu_uti, time_stamps, axes[1], "CPU Utilisation", [0, 110], True,colors)
    plot(fps, time_stamps, axes[2], "FPS", [0, 130], False,colors)
    plot(gpu_uti, time_stamps, axes[3], "GPU Utilisation", [0, 110], False,colors)
    plt.legend(handles=lines, loc='center left', bbox_to_anchor=(1, 0.5), ncol=1, fancybox=True, shadow=True)
    fig.subplots_adjust(left=0.05, right=0.9, top=0.95, bottom=0.05)
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')


def print_averages(results: list[MetricData]):
    mb = 0.
    cpu = 0.
    gpu = 0.
    fps = 0.
    for m in results:
        mb += sum(m.available_mb) / len(m.available_mb)
        cpu += sum(m.cpu_utilisation) / len(m.cpu_utilisation)
        gpu += sum(m.gpu_utilisation) / len(m.gpu_utilisation)
        fps += sum(m.ave_fps) / len(m.ave_fps)

    mb /= len(results)
    cpu /= len(results)
    gpu /= len(results)
    fps /= len(results)
    print(round(mb, 2))
    print(round(cpu, 2))
    print(round(gpu, 2))
    print(round(fps, 2))
#
# vul_multiview_1 = process_csv("OVR_Metrics/autoplay/vulkan_multiview/vmv_1.csv")
# vul_multiview_2 = process_csv("OVR_Metrics/autoplay/vulkan_multiview/vmv_2.csv")
# vul_multiview_3 = process_csv("OVR_Metrics/autoplay/vulkan_multiview/vmv_3.csv")
# vul_multiview_4 = process_csv("OVR_Metrics/autoplay/vulkan_multiview/vmv_4.csv")
# vul_multiview_5 = process_csv("OVR_Metrics/autoplay/vulkan_multiview/vmv_5.csv")
# vul_multiview_6 = process_csv("OVR_Metrics/autoplay/vulkan_multiview/vmv_6.csv")
# vul_multiview_7 = process_csv("OVR_Metrics/autoplay/vulkan_multiview/vmv_7.csv")
# vul_multiview_8 = process_csv("OVR_Metrics/autoplay/vulkan_multiview/vmv_8.csv")
# vul_multiview_9 = process_csv("OVR_Metrics/autoplay/vulkan_multiview/vmv_9.csv")
# vul_multiview = [vul_multiview_1, vul_multiview_2, vul_multiview_3,vul_multiview_4,vul_multiview_5,vul_multiview_6,vul_multiview_7,vul_multiview_8, vul_multiview_9 ]
#
# vul_multipass_1 = process_csv("OVR_Metrics/autoplay/vulkan_multipass/vmp_1.csv")
# vul_multipass_2 = process_csv("OVR_Metrics/autoplay/vulkan_multipass/vmp_2.csv")
# vul_multipass_3 = process_csv("OVR_Metrics/autoplay/vulkan_multipass/vmp_3.csv")
# vul_multipass_4 = process_csv("OVR_Metrics/autoplay/vulkan_multipass/vmp_4.csv")
# vul_multipass_5 = process_csv("OVR_Metrics/autoplay/vulkan_multipass/vmp_5.csv")
# vul_multipass_6 = process_csv("OVR_Metrics/autoplay/vulkan_multipass/vmp_6.csv")
# vul_multipass_7 = process_csv("OVR_Metrics/autoplay/vulkan_multipass/vmp_7.csv")
# vul_multipass_8 = process_csv("OVR_Metrics/autoplay/vulkan_multipass/vmp_8.csv")
# vul_multipass_9 = process_csv("OVR_Metrics/autoplay/vulkan_multipass/vmp_9.csv")
# vul_multipass = [vul_multipass_1, vul_multipass_2, vul_multipass_3,vul_multipass_4,vul_multipass_5,vul_multipass_6,vul_multipass_7,vul_multipass_8, vul_multipass_9 ]
#
# og_multipass_1 = process_csv("OVR_Metrics/autoplay/opengl_multipass/ogmp_1.csv")
# og_multipass_2 = process_csv("OVR_Metrics/autoplay/opengl_multipass/ogmp_2.csv")
# og_multipass_3 = process_csv("OVR_Metrics/autoplay/opengl_multipass/ogmp_3.csv")
# og_multipass_4 = process_csv("OVR_Metrics/autoplay/opengl_multipass/ogmp_4.csv")
# og_multipass_5 = process_csv("OVR_Metrics/autoplay/opengl_multipass/ogmp_5.csv")
# og_multipass_6 = process_csv("OVR_Metrics/autoplay/opengl_multipass/ogmp_6.csv")
# og_multipass_7 = process_csv("OVR_Metrics/autoplay/opengl_multipass/ogmp_7.csv")
# og_multipass_8 = process_csv("OVR_Metrics/autoplay/opengl_multipass/ogmp_8.csv")
# og_multipass_9 = process_csv("OVR_Metrics/autoplay/opengl_multipass/ogmp_9.csv")
# og_multipass = [og_multipass_1, og_multipass_2, og_multipass_3,og_multipass_4,og_multipass_5,og_multipass_6,og_multipass_7,og_multipass_8, og_multipass_9 ]
#
# og_multiview_1 = process_csv("OVR_Metrics/autoplay/opengl_multiview/ogmv_1.csv")
# og_multiview_2 = process_csv("OVR_Metrics/autoplay/opengl_multiview/ogmv_2.csv")
# og_multiview_3 = process_csv("OVR_Metrics/autoplay/opengl_multiview/ogmv_3.csv")
# og_multiview_4 = process_csv("OVR_Metrics/autoplay/opengl_multiview/ogmv_4.csv")
# og_multiview_5 = process_csv("OVR_Metrics/autoplay/opengl_multiview/ogmv_5.csv")
# og_multiview_6 = process_csv("OVR_Metrics/autoplay/opengl_multiview/ogmv_6.csv")
# og_multiview_7 = process_csv("OVR_Metrics/autoplay/opengl_multiview/ogmv_7.csv")
# og_multiview_8 = process_csv("OVR_Metrics/autoplay/opengl_multiview/ogmv_8.csv")
# #og_multiview_9 = process_csv("OVR_Metrics/autoplay/opengl_multiview/ogmv_9.csv")
# og_multiview = [og_multiview_1, og_multiview_2, og_multiview_3,og_multiview_4,og_multiview_5,og_multiview_6,og_multiview_7,og_multiview_8 ]
#
#
#
#
#
# print ("Vul multiview")
# print_averages(vul_multiview)
# print ("Vul multipass")
# print_averages(vul_multipass)
# print ("OG multipass")
# print_averages(og_multipass)
# print ("OG multiview")
# print_averages(og_multiview)
#
# for i in range(8):
#     compare = [og_multiview[i], og_multipass[i], vul_multiview[i], vul_multipass[i]]
#     plot_metrics(compare)
#
# plt.show()
#
