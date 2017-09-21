import csv


class CsvWriter:
    fieldnames = []
    fileout = ''
    rows = []

    def __init__(self, fieldnames, fileout='csv_out.txt'):
        self.fieldnames = fieldnames
        self.fileout = fileout

    def add_row(self, row):
        self.rows.append(row)

    def write(self):
        with open(self.fileout, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writeheader()
            for row in self.rows:
                writer.writerow(row)


if __name__ == "__main__":
    csv_writer = CsvWriter(fieldnames=['lul', 'eksdee'])
    csv_writer.add_row({'lul': 'lol', 'eksdee': 'xd'})
    csv_writer.write()
