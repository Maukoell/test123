# imports
import csv
from datetime import datetime
try:
    from influxdb import InfluxDBClient
except ImportError:
    pass
import os
import glob

from tkinter import *
import tkinter
from tkinter.filedialog import *
#import mysql.connector
#from mysql.connector import Error
#import sqlite3
#conn = sqlite3.connect('messdaten.db')
#c = conn.cursor()
# globale variablen um die Infozeilen, die fehlerhaften Zeilen und die Luecken zu dokumentieren
f = "%Y-%m-%d %H:%M:%S"
info = []
error = []
gap = []
#JSON Body für die übertragung in die Datenbank
json = []

#try:
#    con = mysql.connector.connect(host='localhost', database='messdaten', user='root', password='')
#    cursor = con.cursor()
#except Error as e:
#    print(e)

def connectToDatabase():
    global client
    client = InfluxDBClient(host='localhost', port=8086)
    client.switch_database('test')


def imp(address):
    # oeffnen des Files
    global name
    name = address
    file = open(address, "r",newline='')
    reader = csv.reader(file, delimiter=";")
    return reader


# ueberpruefung ob die aktuelle Zeile eine Infozeile ist und wenn ja das abspeichern dieser mit vorhergehenden Uhrzeit
def infos(row, prev):
    if len(row) > 0 and row[0][0] == "#":
        timestamp = ("2018-" + prev[2].replace(" ", "0") + "-" + prev[3].replace(" ", "0") + " " + prev[4].replace(" ","0") + ":" + prev[5].replace(" ", "0") + ":" + prev[6].replace(" ", "0"))
        info.append(timestamp + "\n" + row[0] + "\n")


# schreibt alle Infozeilen, die fehlerhaften Zeilen und die Luecken in ein Info-File
def write():
    with open(str(name) + "_info.csv", "w",newline='') as infos:
        wtr = csv.writer(infos, delimiter=";")
        wtr.writerow(["INFOS"])
        for row in info:
            wtr.writerow([row])
        wtr.writerow(["=============================================================="])
        wtr.writerow(["=============================================================="])
        wtr.writerow(["GAPS"])
        for row in gap:
            wtr.writerow([row])
        wtr.writerow(["=============================================================="])
        wtr.writerow(["=============================================================="])
        wtr.writerow(["ERRORS"])
        for row in error:
            wtr.writerow([row])


