# imports
from influxdb import InfluxDBClient

# Verbindung zur Datenbank
client = InfluxDBClient(host='localhost', port=8086)
client.switch_database('messdaten')

lis = []
rs =list(client.query("SELECT * from messwerte").get_points())
for i in rs:
    l=list(i.values())
    lis.append(l[3])
    #for j in range(len(l)):
     #   print(l[j])
    #0 Zeit
    #1 Diag
    #2 Gerätenummer
    #ab 3 Messkanäle
client.close()
for i in range(len(lis)):
    print(lis[i])
