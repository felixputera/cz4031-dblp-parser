from xml.sax import parse

from dblp_parser.AuthorHandler import AuthorHandler
from dblp_parser.PublicationHandler import PublicationHandler

if __name__ == "__main__":
    incollection_fieldnames = ('p_id', 'booktitle', 'year', 'pages')
    incollection_handler = PublicationHandler(elementname='incollection', fieldnames=incollection_fieldnames)

    article_fieldnames = ('p_id', 'journal', 'year', 'volume', 'number', 'pages')
    article_handler = PublicationHandler(elementname='article', fieldnames=article_fieldnames)

    inproceedings_fieldnames = ('p_id', 'booktitle', 'year', 'pages',)
    inproceedings_handler = PublicationHandler(elementname='inproceedings', fieldnames=inproceedings_fieldnames)

    thesis_fieldnames = ('p_id', 'school', 'year')
    phdthesis_handler = PublicationHandler(elementname='phdthesis', fieldnames=thesis_fieldnames)
    mastersthesis_handler = PublicationHandler(elementname='mastersthesis', fieldnames=thesis_fieldnames)

    proceedings_fieldnames = ('p_id', 'year', 'volume', 'number', 'series', 'publisher')
    proceedings_handler = PublicationHandler(elementname='proceedings', fieldnames=proceedings_fieldnames)

    book_fieldnames = ('p_id', 'publisher', 'year', 'volume', 'number')
    book_handler = PublicationHandler(elementname='book', fieldnames=book_fieldnames)

    # parse('dblp.xml', incollection_handler)
    # parse('dblp.xml', article_handler)
    # parse('dblp.xml', inproceedings_handler)
    parse('dblp.xml', phdthesis_handler)
    parse('dblp.xml', mastersthesis_handler)
    parse('dblp.xml', book_handler)
    parse('dblp.xml', proceedings_handler)

    author_handler = AuthorHandler()
    parse('dblp.xml', author_handler)