# entfernen der ersten Zahl und abspeichern der Zeile
def delfirst(row, wtr, format):
    if firstisdigit(row):
        timestamp = ("2018-" + row[2].replace(" ", "0") + "-" + row[3].replace(" ", "0") + " " + row[4].replace(" ",
                                                                                                           "0") + ":" +
                row[5].replace(" ", "0") + ":" + row[6].replace(" ", "0"))
        wtr.writerow(row[1:])
        #query1= "INSERT IGNORE INTO messgeraet (Geraetenummer, formatierung) VALUES (%s,%s)"
        #args1=(row[1],0)
        #cursor.execute(query1, args1)
        #query2="INSERT IGNORE INTO messwerte (GeraeteNummer, zeit, k1, k2, k3, k4, k5, k6, k7, k8, DIAG ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        #args2=(row[1],zeit,row[7],0,0,0,0,0,0,0,0)
        #cursor.execute(query2, args2)

        #try:
        #    c.execute('INSERT INTO daten VALUES (?,?,?,?,?,?,?,?,?,?,?)',(row[1],zeit,row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15]))
        #except sqlite3.IntegrityError:
        #    print("Error")
            #json.append (
                #{
                 #   "measurement": "test",
                  #  "tags": {
                   #     "GeraeteNummer": row[1],


                    #},
                    #"time": timestamp,
                    #"fields": {
                    #    "k1": int(row[7]),
                    #    "k2": int(row[8]),
                    #    "k3": int(row[9]),
                    #   "k4": int(row[10]),
                    #    "k5": int(row[11]),
                    #    "k6": int(row[12]),
                  #      "k7": int(row[13]),
                 #       "k8": int(row[14]),
                #        "DIAG": int(row[15]),
               #         "Wochentag": (datetime.strptime(timestamp, f).weekday())
              #      }
             #   },
            #)
        if chVar1.get() == 1:
            if format==9:
                json.append({
                           "measurement": "test",
                           "tags": {
                               "GeraeteNummer": row[1],
                               "Wochentag": (datetime.strptime(timestamp, f).weekday()),
                           },
                           "time": timestamp,
                           "fields": {
                               "k1": int(row[7]),
                               "DIAG": int(row[8])
                           }
                       },)
            elif format==10:
                json.append({
                           "measurement": "test",
                           "tags": {
                               "GeraeteNummer": row[1],
                               "Wochentag": (datetime.strptime(timestamp, f).weekday()),
                           },
                           "time": timestamp,
                           "fields": {
                               "k1": int(row[7]),
                               "k2": int(row[8]),
                               "DIAG": int(row[9])
                           }
                       },)
            elif format==11:
                json.append({
                           "measurement": "test",
                           "tags": {
                               "GeraeteNummer": row[1],
                               "Wochentag": (datetime.strptime(timestamp, f).weekday()),
                           },
                           "time": timestamp,
                           "fields": {
                               "k1": int(row[7]),
                               "k2": int(row[8]),
                               "k3": int(row[9]),
                               "DIAG": int(row[10])
                           }
                       },)
            elif format==12:
                json.append({
                           "measurement": "test",
                           "tags": {
                               "GeraeteNummer": row[1],
                               "Wochentag": (datetime.strptime(timestamp, f).weekday()),
                           },
                           "time": timestamp,
                           "fields": {
                               "k1": int(row[7]),
                               "k2": int(row[8]),
                               "k3": int(row[9]),
                               "k4": int(row[10]),
                               "DIAG": int(row[11])
                           }
                       },)

            elif format==13:
                json.append({
                           "measurement": "test",
                           "tags": {
                               "GeraeteNummer": row[1],
                               "Wochentag": (datetime.strptime(timestamp, f).weekday()),
                           },
                           "time": timestamp,
                           "fields": {
                               "k1": int(row[7]),
                               "k2": int(row[8]),
                               "k3": int(row[9]),
                               "k4": int(row[10]),
                               "k5": int(row[11]),
                               "DIAG": int(row[12])
                           }
                       },)
            elif format==14:
                json.append({
                           "measurement": "test",
                           "tags": {
                               "GeraeteNummer": row[1],
                               "Wochentag": (datetime.strptime(timestamp, f).weekday()),
                           },
                           "time": timestamp,
                           "fields": {
                               "k1": int(row[7]),
                               "k2": int(row[8]),
                               "k3": int(row[9]),
                               "k4": int(row[10]),
                               "k5": int(row[11]),
                               "k6": int(row[12]),
                               "DIAG": int(row[13])
                           }
                       },)

            elif format==15:
                json.append({
                           "measurement": "test",
                           "tags": {
                               "GeraeteNummer": row[1],
                               "Wochentag": (datetime.strptime(timestamp, f).weekday()),
                           },
                           "time": timestamp,
                           "fields": {
                               "k1": int(row[7]),
                               "k2": int(row[8]),
                               "k3": int(row[9]),
                               "k4": int(row[10]),
                               "k5": int(row[11]),
                               "k6": int(row[12]),
                               "k7": int(row[13]),
                               "DIAG": int(row[14]),
                           }
                       },)

            elif format==16:
                json.append({
                           "measurement": "test",
                           "tags": {
                               "GeraeteNummer": row[1],
                               "Wochentag": (datetime.strptime(timestamp, f).weekday()),
                           },
                           "time": timestamp,
                           "fields": {
                               "k1": int(row[7]),
                               "k2": int(row[8]),
                               "k3": int(row[9]),
                               "k4": int(row[10]),
                               "k5": int(row[11]),
                               "k6": int(row[12]),
                               "k7": int(row[13]),
                               "k8": int(row[14]),
                               "DIAG": int(row[15]),
                           }
                       },)


#kompletter Aufruf, um ein file zu bereinigen
def main(reader):
    if chVar1.get() == 1:
        connectToDatabase()
    prev = None
    with open(str(name) + "_result.csv", "w",newline='') as result:
        wtr1 = csv.writer(result, delimiter=";")
        formatreader=reader
        timereader=reader
        #format = findFormat(formatreader)
        format=16
        timegap = findTime(timereader)
        print(timegap)
        for row in reader:
            checkFormat(row, prev, format)
            if (firstisdigit(row) and prev is not None):
                findgap(row, prev, timegap, wtr1,  format)
            infos(row, prev)
            delfirst(row, wtr1, format)
            if(firstisdigit(row)):
                prev = row
    #conn.commit()
    #c.close()
    #conn.close()

    if chVar1.get() == 1:
        client.write_points(json)
        json.clear()
        client.close()
    #print(json)
    write()


