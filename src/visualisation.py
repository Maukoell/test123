# imports
from influxdb import InfluxDBClient

# Verbindung zur Datenbank
client = InfluxDBClient(host='localhost', port=8086)
client.switch_database('messdaten')
#Montag
monlis = []
monrs =list(client.query("SELECT mean(*) from messwerte where wochentag='0' and GeraeteNummer='80 'group by time(1m)").get_points())
for i in monrs:
    l=list(i.values())
    monlis.append(l[3])
    #for j in range(len(l)):
     #   print(l[j])
    #0 Zeit
    #1 Diag
    #2 Gerätenummer
    #ab 3 Messkanäle
client.close()