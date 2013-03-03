#-*- coding:utf-8 -*-

from pit import Pit
from kindle.highlights import PyKindleHighlights

def main():
    config = Pit.get('amazon.co.jp', {'require': {'email': 'email', 'password': 'password'}})

    kindle = PyKindleHighlights(config['email'], config['password'])

    for k, v in kindle.books2highlights.items():
        print '[title] %s' % k
        print '[author] %s' % v['author']
        for text in v['text']:
            print text
    
if __name__ == '__main__':
    main()
