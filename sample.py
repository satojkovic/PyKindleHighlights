#-*- coding:utf-8 -*-

from pit import Pit
from kindle.highlights import PyKindleHighlights

def main():
    config = Pit.get('amazon.co.jp', {'require': {'email': 'email', 'password': 'password'}})

    kindle = PyKindleHighlights(config['email'], config['password'])

    for highlight in kindle.highlights:
        print '[title] %s' %highlight.title
        print '[author] %s' %highlight.author
        for i in range(len(highlight.text)):
            print '(%d) %s' %(i+1, highlight.text[i])
    
if __name__ == '__main__':
    main()
