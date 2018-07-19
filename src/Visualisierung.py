import tkinter
from tkinter.filedialog import *
import plotly.offline as py
import plotly.graph_objs as go
from influxdb import InfluxDBClient

def visualisieren():
    # Verbindung zur Datenbank
    client = InfluxDBClient(host='localhost', port=8086)
    client.switch_database('test')
    traceList = []
    dataList = {}
    rs =list(client.query("select mean(*) from test Group by time(1h)").get_points())
    #Wochentage
    #SELECT MEAN(revenue) FROM revenue_count WHERE time > now() - 7d GROUP BY time(1d)
    set = False
    item=0
    for i in rs:
        l = list(i.values())
        if not set:
            for j in range(len(l)):
                dataList[item,j] = l[j]
                #dataList[item] = l[j] #i = zeile, j = kanal
        item = item+1
        #0 Zeit
        #1 Diag
        #2 Gerätenummer
        #ab 3 Messkanäle
    set=True
    client.close()
    print(len(dataList))
    max=0
    x=[]
    y3=[]
    y4=[]
    y5=[]
    y6=[]
    y7=[]
    y8=[]
    for i in range(len(dataList)):
        if (i,0) in dataList.keys():
     #   for i in dataList:
            x.append(dataList[i,0])
            y3.append(dataList[i, 3])
            y4.append(dataList[i, 4])
            y5.append(dataList[i, 5])
            y6.append(dataList[i, 6])
            y7.append(dataList[i, 7])
            y8.append(dataList[i, 8])
        #max=i
    #data.append(go.Scatter(x=dataList[i,0],
    #                        y=dataList[i,3]),
    #                        name=("channel"+str(i)),
    #                        text=dataList[i,i+3],
    #                        yaxis="y"+str(i))

    trace1 = go.Scattergl(
        x=x,
        y=y3,
        name="K1",
        text=y3,

    )
    trace2 = go.Scattergl(
        x=x,
        y=y4,
        name="K2",
        text=y4,

    )
    trace3 = go.Scattergl(
        x=x,
        y=y5,
        name="K3",
        text=y5,

    )
    trace4 = go.Scattergl(
        x=x,
        y=y6,
        name="K4",
        text=y6,

    )
    data = [trace1, trace2, trace3, trace4]

    if chVar1.get() == 1:
        for k in range(len(data)):
            data[k].update(
                {
                    "hoverinfo": "name+x+text",
                    "line": {"width": 0.5},
                    "marker": {"size": 8},
                    "mode": "lines"
                }
            )
    elif chVar2.get() == 1:
        for k in range(len(data)):
            data[k].update(
                {
                    "hoverinfo": "name+x+text",
                    "line": {"width": 0.5},
                    "marker": {"size": 8},
                    "mode": "lines+markers"
                }
            )
    else:
        for k in range(len(data)):
            data[k].update(
                {
                    "hoverinfo": "name+x+text",
                    "line": {"width": 0.5},
                    "marker": {"size": 8},
                    "mode": "markers"
                }
            )

    layout = dict(
        title="Test Plot",
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label="1d",
                         step="day",
                         stepmode="backward"),
                    dict(count=1,
                         label='1m',
                         step='month',
                         stepmode='backward'),
                    dict(count=6,
                         label='6m',
                         step='month',
                         stepmode='backward'),
                    dict(count=1,
                        label='YTD',
                        step='year',
                        stepmode='todate'),
                    dict(count=1,
                        label='1y',
                        step='year',
                        stepmode='backward'),
                    dict(step='all')
                ])
            ),
            rangeslider= dict(
                    range=["2012-10-31 18:36:37.3129", "2016-05-10 05:23:22.6871"]
            ),
            type='date'
        )
    )
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig)


# Hauptframe
mainFrame = tkinter.Tk()
mainFrame.wm_title("Diplomarbeit")

# Größe bestimmen
fr0 = tkinter.Frame(mainFrame)
fr0.pack()

fr2 = tkinter.Frame(fr0)
fr2.pack(expand=1, fill="x")
chVar1 = IntVar()
chBx1 = tkinter.Checkbutton(fr2, text="lines", variable=chVar1)
chBx1.grid(padx=15, row=0, sticky="E")
chVar2 = IntVar()
chBx2 = tkinter.Checkbutton(fr2, text="lines+markers", variable=chVar2)
chBx2.grid(padx=15, row=0, column=1, sticky="W")
chVar3 = IntVar()
chBx3 = tkinter.Checkbutton(fr2, text="markers", variable=chVar3)
chBx3.grid(padx=15, row=0, column=2, sticky="N")

fr3 = tkinter.Frame(fr0)
fr3.pack(expand=1, fill="x")
bt1 = tkinter.Button(fr3, text="Visualisieren", width=15, command=visualisieren)
bt1.pack(padx=20, pady=10)


mainFrame.mainloop()