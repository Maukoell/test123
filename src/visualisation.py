# imports
from influxdb import InfluxDBClient
from datetime import datetime
f = "%Y-%m-%dT%H:%M:%SZ"
# Verbindung zur Datenbank
client = InfluxDBClient(host='localhost', port=8086)
client.switch_database('test')
lis=[]
for weekday in range(0, 6):
    print("Wochentag: ", weekday)
    rs =list(client.query("SELECT mean(*) from test WHERE Wochentag='"+str(weekday)+"'group by Wochentag, time(1h)").get_points())
    for i in range(0, len(rs)-1):
        count = 1
        l1 = list(rs[i].values())
        if(l1[1]==None):
            break
        date1=datetime.strptime(l1[0], f)
        for j in range(i, len(rs)-1):
            l2=list(rs[j].values())
            if (l2[1]== None):
                break
            date2 = datetime.strptime(l2[0], f)
            if l1[1]!=None and l2[1]!=None and date1.second==date2.second and date1.minute==date2.minute and date1.hour==date2.hour and date1 != date2:
                for k in range(1,len(l1)):
                    l1[k]+=l2[k]
                count+=1
        for l in range(1,len(l1)):
            if l1[l]!=None:
                l1[l]=int(l1[l])/count
        if(l1[1]!=None):
            lis.append(l1)
for i in lis:
    print()
    print(i)
    #0 Zeit
    #1 Diag
    #2 Gerätenummer
    #ab 3 Messkanäle
client.close()