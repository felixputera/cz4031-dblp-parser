from xml.sax.handler import ContentHandler

from dblp_parser.CsvWriter import CsvWriter


class AuthorHandler(ContentHandler):

    def __init__(self):
        ContentHandler.__init__(self)

        self.is_www = False
        self.new_row = {}
        self.csv_writer = CsvWriter(fieldnames=('id', 'name', 'affiliation'), fileout='author.txt')
        self.is_title = False
        self.is_affiliation = False
        self.is_author = False
        self.element_count = 1
        self.author_id = 1
        self.content = ''
        self.name_list = []

    def resolveEntity(self, publicId, systemId):
        print('resolveEntity(): %s %s' % (publicId, systemId))
        return systemId

    def skippedEntity(self, name):
        print('skippedEntity(): %s' % name)

    def unparsedEntityDecl(self, name, publicId, systemId, ndata):
        print('unparsedEntityDecl(): %s %s' % (publicId, systemId))

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
        if self.content != '':
            self.content = self.content.strip()
            if self.is_title:
                if self.content not in 'Home Page':
                    self.new_row = {}
                    self.name_list = []
                    self.is_www = False
                else:
                    print('title is homepage')
                self.is_title = False
            elif self.is_affiliation:
                print('isaffiliation' + self.content)
                self.new_row['affiliation'] = self.content.strip('\\"')
                self.is_affiliation = False
            elif self.is_author:
                print('isauthor' + self.content)
                self.name_list.append(self.content)
                self.is_author = False
            self.content = ''
        if self.is_www:
            if name == 'www':
                if self.new_row or self.name_list:
                    self.new_row['id'] = self.author_id
                    self.new_row['name'] = self.name_list
                    self.author_id += 1
                    self.csv_writer.add_row(self.new_row)
                    print(self.new_row)
                    # print('Added new row to be output to csv')
                self.new_row = {}
                self.name_list = []
                self.is_www = False
                print('End of www element. id: %d' % self.author_id)
        # print('Processed %d element(s)' % self.element_count)
        self.element_count += 1

    def characters(self, content):
        self.content += content
        # print(self.content)

    def endDocument(self):
        self.csv_writer.write()
        del self.csv_writer
