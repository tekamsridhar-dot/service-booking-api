import csv

def export_csv(filename,headers,rows):

    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)
    return filename