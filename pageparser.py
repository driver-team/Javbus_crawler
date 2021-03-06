#!/usr/bin/env python
#-*-coding:utf-8-*-

from bs4 import BeautifulSoup
import downloader
import time

def _get_cili_url(soup):
    """get_cili(soup).get the ajax url and Referer url of request"""

    ajax_get_cili_url = 'https://www.javbus.com/ajax/uncledatoolsbyajax.php?lang=zh'
    ajax_data = soup.select('script')[8].text
    for l in ajax_data.split(';')[:-1]:
        ajax_get_cili_url += '&%s' % l[7:].replace("'","").replace(' ','')
    return ajax_get_cili_url


def _parser_magnet(html):
    """parser_magnet(html),get all magnets from a html and return the str of magnet"""

    #存放磁力的字符串
    magnet = ''
    soup = BeautifulSoup(html,"html.parser")
    for td in soup.select('td[width="70%"]'):
        magnet += td.a['href'] + '\n'
    return magnet

def _another_parser_magnet(html):
    magnet_dict={}
    soup = BeautifulSoup(html,"html.parser")
    for tr in soup.select('tr[style=" border-top:#DDDDDD solid 1px"]'):
        m=[]
        magnet= tr.a['href']
        for x in tr.select('a[style="color:#333"]'):
            m.append(x.text.strip())
        magnet_dict[magnet]=m
    return magnet

def get_next_page_url(html):
    """get_next_page_url(html),return the url of next page if exist"""
    print("done the page.......")
    soup = BeautifulSoup(html, "html.parser")
    next_page = soup.select('a[id="next"]')
    if next_page:
        next_page_link = next_page[0]['href']
        # next_page_link = '/'+'/'.join(next_page_link)
        next_page_url = 'https://www.javbus.com' + next_page_link
        return next_page_url
    return None

def parser_genreurl(html):

    soup = BeautifulSoup(html,"html.parser")
    for x in soup.select('a[class="col-lg-2 col-md-2 col-sm-3 col-xs-6 text-center"]'):
        yield x['href']

def parser_homeurl(html):
    """parser_homeurl(html),parser every url on every page and yield the url"""

    soup = BeautifulSoup(html,"html.parser")
    for url in soup.select('a[class="movie-box"]'):
        yield url['href']


def parser_content(html):
    """parser_content(html),parser page's content of every url and yield the dict of content"""

    soup = BeautifulSoup(html, "html.parser")

    categories = {}

    name_doc = soup.find('h3')
    name = name_doc.text if name_doc else ''
    categories['name'] = name

    code_name_doc = soup.find('span', text="識別碼:")
    code_name = code_name_doc.parent.contents[2].text if code_name_doc else ''
    categories['code_name'] = code_name
    #code_name = soup.find('span', text="識別碼:").parent.contents[2].text if soup.find('span', text="識別碼:") else ''

    cover_image_doc = soup.find('a', attrs={"class": "bigImage"})
    cover_image = cover_image_doc.get('href') if cover_image_doc else ''
    categories['cover_image'] = cover_image

    date_issue_doc = soup.find('span', text="發行日期:")
    date_issue = date_issue_doc.parent.contents[1].strip() if date_issue_doc else ''
    categories['release_date'] = date_issue
    #date_issue = soup.find('span', text="發行日期:").parent.contents[1].strip() if soup.find('span', text="發行日期:") else ''

    duration_doc = soup.find('span', text="長度:")
    duration = duration_doc.parent.contents[1].strip() if duration_doc else ''
    categories['duration'] = duration
    #duration = soup.find('span', text="長度:").parent.contents[1].strip() if soup.find('span', text="長度:") else ''

    director_doc = soup.find('span', text="導演:")
    director = director_doc.parent.contents[2].text if director_doc else ''
    categories['director'] = director
    #director = soup.find('span', text="導演:").parent.contents[2].text if soup.find('span', text="導演:") else ''

    manufacturer_doc = soup.find('span', text="製作商:")
    manufacturer = manufacturer_doc.parent.contents[2].text if manufacturer_doc else ''
    categories['manufacturer'] = manufacturer
    #manufacturer = soup.find('span', text="製作商:").parent.contents[2].text if soup.find('span', text="製作商:") else ''

    publisher_doc = soup.find('span', text="發行商:")
    publisher = publisher_doc.parent.contents[2].text if publisher_doc else ''
    categories['publisher'] = publisher
    #publisher = soup.find('span', text="發行商:").parent.contents[2].text if soup.find('span', text="發行商:") else ''

    series_doc = soup.find('span', text="系列:")
    series = series_doc.parent.contents[2].text if series_doc else ''
    categories['series'] = series
    #series = soup.find('span', text="系列:").parent.contents[2].text if soup.find('span', text="系列:") else ''

    genre_doc = soup.find('p', text="類別:")
    genre =(i.text.strip() for i in genre_doc.find_next('p').select('span')) if genre_doc else ''
    #genre =(i.text.strip() for i in soup.find('p', text="類別:").find_next('p').select('span')) if soup.find('p', text="類別:") else ''
    genre_text = ''
    for tex in genre:
        genre_text += '%s   ' % tex
    categories['genre'] = genre_text

    actor_doc = soup.select('span[onmouseover^="hoverdiv"]')
    actor = (i.text.strip() for i in actor_doc) if actor_doc else ''
    #actor = (i.text.strip() for i in soup.select('span[onmouseover^="hoverdiv"]')) if soup.select('span[onmouseover^="hoverdiv"]') else ''
    actor_text = ''
    for tex in actor:
        actor_text += '%s   ' % tex
    categories['actor'] = actor_text

    #网址加入字典
    url = soup.select('link[hreflang="zh"]')[0]['href']
    categories['URL'] = url

    #将磁力链接加入字典
    # time.sleep(5)
    ajax_get_cili_url = _get_cili_url(soup)
    magnet_html = downloader.get_html(ajax_get_cili_url, Referer_url=url)
    magnet = _parser_magnet(magnet_html)
    categories['ajax_get_cili_url'] = ajax_get_cili_url
    categories['magnet'] = magnet

    return categories