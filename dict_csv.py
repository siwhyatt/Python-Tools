import csv

def dictToCSV(filename: str, data: list, header: list) -> None:
    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        writer.writerows(data)


def csvToDict(csv_file: str) -> dict:
    result_dict = {}
    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if len(row) == 2 and row[0].isdigit():
                result_dict[row[0]] = row[1]
        return result_dict