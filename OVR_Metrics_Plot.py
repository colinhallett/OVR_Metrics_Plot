import PySimpleGUI as sg
import matplotlib.pyplot as plt
import analyser as ana
import colors
from analyser import MetricData

"file browser" \
"processed csvs" \
"selection of csvs" \
"show plot"

metrics: list[MetricData] = []

def import_csvs(csvs: str):
    selections = csvs.split(";")
    for csv in selections:
        if not any(x.name == csv for x in metrics):
            metrics.append(ana.process_csv(csv))
    window['metrics_list'].update(values=metrics)


def draw_plot():
    data = window['metrics_list'].get()
    ana.plot_metrics(data, colors.COLORS)
    plt.show(block=False)


layout = [[sg.Input(key='_FILEBROWSE_', enable_events=True, visible=False)], [sg.FilesBrowse("Process", target='_FILEBROWSE_'), sg.Text("Process OVR Metrics CSVs")],
          [sg.Button('Plot'), sg.Text("Plot selected metrics")],
          [sg.Text("Select metrics:")],
          [sg.Listbox(metrics, key='metrics_list', size=(300,500), select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, highlight_background_color="green")]]

window = sg.Window('OVRMetrics Plot', layout, size=(300,500))
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


































