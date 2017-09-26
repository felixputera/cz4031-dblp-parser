import xml.sax.handler
from dblp_parser.CsvWriter import CsvWriter


class PublicationHandler(xml.sax.handler.ContentHandler):

    def __init__(self, elementname, fieldnames):
        xml.sax.ContentHandler.__init__(self)

        self.pub_csv_writer = CsvWriter(fieldnames=('id', 'key', 'mdate', 'publtype'), fileout='publication.txt')
        self.my_fieldnames = fieldnames
        self.my_elementname = elementname
        self.my_csv_writer = CsvWriter(fieldnames=self.my_fieldnames, fileout='%s.txt' % self.my_elementname)

        self.is_field = {value: False for value in self.my_fieldnames}
        self.is_my_element = False

        self.pub_id = 1
        self.element_count = 1

        self.pub_row = {}
        self.my_row = {}

    def startElement(self, name, attrs):
        if not self.is_my_element:
            if name == self.my_elementname:
                self.is_my_element = True
                if 'key' in attrs.getNames():
                    self.pub_row['key'] = attrs.getValue('key')
                if 'mdate' in attrs.getNames():
                    self.pub_row['mdate'] = attrs.getValue('mdate')
                if 'publtype' in attrs.getNames():
                    self.pub_row['publtype'] = attrs.getValue('publtype')

        else:
            for fieldname in self.my_fieldnames:
                if name == fieldname:
                    self.is_field[fieldname] = True
                    break

    def endElement(self, name):
        if self.is_my_element:
            if name == self.my_elementname:
                # if self.pub_row and self.my_row:
                self.pub_row['id'] = self.pub_id
                self.my_row['p_id'] = self.pub_id
                self.pub_id += 1
                self.pub_csv_writer.add_row(self.pub_row)
                self.my_csv_writer.add_row(self.my_row)
                # print(self.my_row)
                # exit(0)
                print('Added new row to 2 csvs')
                self.my_row = {}
                self.pub_row = {}
                self.is_my_element = False
        print('Processed %d element(s)' % self.element_count)
        self.element_count += 1

    def characters(self, content):
        for fieldname in self.my_fieldnames:
            if self.is_field[fieldname]:
                self.my_row[fieldname] = content
                self.is_field[fieldname] = False

    def endDocument(self):
        self.my_csv_writer.write()
        self.pub_csv_writer.write(append=True)
