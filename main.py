from xml.sax import parse
from dblp_parser.AuthorHandler import AuthorHandler
from dblp_parser.ArticleHandler import ArticleHandler
from dblp_parser.PublicationHandler import PublicationHandler

if __name__ == "__main__":
    incollection_fieldnames = ('p_id', 'title', 'booktitle', 'publisher', 'year', 'editor', 'volume', 'number',
     'series', 'type', 'chapter', 'pages', 'address', 'edition', 'month', 'note')
    handler = PublicationHandler(elementname='incollection', fieldnames=incollection_fieldnames)
    parse('dblp.xml', handler)
