#-*- coding: utf-8 -*-

from pit import Pit
import mechanize
import re
import lxml.html

class KindleHighlight(object):
    def __init__(self, email, password, domain='jp'):
        self.br = mechanize.Browser()
        self.br.set_handle_robots(False)
        self.br.addheaders = [("User-agent", "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13")]
        if domain == 'jp':
            page = self.br.open("https://www.amazon.co.jp/ap/signin?openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fkindle.amazon.co.jp%3A443%2Fauthenticate%2Flogin_callback%3Fwctx%3D%252F&pageId=amzn_kindle&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.assoc_handle=amzn_kindle_jp&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0")
        else:
            page = self.br.open("https://www.amazon.com/ap/signin?openid.assoc_handle=amzn_kindle&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.pape.max_auth_age=0&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.return_to=https%3A%2F%2Fkindle.amazon.com%3A443%2Fauthenticate%2Flogin_callback%3Fwctx%3D%252F&pageId=amzn_kindle")

        page.set_data(re.sub('<!DOCTYPE(.*)>', '', page.get_data()))
        self.br.set_response(page)
        self.br.select_form(name = 'signIn')
        self.br['email'] = email
        self.br['password'] = password
        self.highlighted_books = 0

        signedin_page = self.br.submit()
        self.scrape_highlights(signedin_page)

    def scrape_highlights(self, signedin_page):
        highlights_page = self.br.follow_link(url_regex='your_highlights')

        # get next link
        root = lxml.html.fromstring(highlights_page.read())

        hl = root.xpath("//span[@class='highlight']")
        for h in hl:
            print h.text
        next_book = root.xpath("//a[@id='nextBookLink']")
        next_url = ''
        for nb in next_book:
            next_url = nb.attrib['href']
            print nb.attrib['href']
            self.highlighted_books += 1

        # scrape next book
        n1 = self.br.follow_link(url=next_url)

        p1 = lxml.html.fromstring(n1.read())

        hl1 = p1.xpath("//span[@class='highlight']")
        for h in hl1:
            print h.text
        next_book1 = p1.xpath("//a[@id='nextBookLink']")
        next_url1 = ''
        for nb in next_book1:
            next_url1 = nb.attrib['href']
            print next_url1
            self.highlighted_books += 1            

        # scrape next next book
        n2 = self.br.follow_link(url=next_url1)

        p2 = lxml.html.fromstring(n2.read())
        hl2 = p2.xpath("//span[@class='highlight']")
        for h in hl2:
            print h.text
        next_book2 = p2.xpath("//a[@id='nextBookLink']")
        next_url2 = ''
        for nb in next_book2:
            next_url2 = nb.attrib['href']
            print next_url2
            self.highlighted_books += 1            

        # scrape next ** 3 book
        n3 = self.br.follow_link(url=next_url2)

        p3 = lxml.html.fromstring(n3.read())
        next_book3 = p3.xpath("//a[@id='nextBookLink']")
        if len(next_book3) == 0:
            print 'end'
        else:
            for nb in next_book3:
                print nb.attrib['href']
                self.highlighted_books += 1                
        
def main():
    config = Pit.get('amazon.co.jp', {'require': {'email': 'email', 'password': 'password'}})

    domain = 'jp'
    kindle = KindleHighlight(config['email'], config['password'], domain)

    print 'Highlighted Books: %d' % kindle.highlighted_books
    
if __name__ == '__main__':
    main()
