import xml.sax.handler
from dblp_parser.CsvWriter import CsvWriter


class MastersThesisHandler(xml.sax.handler.ContentHandler):
    is_masters_thesis = False
    new_row = {}
    new_row_parent = {}
    csv_writer = CsvWriter(fieldnames=('id', 'title', 'school', 'year', 'type', 'address', 'month', 'note', 'author'), fieldnames_parent=('id', 'key', 'mdate', 'publtype'), fileout='mastersthesis.txt', fileout_parent='publication.txt')
    is_title = False
    is_school = False
    is_year = False
    is_type = False
    is_address = False
    is_month = False
    is_note = False
    is_author = False
    element_count = 1
    publication_id = 1

    def __init__(self):
        xml.sax.ContentHandler.__init__(self)

    def startElement(self, name, attrs):
        if not self.is_masters_thesis:
            if name == 'mastersthesis':
                self.is_masters_thesis = True
                if 'key' in attrs.getNames():
                    self.new_row_parent['key'] = attrs.getValue('key')
                if 'mdate' in attrs.getNames():
                    self.new_row_parent['mdate'] = attrs.getValue('mdate')
                if 'publtype' in attrs.getNames():
                    self.new_row_parent['publtype'] = attrs.getValue('publtype')
        else:
            if name == 'title':
                self.is_title = True
            elif name == 'school':
                self.is_school = True
            elif name == 'year':
                self.is_year = True
            elif name == 'type':
                self.is_type = True
            elif name == 'address':
                self.is_address = True
            elif name == 'month':
                self.is_month = True
            elif name == 'note':
                self.is_note = True
            elif name == 'author':
                self.is_author = True

    def endElement(self, name):
        if self.is_masters_thesis:
            if name == 'mastersthesis':
                if self.new_row:
                    self.new_row['id'] = self.publication_id
                    self.new_row_parent['id'] = self.publication_id
                    self.publication_id += 1
                    self.csv_writer.add_row(self.new_row,0)
                    self.csv_writer.add_row(self.new_row_parent,1)
                    print('Added new row to be output to csv')
                self.new_row = {}
                self.new_row_parent = {}
                self.is_masters_thesis = False
        print('Processed %d element(s)' % self.element_count)
        self.element_count += 1

    def characters(self, content):
        if self.is_title:
            if 'title' in new_row:
                self.new_row['title'].append(content)
            else:
                self.new_row['title'] = [content]
            self.is_title = False
        elif self.is_school:
            if 'school' in new_row:
                self.new_row['school'].append(content)
            else:
                self.new_row['school'] = [content]
            self.is_school = False
        elif self.is_year:
            if 'year' in new_row:
                self.new_row['year'].append(content)
            else:
                self.new_row['year'] = [content]
            self.is_year = False
        elif self.is_type:
            if 'type' in new_row:
                self.new_row['type'].append(content)
            else:
                self.new_row['type'] = [content]
            self.is_type = False
        elif self.is_address:
            if 'address' in new_row:
                self.new_row['address'].append(content)
            else:
                self.new_row['address'] = [content]
            self.is_address = False
        elif self.is_month:
            if 'month' in new_row:
                self.new_row['month'].append(content)
            else:
                self.new_row['month'] = [content]
            self.is_month = False
        elif self.is_note:
            if 'note' in new_row:
                self.new_row['note'].append(content)
            else:
                self.new_row['note'] = [content]
            self.is_note = False
        elif self.is_author:
            if 'author' in new_row:
                self.new_row['author'].append(content)
            else:
                self.new_row['author'] = [content]
            self.is_author = False


    def endDocument(self):
        self.csv_writer.write()