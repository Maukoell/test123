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

    rs = list(client.query("select mean(*) from test1 Group by time(1h)").get_points())
    # Wochentage
    # SELECT MEAN(revenue) FROM revenue_count WHERE time > now() - 7d GROUP BY time(1d)
    set = False
    item = 0
    print(len(rs[0]))
    matrix = [[0 for i in range(len(rs[0]))] for i in range(len(rs))]
    for i in rs:
        l = list(i.values())
        if not set:
            for j in range(len(l)):
                dataList[item, j] = l[j]
                # dataList[item] = l[j] #i = zeile, j = kanal
        item = item + 1
        # 0 Zeit
        # 1 Diag
        # 2 Gerätenummer
        # ab 3 Messkanäle
    set = True
    client.close()
    print(len(dataList))
    max = 0
    x = []
    y3 = []
    y4 = []
    y5 = []
    y6 = []
    y7 = []
    y8 = []
    yList = []

    for i in range(len(dataList)):
        print(dataList.items())
        if (i, 0) in dataList.keys():
            testList = []
            for t in range(len(dataList[i])):
                testList.append(dataList[i, 0])
                #x.append(dataList[i, 0])
                #y3.append(dataList[i, 3])
                #y4.append(dataList[i, 4])
                #y5.append(dataList[i, 5])
                #y6.append(dataList[i, 6])
                #y7.append(dataList[i, 7])
                #y8.append(dataList[i, 8])
            yList.append(testList)
        # max=i
    # data.append(go.Scatter(x=dataList[i,0],
    #                        y=dataList[i,3]),
    #                        name=("channel"+str(i)),
    #                        text=dataList[i,i+3],
    #                        yaxis="y"+str(i))

    for i in range(len(yList)):
        traceList.append(go.Scattergl(
            x=x,
            y=yList[i],
            name="Kanal" + str(i),
        ))

    data = []
    for i in range(len(traceList)):
        data.append(traceList[i])

    if rbVar.get() == 2:
        for k in range(len(data)):
            data[k].update(
                {
                    "hoverinfo": "name+x+y",
                    "line": {"width": 0.5},
                    "marker": {"size": 8},
                    "mode": "lines+markers"
                }
            )
    elif rbVar.get() == 1:
        for k in range(len(data)):
            data[k].update(
                {
                    "hoverinfo": "name+x+text",
                    "line": {"width": 0.5},
                    "marker": {"size": 8},
                    "mode": "lines"
                }
            )
    elif rbVar.get() == 3:
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
            rangeslider=dict(
                range=["2018-01-01 00:00:00.0000", "2018-12-31 23:23:22.6871"]
            ),
            range=["2018-01-01 00:00:00.0000", "2018-12-31 23:23:22.6871"],
            type='date'
        ),
        yaxis=dict(
            hoverformat='.2f'
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

von = StringVar()
bis = StringVar()
von.set("2018-01-01")
bis.set("2018-12-31")

fr1 = tkinter.Frame(fr0)
fr1.pack()
lb1 = tkinter.Label(fr1, text="Von:", anchor="w", textvariable=von)
lb1.pack(padx=15, pady=5)
ent1 = tkinter.Entry(fr1, width=30)
ent1.pack(fill="x", expand=1, padx=5)
lb2 = tkinter.Label(fr1, text="Bis:", anchor="w")
lb2.pack(padx=15, pady=5)
ent2 = tkinter.Entry(fr1, width=30)
ent2.pack(fill="x", expand=1, padx=5)

fr2 = tkinter.Frame(fr0)
fr2.pack(expand=1, fill="x")
rbVar = IntVar()
rb1 = tkinter.Radiobutton(fr2, text="lines", variable=rbVar, value=1, padx=10)
rb1.grid(padx=15, row=0, column=0, sticky="W")
rb1 = tkinter.Radiobutton(fr2, text="lines+markers", variable=rbVar, value=2, padx=10)
rb1.grid(padx=15, row=0, column=1, sticky="W")
rb1 = tkinter.Radiobutton(fr2, text="markers", variable=rbVar, value=3, padx=10)
rb1.grid(padx=15, row=0, column=2, sticky="W")

fr3 = tkinter.Frame(fr0)
fr3.pack(expand=1, fill="x")
bt1 = tkinter.Button(fr3, text="Visualisieren", width=15, command=visualisieren)
bt1.pack(padx=20, pady=10)



mainFrame.mainloop()
