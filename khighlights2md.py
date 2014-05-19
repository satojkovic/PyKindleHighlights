#-*- coding:utf-8 -*-
from docopt import docopt
from pit import Pit
from kindle.highlights import PyKindleHighlights
import html2text


def main():
    config = Pit.get('amazon.co.jp',
                     {'require': {'email': 'email', 'password': 'password'}})

    kindle = PyKindleHighlights(config['email'], config['password'])
    highlights = [highlight for highlight in kindle.highlights]

    for highlight in highlights:
        # title => h4
        print html2text.html2text("<h4>" + highlight.title + "</h4>")
        # author => emphasis
        print html2text.html2text("__" + highlight.author + "__")
        # text => unorederd list
        html = "<ul>"
        for hl_text in highlight.text:
            html += "<li>" + hl_text + "</li>"
        html += "</ul>"
        print html2text.html2text(html)

if __name__ == '__main__':
    main()