# erkennung der Zeitabstaende
def findTime(reader):
    time = 0
    counter = 0
    rowNumber = 1
    prev = None
    for row, i in zip(reader, range(0, 9)):
        if prev is not None:
            if rowNumber == 1:
                if row is not None and len(row)>0 and row[0][0] != "#" and len(prev)>0 and prev[0][0] != "#":
                    time = int(row[6]) - int(prev[6])
                else:
                    next(reader)
            if firstisdigit(row) and firstisdigit(prev):
                if int(row[6]) - int(prev[6]) == time or (
                        int(row[6]) < int(prev[6]) and 60 + int(row[6]) - int(prev[6]) == time):
                    counter += 1
                    rowNumber += 1
                    i += 1
                else:
                    rowNumber += 1
                    i += 1
            else:
                rowNumber += 1
                i += 1
                counter += 1
        prev = row
    if counter < 5:
        gap.append("zeitabstand nicht gefunden")
        # Neue GUI geht auf, und der Benutzer wird angehalten den Zeitabstand zwischen zwei Zeilen in Sekunden einzugeben
        time = None
    return time


# ueberprufung ob das erste Element der Zeile eine Zahl ist
def firstisdigit(row):
    if len(row) > 0 and row[0][1] != None and row[0][1].isdigit() and row[0][2] != None and row[0][2].isdigit() and row[0][0] == " ":
        return True
    return False


# ueberprueft ob zwischen der aktuellen und der vorherigen Zeile zu großer zeitlicher unterschied war
def findgap(row, prev, timegap, wtr, format):
    if timegap != None:
        if len(row) > 0 and int(row[6]) != (int(prev[6]) + timegap) and int(prev[6]) != 59:
            von = datetime.strptime(("2018-" + prev[2].replace(" ", "0") + "-" + prev[3].replace(" ", "0") + " " + prev[4].replace(" ",
                                                                                                                   "0") + ":" +
                     prev[5].replace(" ", "0") + ":" + prev[6].replace(" ", "0")),f)
            bis = datetime.strptime(("2018-" + row[2].replace(" ", "0") + "-" + row[3].replace(" ", "0") + " " + row[4].replace(" ",
                                                                                                                "0") + ":" +
                     row[5].replace(" ", "0") + ":" + row[6].replace(" ", "0")),f)
            gap.append(str(von) + " " + str(bis))
            #Ausfälle nur minutenlang, nicht über stunden schlägt fehl nach 59:59
            steps=int((bis-von).total_seconds())
            #steigung
            k=[]
            messk=[]
            for i in range(7, format):
                k.append((int(row[i])-int(prev[i]))/steps)
            for i in range(0, steps):
                seconds=(int(prev[6])+i)%60
                minutes=(int(prev[5])+int((int(prev[6])+i)/60))%60
                hours=int(prev[4])+int(int(prev[5])+int((int(prev[6])+i)/60)/60)
                for j in range(0, len(k)):
                    messk.append(int((k[j] * i) + int(prev[j+7])))
                wtr.writerow(prev[1:4] + [hours] + [minutes] + [seconds]+ messk)
                messk.clear()
                #wtr.writerow(prev[1:4]+[hours]+[minutes]+[seconds]+prev[7:]) vorheriger wert

        prev = row

# ueberpruefen ob das format der Zeile mit dem erkannten format uebereinstimmt
def checkFormat(row, prev, format):
    if (format != None):
        if len(row) > 0 and row[0][0] == "#":
            prev = row
        elif len(row) != format and prev != None and firstisdigit(prev):
            error.append("Format Fehler nach: {}.{}. {}.{}.{}".format(prev[2], prev[3], prev[4], prev[5], prev[6]))
            prev = row
        else:
            prev = row


# erkennen des Formats
def findFormat(reader):
    format = 0
    counter = 0
    rowNumber = 1

    for row, i in zip(reader, range(0, 9)):
        if rowNumber == 1:
            if firstisdigit(row):
                format = len(row)
            else:
                next(reader)

        if len(row) == format:
            counter += 1
            rowNumber += 1
            i += 1
        else:
            rowNumber += 1
            i += 1
    if counter < 5:
        error.append("Format nicht gefunden")
        # Neue GUI geht auf, und der Benutzer wird angehalten das Format einzugeben
        format = None

    return format


