PyKindleHighlights
==================
Scraping kindle highlights from kindle.amazon.co.jp (jp only)

Example Usage
==================

    from kindle.highlights import PyKindleHighlights

    kindle = PyKindleHighlights("your@email.com", "your_password")

    for highlight in kindle.highlights:
        print '[title] %s' %highlight.title
        print '[author] %s' %highlight.author
        for i in range(len(highlight.text)):
            print '(%d) %s' %(i+1, highlight.text[i])
