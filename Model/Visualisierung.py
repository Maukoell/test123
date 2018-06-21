import plotly.offline as py
import plotly.graph_objs as go
from influxdb import InfluxDBClient




# Verbindung zur Datenbank
client = InfluxDBClient(host='localhost', port=8086)
client.switch_database('messdaten')
traceList = []
dataList = []
rs =list(client.query("SELECT * from messwerte").get_points())
set = False
for i in rs:
    l = list(i.values())
    if not set:
        for j in range(len(l) - 3):
            dataList.append([])

    for j in range(len(l)):
        dataList[j][i] = l[j] #i = zeile, j = kanal
    #0 Zeit
    #1 Diag
    #2 Gerätenummer
    #ab 3 Messkanäle
client.close()

#data = go.Data([trace1, trace2, trace3, trace4, trace5])
data = go.Data([])
for i in range(len(dataList-3)):
    data.append(go.Scatter(x=dataList[i][1],
                           y=dataList[i][i+3]),
                            name="channel"+i,
                            text=dataList[i][i+3],
                            yaxis="y+i")

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
      "x": "2013-06-01",
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
      "x": "2014-09-13",
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
  "shapes": [
    {
      "fillcolor": "rgba(63, 81, 181, 0.2)",
      "line": {"width": 0},
      "type": "rect",
      "x0": "2013-01-15",
      "x1": "2013-10-17",
      "xref": "x",
      "y0": 0,
      "y1": 0.95,
      "yref": "paper"
    },
    {
      "fillcolor": "rgba(76, 175, 80, 0.1)",
      "line": {"width": 0},
      "type": "rect",
      "x0": "2013-10-22",
      "x1": "2015-08-05",
      "xref": "x",
      "y0": 0,
      "y1": 0.95,
      "yref": "paper"
    }
  ],
  "xaxis": {
    "autorange": True,
    "range": [dataList[0][0], dataList[0][len(dataList)]],
    "rangeslider": {
      "autorange": True,
      "range": [dataList[0][0], dataList[0][len(dataList)]]
    },
    "type": "date"
  },
  "yaxis": {
    "anchor": "x",
    "autorange": True,
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
