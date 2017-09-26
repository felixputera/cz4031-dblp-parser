import xml.sax.handler
from dblp_parser.CsvWriter import CsvWriter


class ArticleHandler(xml.sax.handler.ContentHandler):
    is_article = False
    new_row = {}
    new_row_parent = {}
    csv_writer = CsvWriter(fieldnames=('id', 'title', 'journal', 'author', 'year', 'volume', 'number', 'pages', 'month'), fieldnames_parent=('id', 'key', 'mdate', 'publtype'), fileout='article.txt', fileout_parent='publication.txt')
    is_title = False
    is_journal = False
    is_author = False
    is_year = False
    is_volume = False
    is_number = False
    is_pages = False
    is_month = False
    element_count = 1
    publication_id = 1

    def __init__(self):
        xml.sax.ContentHandler.__init__(self)

    def startElement(self, name, attrs):
        if not self.is_article:
            if name == 'article':
                self.is_article = True
                if 'key' in attrs.getNames():
                    self.new_row_parent['key'] = attrs.getValue('key')
                if 'mdate' in attrs.getNames():
                    self.new_row_parent['mdate'] = attrs.getValue('mdate')
                if 'publtype' in attrs.getNames():
                    self.new_row_parent['publtype'] = attrs.getValue('publtype')
        else:
            if name == 'title':
                self.is_title = True
            elif name == 'journal':
                self.is_journal = True
            elif name == 'author':
                self.is_author = True
            elif name == 'year':
                self.is_year = True
            elif name == 'volume':
                self.is_volume = True
            elif name == 'number':
                self.is_number = True
            elif name == 'pages':
                self.is_pages = True
            elif name == 'month':
                self.is_month = True

    def endElement(self, name):
        if self.is_article:
            if name == 'article':
                if self.new_row:
                    self.new_row['id'] = self.publication_id
                    self.new_row_parent['id'] = self.publication_id
                    self.publication_id += 1
                    self.csv_writer.add_row(self.new_row,0)
                    self.csv_writer.add_row(self.new_row_parent,1)
                    print('Added new row to be output to csv')
                self.new_row = {}
                self.new_row_parent = {}
                self.is_article = False
        print('Processed %d element(s)' % self.element_count)
        self.element_count += 1

    def characters(self, content):
        if self.is_title:
            if 'title' in new_row:
                self.new_row['title'].append(content)
            else:
                self.new_row['title'] = [content]
            self.is_title = False
        elif self.is_journal:
            if 'journal' in new_row:
                self.new_row['journal'].append(content)
            else:
                self.new_row['journal'] = [content]
            self.is_journal = False
        elif self.is_author:
            if 'author' in new_row:
                self.new_row['author'].append(content)
            else:
                self.new_row['author'] = [content]
            self.is_author = False
        elif self.is_year:
            if 'year' in new_row:
                self.new_row['year'].append(content)
            else:
                self.new_row['year'] = [content]
            self.is_year = False
        elif self.is_volume:
            if 'volume' in new_row:
                self.new_row['volume'].append(content)
            else:
                self.new_row['volume'] = [content]
            self.is_volume = False
        elif self.is_number:
            if 'number' in new_row:
                self.new_row['number'].append(content)
            else:
                self.new_row['number'] = [content]
            self.is_number = False
        elif self.is_pages:
            if 'pages' in new_row:
                self.new_row['pages'].append(content)
            else:
                self.new_row['pages'] = [content]
            self.is_pages = False
        elif self.is_month:
            if 'month' in new_row:
                self.new_row['month'].append(content)
            else:
                self.new_row['month'] = [content]
            self.is_month = False


    def endDocument(self):
        self.csv_writer.write()