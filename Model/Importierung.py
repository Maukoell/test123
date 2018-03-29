import csv


def imp(address):
    file = open(address, "r")
    reader = csv.reader(file, delimiter=";")
    return reader


def info(row, prev, wtr):
    if row[0][0] == "#" and prev is not None and firstisdigit(prev):
        wtr.writerow(prev[3] + "." + prev[2] + " " + prev[4] + ":" + prev[5] + ":" + prev[6] + "\n" + row[0] + "\n")

def delfirst(row, wtr):
    if firstisdigit(row):
        wtr.writerow(row[1:])

def main(reader):
    prev = None
    with open("result.csv", "w") as result:
        wtr1 = csv.writer(result)
        with open("info.csv", "w") as info:
            wtr2 = csv.writer(info)
            wtr2.writerow("INFOS")
            for row in reader:
                info(row, prev, wtr2)
                delfirst(row, wtr1)
                findgap(row, prev)
                prev = row

def firstisdigit(row):
    if row[0][1].isdigit() and row[0][2].isdigit() and row[0][0] == " ":
        return True
    return False

def findgap(row, prev):
       if row[6]!=(prev[6]+1):
            print("Lücke von "+ prev[3] + "." + prev[2] + " " + prev[4] + ":" + prev[5] + ":" + prev[6])
       prev = row


if __name__ == '__main__':
    main(imp("F0800305.csv"))