# if __name__ == '__main__':
#    main(imp("F0800305"))



# Beenden des main GUI Fensters
def ende():
    mainFrame.destroy()


# Beenden aller GUI Fenster
def endAll():
    popup.destroy()

def openFolder():
    if chVar2.get() == 1:
        os.startfile(directory)
    else:
        os.startfile(filename)

# öffnen des FileChoosers
def openFileChooser():
    if chVar2.get() == 1:
        global directory
        directory = askdirectory()
        tx1.delete(0, len(tx1.get()))
        tx1.insert(0, directory)
    else:
        global filename
        filename = askopenfilename()
        tx1.delete(0, len(tx1.get()))
        tx1.insert(0, filename)


# Vorgang mit Datei durchführen
def startProgramm():
    if chVar2.get() == 1:
        extension = 'csv'
        os.chdir(directory)
        result = [i for i in glob.glob('*.{}'.format(extension))]

        for i in range(len(result)):
            if "info" or "result" not in result[i]:
               main(imp(result[i]))
        finished()
    else:
        if "info" or "result" in tx1.get():
            print("test")
            #errorPopup()
        else:
            main(imp(tx1.get()))
        finished()


def errorPopup():
    global popup1
    popup1 = tkinter.Tk()
    popup1.wm_title("Fehler")
    frame1 = tkinter.Frame(popup1)
    frame1.pack()
    label = tkinter.Label(frame1, text="Die angegebene Datei kann nicht verarbeitet werden")
    label.pack(padx=10, pady=15);
    button1 = tkinter.Button(frame1, text="Ok", command=endAll)
    popup1.mainloop()

# Popup nach Fertigstellung
def finished():
    global popup
    popup = tkinter.Tk()
    popup.wm_title("Vorgang durchgeführt")
    frame1 = tkinter.Frame(popup)
    frame1.pack()
    label = tkinter.Label(frame1, text="Der Vorgang wurde durchgeführt.")
    label.pack(padx=10, pady=15);
    button1 = tkinter.Button(frame1, text="Ok", command=endAll)
    button1.pack(ipadx=50, padx=5, pady=5, side="left")
    if chVar2.get() == 1:
        button2 = tkinter.Button(frame1, text="Ordner öffnen", command=openFolder)
        button2.pack(padx=5, pady=5, side="left")
    else:
        button2 = tkinter.Button(frame1, text="Datei öffnen", command=openFolder)
        button2.pack(padx=5, pady=5, side="left")
    popup.mainloop()


# Hauptframe
mainFrame = tkinter.Tk()
mainFrame.wm_title("Diplomarbeit")

# Größe bestimmen
fr0 = tkinter.Frame(mainFrame)
fr0.pack()

# Pfad Eingabefeld
fr1 = tkinter.Frame(fr0)
fr1.pack(expand=1, fill="x")
lb1 = tkinter.Label(fr1, anchor="n", text="Bitte Dateipfad eingeben oder auswählen:")
lb1.pack(fill="x", expand=1, padx=10, pady=10)
tx1 = tkinter.Entry(fr1, width=30)
tx1.pack(fill="x", expand=1, padx=10, pady=10)

fr2 = tkinter.Frame(fr0)
fr2.pack(expand=1, fill="x")
chVar1 = IntVar()
chBx1 = tkinter.Checkbutton(fr2, text="Datenbankverknüpfung", variable=chVar1)
chBx1.grid(padx=15, row=0, sticky="E")
chVar2 = IntVar()
chBx2 = tkinter.Checkbutton(fr2, text="Ordner?", variable=chVar2)
chBx2.grid(padx=15, row=0, column=1, sticky="W")

# Button Datei auswählen, Bestätigen, Abbrechen
fr3 = tkinter.Frame(fr0)
fr3.pack(expand=1, fill="x")
bt1 = tkinter.Button(fr3, text="Datei auswählen", width=15, command=openFileChooser)
bt1.pack(padx=20, pady=10, side="left")
bt2 = tkinter.Button(fr3, text="Bestätigen", width=15, command=startProgramm)
bt2.pack(padx=20, pady=10, side="left")
bt3 = tkinter.Button(fr3, text="Abbrechen", width=15, command=ende)
bt3.pack(padx=20, pady=10, side="left")


mainFrame.mainloop()
