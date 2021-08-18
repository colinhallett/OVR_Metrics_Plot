import PySimpleGUI as sg
import matplotlib.pyplot as plt
import analyser as ana
import colors
from analyser import MetricData

metrics: list[MetricData] = []
selected_metrics: list[str] = []

def import_csvs(csvs: str):
    selections = csvs.split(";")
    for csv in selections:
        if not any(x.name == csv for x in metrics):
            metrics.append(ana.process_csv(csv))
    window['imported_metrics'].update(values=metrics)
    window['selected_metrics'].update(values=metrics[0].data_frame.head())


def draw_plot():
    data = window['imported_metrics'].get()
    selected_data = window['selected_metrics'].get()
    ana.plot_metrics(data, selected_data, colors.COLORS)
    plt.show(block=False)


layout = [[sg.Input(key='_FILEBROWSE_', enable_events=True, visible=False)], [sg.FilesBrowse("Process", target='_FILEBROWSE_'), sg.Text("Process OVR Metrics CSVs")],
          [sg.Button('Plot'), sg.Text("Plot selected metrics")],
          [sg.Text("Select metrics:")],
          [sg.Listbox(metrics, key='imported_metrics', size=(20, 20), select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE),
           sg.Listbox(selected_metrics, key='selected_metrics', size=(20, 20), select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE)]
          ]

window = sg.Window('OVRMetrics Plot', layout)
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == 'Plot':
        draw_plot()
    elif event == '_FILEBROWSE_':
        import_csvs(values["_FILEBROWSE_"])
        values["_FILEBROWSE_"] = ""
window.close()


































