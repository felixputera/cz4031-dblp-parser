import csv


class CsvWriter:
    fieldnames = []
    fieldnames_parent = []
    fileout = ''
    fileout_parent =''
    rows = []
    rows_parent = []

    def __init__(self, fieldnames, fieldnames_parent=(), fileout='csv_out.txt', fileout_parent='csv_parent_out.txt'):
        self.fieldnames = fieldnames
        self.fieldnames_parent = fieldnames_parent
        self.fileout = fileout
        self.fileout_parent = fileout_parent

    def add_row(self, row, parent):
        if parent:
            self.rows_parent.append(row)
        else:
            self.rows.append(row)

    def write(self):
        with open(self.fileout, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writeheader()
            for row in self.rows:
                for key, value in row.iteritems():
                    if isinstance(value, list):
                        row[key] = ','.join(value)
                writer.writerow(row)

        if not(fileout_parent == 'csv_parent_out.txt'):
            with open(self.fileout_parent, 'a') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames_parent)
                writer.writeheader()
                for row_parent in self.rows_parent:
                    for key, value in row_parent.iteritems():
                        if isinstance(value, list):
                            row_parent[key] = ','.join(value)
                    writer.writerow(row_parent)
