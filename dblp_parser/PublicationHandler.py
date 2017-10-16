import json
import xml.sax.handler

from dblp_parser.CsvWriter import CsvWriter


class PublicationHandler(xml.sax.handler.ContentHandler):

    def __init__(self, elementname, fieldnames):
        xml.sax.ContentHandler.__init__(self)

        self.pub_csv_writer = CsvWriter(fieldnames=('id', 'key', 'mdate', 'title', 'url', 'ee', 'author'),
                                        fileout='publication.txt')
        self.my_fieldnames = fieldnames
        self.my_elementname = elementname
        self.my_csv_writer = CsvWriter(fieldnames=self.my_fieldnames, fileout='%s.txt' % self.my_elementname)

        self.is_field = {value: False for value in self.my_fieldnames}
        self.is_my_element = False

        with open('publication_id.json') as pub_id_json:
            pub_id_dict = json.load(pub_id_json)
            self.pub_id = pub_id_dict[self.my_elementname]

        self.element_count = 1

        self.is_author = False
        self.author_list = []

        self.is_title = False

        self.is_url = False
        self.is_ee = False

        self.pub_row = {}
        self.my_row = {value: [] for value in self.my_fieldnames}

        self.content = ''

    def startElement(self, name, attrs):
        if not self.is_my_element:
            if name == self.my_elementname:
                self.is_my_element = True
                if 'key' in attrs.getNames():
                    self.pub_row['key'] = attrs.getValue('key')
                if 'mdate' in attrs.getNames():
                    self.pub_row['mdate'] = attrs.getValue('mdate')
        else:
            if name == 'author' or name == 'editor':
                self.is_author = True
            if name == 'title':
                self.is_title = True
            elif name == 'url':
                self.is_url = True
            elif name == 'ee':
                self.is_ee = True
            else:
                for fieldname in self.my_fieldnames:
                    if name == fieldname:
                        self.is_field[fieldname] = True
                        break

    def endElement(self, name):
        if name in ['ref', 'sup', 'sub', 'i', 'tt']:
            return
        if self.content != '':
            self.content = self.content.strip()
            if self.is_author:
                self.author_list.append(self.content)
                self.is_author = False
            if self.is_title:
                self.pub_row['title'] = self.content
                self.is_title = False
            elif self.is_url:
                self.pub_row['url'] = self.content
                self.is_url = False
            elif self.is_ee:
                self.pub_row['ee'] = self.content
                self.is_ee = False
            else:
                for fieldname in self.my_fieldnames:
                    if self.is_field[fieldname]:
                        (self.my_row[fieldname]).append(self.content)
                        self.is_field[fieldname] = False
            self.content = ''

        if self.is_my_element:
            if name == self.my_elementname:
                self.pub_row['id'] = self.pub_id
                self.my_row['p_id'] = self.pub_id
                self.pub_id += 1

                self.pub_row['author'] = self.author_list

                self.pub_csv_writer.add_row(self.pub_row)
                self.my_csv_writer.add_row(self.my_row)
                # print('Added new row to 2 csvs')
                self.my_row = {value: [] for value in self.my_fieldnames}
                self.pub_row = {}
                self.is_my_element = False
                self.author_list = []
        # print('Processed %d element(s)' % self.element_count)
        self.element_count += 1

    def characters(self, content):
        self.content += content

    def endDocument(self):
        self.my_csv_writer.write()
        self.pub_csv_writer.write(append=True)
        del self.my_csv_writer
        del self.pub_csv_writer
        print(self.pub_id)
