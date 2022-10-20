import csv
import json
from models.Ticket import CATEGORIES, LEVELS, GRADES, PRICES


def procedure():
    plates = list()
    bingos = list()
    names = dict()
    max_idx_category = {
        "F": 0,
        "O": "000",
        "P": "000",
        "R": "000",
        "L": "000",
        "A": "000",
        "B": "000",
    }
    categories = ["O", "P", "R", "L", "A", "O", "P"]
    cont = 0
    idx_names = 0
    print("---DATA")
    with open("db/PLATOS.csv", mode="r") as infile:
        reader = csv.reader(infile)
        category_idx = 0
        for i, row in enumerate(reader):
            print(row)
            for idx in range(3, 10):
                if row[idx] != "":
                    cont += 1
                    cat = categories[category_idx]
                    key_level = "10"
                    if names.get(row[0]) is not None:
                        names.update({personid: idx_names +1})
                    else:
                        personid = names[row[0]]
                    for k, v in LEVELS.items():
                        if v == row[1].strip(" "):
                            key_level = k
                    key_grade = "5"
                    for k, v in GRADES.items():
                        if v == row[2].strip(" "):
                            key_grade = k
                    plates.append(
                        {
                            "ticketid": row[idx],
                            "name": row[0] if row[0] != "" else "N/A",
                            "personid": personid,
                            "level": key_level,
                            "grade": key_grade,
                            "category": cat,
                            "state": "P",
                            "write_udi": "N/A",
                            "write_at": "17/10/2022, 00:00:00",
                            "flag": 0,
                            "idx": cont,
                        }
                    )
                    if int(max_idx_category[cat]) < int(row[idx]):
                        max_idx_category[cat] = row[idx]
                category_idx += 1
            category_idx = 0
    with open("db/BINGOS.csv", mode="r") as infile:
        reader = csv.reader(infile)
        cat = "B"
        for i, row in enumerate(reader, start=cont):
            for idx in range(3, 10):
                if row[idx] != "":
                    cont += 1
                    key_level = "10"
                    if names.get(row[0]) is not None:
                        personid = idx_names +1
                    else:
                        personid = names[row[0]]
                    for k, v in LEVELS.items():
                        if v == row[1].strip(" "):
                            key_level = k
                    key_grade = "5"
                    for k, v in GRADES.items():
                        if v == row[2].strip(" "):
                            key_grade = k
                    bingos.append(
                        {
                            "ticketid": row[idx],
                            "name": row[0] if row[0] != "" else "N/A",
                            "personid": personid,
                            "level": key_level,
                            "grade": key_grade,
                            "category": cat,
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
    with open("db/name.json", "w", encoding="utf-8") as f:
        json.dump(names, f, ensure_ascii=False, indent=4)
