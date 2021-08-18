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
        smooth_amount = int(interpolation_amount)
    if len(data) > 0 and len(selected_data_y) > 0 and len(selected_data_x) > 0:
        ana.plot_metrics(data, selected_data_y, selected_data_x[0], colors.COLORS, smooth_amount)
        plt.show(block=False)

def set_preset():
    columns = list(metrics[0].data_frame)
    time_stamp_index = columns.index("Time Stamp")
    amb_index = columns.index("available_memory_MB")
    cpu_index = columns.index("cpu_utilization_percentage")
    gpu_index = columns.index("gpu_utilization_percentage")
    fps_index = columns.index("average_frame_rate")
    window['selected_metrics_x'].update(set_to_index=[time_stamp_index])
    window['selected_metrics_y'].update(set_to_index=[amb_index, cpu_index, gpu_index, fps_index])

layout = [[sg.Input(key='_FILEBROWSE_', enable_events=True, visible=False)],

          [sg.FilesBrowse("Process", target='_FILEBROWSE_'),
           sg.Text("Process OVR Metrics CSVs")],

          [sg.Button('Plot')],

          [sg.Button('Plot Smooth')],

          [sg.Slider(range=(1, 50), default_value=50, orientation="h", key="smooth_slider"),
           sg.Text("Set no. interpolation points")],

          [sg.Text("Imported Metrics:", size=(30, 1)), sg.Text("Select X",size=(30, 1)), sg.Text("Select Y",size=(30, 1))],

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
    elif event == '_FILEBROWSE_':
        import_csvs(values["_FILEBROWSE_"])
        values["_FILEBROWSE_"] = ""
    elif event == 'OVR Preset':
        set_preset()

window.close()
