import csv
import json

def procedure():
    plates = list()
    bingos = list()
    plates_categorys = ["POLLADA", "PARRILLADA", "ROCOTO", "LECHON", "ARROZ", "POLLADA", "PARRILLADA"]
    category = ["O", "P", "R", "L", "A"]
    print("---DATA")
    with open('db/PLATOS.csv', mode='r') as infile:
        reader = csv.reader(infile)
        i = 0
        for row in reader:
            i += 1
            print(row)
            for idx in range(3,10):
                if row[idx] != '':
                    plates.append({"ticketid": category[i] + row[idx], "name": row[0] if row[0] != '' else "N/A", "level": row[1].upper(), "grade": row[2].upper(), "category": plates_categorys[i], "state": "P", "write_udi": "N/A", "write_at": "17/10/2022, 00:00:00"})
            i = 0
    with open('db/BINGOS.csv', mode='r') as infile:
        reader = csv.reader(infile)
        for row in reader:
            for idx in range(3, 10):
                if row[idx] != '':
                    bingos.append({"ticketid": "B" + row[idx], "name": row[0] if row[0] != '' else "N/A", "level": row[1].upper(), "grade": row[2].upper(), "category": "BINGO", "state": "P", "write_udi": "N/A", "write_at": "17/10/2022, 00:00:00"})
    with open('db/platos.json', 'w', encoding='utf-8') as f:
        json.dump(plates, f, ensure_ascii=False, indent=4)
    with open('db/bingos.json', 'w', encoding='utf-8') as f:
        json.dump(bingos, f, ensure_ascii=False, indent=4)
