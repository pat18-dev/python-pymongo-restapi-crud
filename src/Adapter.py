import csv
import json

def procedure():
    plates = list()
    bingos = list()
    plates_categorys = ["POLLADA", "PARRILLADA", "ROCOTO", "LECHON", "ARROZ", "POLLADA", "PARRILLADA"]
    print("---DATA")
    with open('db/PLATOS.csv', mode='r') as infile:
        reader = csv.reader(infile)
        i = 0
        for row in reader:
            i += 1
            print(row)
            for idx in range(3,10):
                if row[idx] != '':
                    plates.append({"ticketid": row[idx], "name": row[0], "level": row[1], "grade": row[2], "category": plates_categorys[i], "state": "P"})
            i = 0
    with open('db/BINGOS.csv', mode='r') as infile:
        reader = csv.reader(infile)
        i = 0
        for row in reader:
            i += 1
            for idx in range(3,10):
                if row[idx] != '':
                    bingos.append({"ticketid": row[idx], "name": row[0], "level": row[1], "grade": row[2], "category": "BINGO", "state": "P"})
            i = 0
    with open('db/platos.json', 'w', encoding='utf-8') as f:
        json.dump(plates, f, ensure_ascii=False, indent=4)
    with open('db/bingos.json', 'w', encoding='utf-8') as f:
        json.dump(bingos, f, ensure_ascii=False, indent=4)
