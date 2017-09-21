import xml.sax.handler
from dblp_parser.CsvWriter import CsvWriter


class AuthorHandler(xml.sax.handler.ContentHandler):
    is_www = False
    new_row = {}
    csv_writer = CsvWriter(fieldnames=('id', 'name', 'affiliation'), fileout='author.txt')
    is_title = False
    is_affiliation = False
    is_author = False
    element_count = 1
    author_id = 1

    def __init__(self):
        xml.sax.ContentHandler.__init__(self)

    def startElement(self, name, attrs):
        if not self.is_www:
            if name == 'www':
                self.is_www = True
        else:
            if name == 'note':
                if 'type' in attrs.getNames():
                    if attrs.getValue('type') == 'affiliation':
                        self.is_affiliation = True
            elif name == 'title':
                self.is_title = True
            elif name == 'author':
                self.is_author = True

    def endElement(self, name):
        if self.is_www:
            if name == 'www':
                if self.new_row:
                    self.new_row['id'] = self.author_id
                    self.author_id += 1
                    self.csv_writer.add_row(self.new_row)
                    print('Added new row to be output to csv')
                self.new_row = {}
                self.is_www = False
        print('Processed %d element(s)' % self.element_count)
        self.element_count += 1

    def characters(self, content):
        if self.is_title:
            if content != 'Home Page':
                self.new_row = {}
                self.is_www = False
            self.is_title = False
        elif self.is_affiliation:
            self.new_row['affiliation'] = content.strip('\"')
            self.is_affiliation = False
        elif self.is_author:
            self.new_row['name'] = content
            self.is_author = False

    def endDocument(self):
        self.csv_writer.write()