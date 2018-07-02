import plotly.offline as py
import plotly.graph_objs as go
from influxdb import InfluxDBClient




# Verbindung zur Datenbank
client = InfluxDBClient(host='localhost', port=8086)
client.switch_database('messdaten')
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

trace1 = go.Scatter(
    x=x,
    y=y3,
    name="K1",
    text=y3,
    yaxis="y"+str(y3),
)
trace2 = go.Scatter(
    x=x,
    y=y4,
    name="K2",
    text=y4,
    yaxis="y"+str(y4),
)
trace3 = go.Scatter(
    x=x,
    y=y5,
    name="K3",
    text=y5,
    yaxis="y"+str(y5),
)
trace4 = go.Scatter(
    x=x,
    y=y6,
    name="K4",
    text=y6,
    yaxis="y"+str(y6),
)
data = go.Data([trace1, trace2, trace3, trace4])

# style all the traces
for k in range(len(data)):
    data[k].update(
        {
            "type": "scatter",
            "hoverinfo": "name+x+text",
            "line": {"width": 0.5},
            "marker": {"size": 8},
            "mode": "lines+markers",
            "showlegend": False
        }
    )

layout = {
  "annotations": [
    {
      "x": "2018-01-01",
      "y": 0,
      "arrowcolor": "rgba(63, 81, 181, 0.2)",
      "arrowsize": 0.3,
      "ax": 0,
      "ay": 30,
      "text": "state1",
      "xref": "x",
      "yanchor": "bottom",
      "yref": "y"
    },
    {
      "x": "2019-01-01",
      "y": 0,
      "arrowcolor": "rgba(76, 175, 80, 0.1)",
      "arrowsize": 0.3,
      "ax": 0,
      "ay": 30,
      "text": "state2",
      "xref": "x",
      "yanchor": "bottom",
      "yref": "y"
    }
  ],
  "dragmode": "zoom",
  "hovermode": "x",
  "legend": {"traceorder": "reversed"},
  "margin": {
    "t": 100,
    "b": 100
  },
  "xaxis": {
    "autorange": True,
    "range": [0, 1500],
    "rangeslider": {
      "autorange": True,
      "range": [0, 1500]
    },
    "type": "date"
  },
  "yaxis": {
    "anchor": "x",
    "autorange": False,
    "domain": [0, 0.2],
    "linecolor": "#673ab7",
    "mirror": True,
    "range": [0, 1500],
    "showline": True,
    "side": "right",
    "tickfont": {"color": "#673ab7"},
    "tickmode": "auto",
    "ticks": "",
    "titlefont": {"color": "#673ab7"},
    "type": "linear",
    "zeroline": False
  },

}
fig = go.Figure(data=data, layout=layout)
py.plot(fig)
