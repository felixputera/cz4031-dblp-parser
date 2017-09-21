from lxml import etree
from dblp_parser.CsvWriter import CsvWriter


def parse_author(source_file):
    csv_writer = CsvWriter(fieldnames=['id', 'name', 'affiliation'], fileout='author.txt')

    is_www = False
    new_row = {}
    line = 1

    for event, elem in etree.iterparse(source_file, events=['start', 'end'],
                                       load_dtd=False, dtd_validation=False, huge_tree=True):
        if event == 'start' and elem.tag == 'www':
            is_www = True
        elif is_www and event == 'end':
            if elem.tag == 'author':
                new_row['name'] = elem.text
            elif elem.tag == 'title' and elem.text != 'Home Page':
                new_row = {}
                is_www = False
            elif elem.tag == 'note' and 'type' in elem.attrib and elem.attrib['type'] == 'affiliation':
                new_row['affiliation'] = elem.text
            elif elem.tag == 'www':
                if new_row:
                    csv_writer.add_row(new_row)
                new_row = {}
                is_www = False

        elem.clear()

        print('Processed line %d' % line)
        line += 1

    csv_writer.write()