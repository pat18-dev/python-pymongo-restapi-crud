import csv
import json


def procedure():
    plates = list()
    bingos = list()
    max_idx_category = {
        "F": 0,
        "O": "000",
        "P": "000",
        "R": "000",
        "L": "000",
        "A": "000",
        "B": "000",
    }
    plates_categorys = [
        "POLLADA",
        "PARRILLADA",
        "ROCOTO",
        "LECHON",
        "ARROZ",
        "POLLADA",
        "PARRILLADA",
    ]
    price_plates = [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0]
    categories = ["O", "P", "R", "L", "A", "O", "P"]
    cont = 0
    print("---DATA")
    with open("db/PLATOS.csv", mode="r") as infile:
        reader = csv.reader(infile)
        category_idx = 0
        for i, row in enumerate(reader):
            print(row)
            for idx in range(3, 10):
                if row[idx] != "":
                    cont += 1
                    plates.append(
                        {
                            "ticketid": row[idx],
                            "name": row[0] if row[0] != "" else "N/A",
                            "level": row[1].upper() if row[1] != "" else "N/A",
                            "grade": row[2].upper() if row[2] != "" else "N/A",
                            "category": plates_categorys[category_idx],
                            "state": "P",
                            "write_udi": "N/A",
                            "write_at": "17/10/2022, 00:00:00",
                            "price": price_plates[category_idx],
                            "flag": 0,
                            "idx": cont,
                        }
                    )
                    if int(max_idx_category[categories[category_idx]]) < int(row[idx]):
                        max_idx_category[categories[category_idx]] = row[idx]
                category_idx += 1
            category_idx = 0
    with open("db/BINGOS.csv", mode="r") as infile:
        reader = csv.reader(infile)
        for i, row in enumerate(reader, start=cont):
            for idx in range(3, 10):
                if row[idx] != "":
                    cont += 1
                    bingos.append(
                        {
                            "ticketid": row[idx],
                            "name": row[0] if row[0] != "" else "N/A",
                            "level": row[1].upper(),
                            "grade": row[2].upper(),
                            "category": "BINGO",
                            "state": "P",
                            "write_udi": "N/A",
                            "write_at": "17/10/2022, 00:00:00",
                            "flag": 0,
                            "price": 5.0,
                            "idx": cont,
                        }
                    )
                    if int(max_idx_category["B"]) < int(row[idx]):
                        max_idx_category["B"] = row[idx]
    with open("db/data.json", "w", encoding="utf-8") as f:
        json.dump(plates + bingos, f, ensure_ascii=False, indent=4)
    with open("db/serial.json", "w", encoding="utf-8") as f:
        json.dump(max_idx_category, f, ensure_ascii=False, indent=4)
