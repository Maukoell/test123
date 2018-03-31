#import der csv library
import csv

#globale variablen um die Infozeilen, die fehlerhaften Zeilen und die Luecken zu dokumentieren
info = []
error = []
gap = []

#oeffnen des Files
def imp(address):
    global name
    name = address
    file = open((address+".csv"), "r")
    reader = csv.reader(file, delimiter=";")
    return reader


#ueberpruefung ob die aktuelle Zeile eine Infozeile ist und wenn ja das abspeichern dieser mit vorhergehenden Uhrzeit
def infos(row, prev):
    if row[0][0] == "#" and prev is not None and firstisdigit(prev):
        info.append(prev[3] + "." + prev[2] + " " + prev[4] + ":" + prev[5] + ":" + prev[6] + "\n" + row[0] + "\n")

#schreibt alle Infozeilen, die fehlerhaften Zeilen und die Luecken in ein Info-File
def write():
    with open(str(name)+"_info.csv", "w") as infos:
        wtr = csv.writer(infos)
        wtr.writerow("INFOS")
        for row in info:
            wtr.writerow(row)
        wtr.writerow("==============================================================")
        wtr.writerow("==============================================================")
        wtr.writerow("GAPS")
        for row in gap:
            wtr.writerow(row)
        wtr.writerow("==============================================================")
        wtr.writerow("==============================================================")
        wtr.writerow("ERRORS")
        for row in error:
            wtr.writerow(row)

#entfernen der ersten Zahl und abspeichern der Zeile
def delfirst(row, wtr):
    if firstisdigit(row):
        wtr.writerow(row[1:])

#kompletter Aufruf, um ein file zu bereinigen
def main(reader):
    prev = None
    with open(str(name)+"_result.csv", "w") as result:
        wtr1 = csv.writer(result)
        format=findFormat(reader)
        for row in reader:
            checkFormat(row, prev, format)
            if(row[0][0] != "#" and prev is not None and firstisdigit(prev)):
                findgap(row, prev)
            infos(row, prev)
            delfirst(row, wtr1)
            prev = row
    write()

#ueberprufung ob das erste Element der Zeile eine Zahl ist
def firstisdigit(row):
    if row[0][1].isdigit() and row[0][2].isdigit() and row[0][0] == " ":
        return True
    return False

#ueberprueft ob zwischen der aktuellen und der vorherigen Zeile zu großer zeitlicher unterschied war
def findgap(row, prev):
       if int(row[6]) !=(int(prev[6])+1) and int(prev[6]) != 59:
            gap.append("Lücke von: "+ prev[3] + "." + prev[2] + " " + prev[4] + ":" + prev[5] + ":" + prev[6]+ " bis: "+ row[3] + "." + row[2] + "  " + row[4] + ":" + row[5] + ":" + row[6])
       prev = row

#ueberpruefen ob das format der Zeile mit dem erkannten format uebereinstimmt
def checkFormat(row, prev, format):
        if row[0][0] == "#":
            prev = row
        elif len(row) != format:
            error.append("Format Fehler nach: {}.{}. {}.{}.{}".format(prev[2],prev[3],prev[4],prev[5],prev[6]))
            prev = row
        else:
            prev = row

#erkennen des Formats
def findFormat(reader):
    format = 0
    counter = 0
    rowNumber = 1

    for row, i in zip(reader, range(0, 9)):
        if rowNumber == 1:
            if row[0][0] != "#":
                format = len(row)
            else:
                next(reader)

        if len(row) == format:
            counter += 1
            print("+1")
            rowNumber += 1
            i += 1
        else:
            rowNumber += 1
            i += 1
    if counter > 5:
        print("Format gefunden: {}".format(format))
    else:
        print("Format nicht gefunden")

    return format

def printList(reader):
    for row in reader:
        print(row)
        
if __name__ == '__main__':
    main(imp("F0800305"))
