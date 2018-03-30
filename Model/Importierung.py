import csv

info = []
error = []
gap = []
def imp(address):
    file = open(address, "r")
    reader = csv.reader(file, delimiter=";")
    return reader


def infos(row, prev):
    if row[0][0] == "#" and prev is not None and firstisdigit(prev):
        info.append(prev[3] + "." + prev[2] + " " + prev[4] + ":" + prev[5] + ":" + prev[6] + "\n" + row[0] + "\n")

def write():
    with open("info.csv", "w") as infos:
        wtr = csv.writer(infos)
        wtr.writerow("INFOS")
        for row in info:
            wtr.writerow(row)
        wtr.writerow("==============================================================")
        wtr.writerow("==============================================================")
        wtr.writerow("GAPS")
        for row in gap:
            wtr.writerow(row)

def delfirst(row, wtr):
    if firstisdigit(row):
        wtr.writerow(row[1:])

def main(reader):
    prev = None
    with open("result.csv", "w") as result:
        wtr1 = csv.writer(result)
        for row in reader:
            if(row[0][0] != "#" and prev is not None and firstisdigit(prev)):
                findgap(row, prev)
            infos(row, prev)
            delfirst(row, wtr1)
            prev = row
    write()

def firstisdigit(row):
    if row[0][1].isdigit() and row[0][2].isdigit() and row[0][0] == " ":
        return True
    return False

def findgap(row, prev):
       if int(row[6]) !=(int(prev[6])+1) and int(prev[6]) != 59:
            gap.append("Lücke von: "+ prev[3] + "." + prev[2] + " " + prev[4] + ":" + prev[5] + ":" + prev[6]+ " bis: "+ row[3] + "." + row[2] + "  " + row[4] + ":" + row[5] + ":" + row[6])
       prev = row

if __name__ == '__main__':
    main(imp("F0800305.csv"))