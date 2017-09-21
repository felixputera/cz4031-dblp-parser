from xml.sax import parse
from dblp_parser.Author import parse_author
from dblp_parser.AuthorHandler import AuthorHandler


if __name__ == "__main__":
    handler = AuthorHandler()
    parse('dblp.xml', handler)