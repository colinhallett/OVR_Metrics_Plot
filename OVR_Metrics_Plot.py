import PySimpleGUI as sg
import matplotlib.pyplot as plt
import analyser as ana
import colors
from analyser import MetricData

metrics: list[MetricData] = []
selected_metrics_y: list[str] = []
selected_metrics_x: list[str] = []
interpolation_amount: int = -1


def import_csvs(csvs: str):
    if csvs is None or len(csvs) == 0:
        return
    selections = csvs.split(";")
    for csv in selections:
        if not any(x.name == csv for x in metrics):
            metrics.append(ana.process_csv(csv))
    window['imported_metrics'].update(values=metrics)
    window['selected_metrics_y'].update(values=metrics[0].data_frame.head())
    window['selected_metrics_x'].update(values=metrics[0].data_frame.head())


def draw_plot(smooth: bool):
    data = window['imported_metrics'].get()
    selected_data_y = window['selected_metrics_y'].get()
    selected_data_x = window['selected_metrics_x'].get()
    smooth_amount = -1
    if smooth:
        smooth_amount = (int)(100 - interpolation_amount)
    if len(data) > 0 and len(selected_data_y) > 0 and len(selected_data_x) > 0:
        ana.plot_metrics_single(data, selected_data_y, selected_data_x[0], colors.COLORS, smooth_amount)
        plt.show(block=False)


def draw_plot_multiple(smooth: bool):
    data = window['imported_metrics'].get()
    selected_data_y = window['selected_metrics_y'].get()
    selected_data_x = window['selected_metrics_x'].get()
    smooth_amount = -1
    if smooth:
        smooth_amount = (int)(100 - interpolation_amount)
    if len(data) > 0 and len(selected_data_y) > 0 and len(selected_data_x) > 0:
        ana.plot_metrics_multiple(data, selected_data_y, selected_data_x[0], colors.COLORS, smooth_amount)
        plt.show(block=False)


def set_preset():
    if len(metrics) == 0: return
    columns = list(metrics[0].data_frame)
    if "Time Stamp" not in columns: return
    time_stamp_index = columns.index("Time Stamp")
    amb_index = columns.index("available_memory_MB")
    cpu_index = columns.index("cpu_utilization_percentage")
    gpu_index = columns.index("gpu_utilization_percentage")
    fps_index = columns.index("average_frame_rate")
    window['selected_metrics_x'].update(set_to_index=[time_stamp_index])
    window['selected_metrics_y'].update(set_to_index=[amb_index, cpu_index, gpu_index, fps_index])


plot_single_layout = [[sg.Button('Plot'), sg.T("Plot one y axis variable per chart")],
                      [sg.Button('Plot Smooth')],
                      [sg.Slider(range=(1, 100), default_value=25, orientation="h", key="smooth_slider", disable_number_display=True), sg.Text("Set smoothness")]]


plot_multi_layout = [[sg.Button('Plot Multiple'), sg.T("Plot multiple y axes variable on single chart")],
                      [sg.Button('Plot Multiple Smooth')],
                      [sg.Slider(range=(1, 100), default_value=25, orientation="h", key="smooth_slider_multiple", disable_number_display=True), sg.Text("Set smoothness")]]

layout = [[sg.Input(key='_FILEBROWSE_', enable_events=True, visible=False)],

          [sg.FilesBrowse("Import", target='_FILEBROWSE_'),
           sg.Text("Process OVR Metrics CSVs")],

          [sg.TabGroup([[sg.Tab("Single Variable", plot_single_layout), sg.Tab("Multi Variable", plot_multi_layout)]], tab_background_color="grey")],

          [sg.Text("Select Metrics (multiple)", size=(30, 1)), sg.Text("Select X Axis (single)",size=(30, 1)), sg.Text("Select Y Axis (multiple)",size=(30, 1))],

          [sg.Listbox(metrics, key='imported_metrics', size=(30, 20), select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE),
           sg.Listbox(selected_metrics_y, key='selected_metrics_x', size=(30, 20), select_mode=sg.SELECT_MODE_SINGLE),
           sg.Listbox(selected_metrics_y, key='selected_metrics_y', size=(30, 20), select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE)],

          [sg.Button('OVR Preset')]
          ]

window = sg.Window('OVRMetrics Plot', layout)
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == 'Plot':
        draw_plot(False)
    elif event == 'Plot Smooth':
        interpolation_amount = values['smooth_slider']
        draw_plot(True)
    elif event == 'Plot Multiple':
        draw_plot_multiple(False)
    elif event == 'Plot Multiple Smooth':
        interpolation_amount = values['smooth_slider_multiple']
        draw_plot_multiple(True)
    elif event == '_FILEBROWSE_':
        import_csvs(values["_FILEBROWSE_"])
        values["_FILEBROWSE_"] = ""
    elif event == 'OVR Preset':
        set_preset()

window.close()
