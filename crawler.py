#!/usr/bin/env python
#-*-coding:utf-8-*-

import controler
import downloader
import pageparser
import time
import sqlite3
import string
import os

# 250/274
# finish_list = [
#     '62', '5g', '59', '57', '52', '4y', '4r', '4e', '4d', '4a', '49', '44', '41',
#     '40', '3x', '3w', '3v', '3t', '3r', '3g', '3e', '3d', '3c', '3b', '37', '35',
#     '2y', '2x', '2v', '2t', '2r', '2e', '2d', '20', '1y', '1u', '1i', '1e', '1d',
#     '11', '6h', '5l', '5p', '61', '6i', '6j', '6k', '6l', '6n', '6o', '6p', '6q',
#     '6r', '6s', '6t', '6u', '6v', '6w', '77', '7d', '7c', '7f', '7g', '7h', '7i',
#     '7j', '7t', '7u', '7v', '7w', '5w', '5k', '5i', '5f', '58', '4s', '4l', '4h',
#     '3o', '39', '38', '34', '32', '30', '2z', '2w', '2q', '2o', '2f', '2b', '2a',
#     '29', '27', '26', '23', '21', '1x', '1v', '1n', '1k', '1c', '17', '10', 'z',
#     'p', 'c', 'b', '7', '5r', '65', '64', '6c', '6f', '5v', '5u', '5h', '5c','5b',
#     '56', '55', '50', '4z', '4p', '4n', '4k', '4i', '3i', '3a', '2s', '2m','2l',
#     '28', '1w', '18', '12', 'y', 'v', 'm', 'l', 'k', 'j', 'i', 'a', '9', '8','1',
#     '6b', '5x', '5d', '4x', '3n', '3k', '2k', '2i', '2g', '22', '1t', '1f','15',
#     '13', 'w', 't', 'e', '4w', '4t', '4j', '47', '46','45','42','3q','3l','3f',
#     '2h', '24', '1z', '1s', '1r', '1p', '1o', '1j', '19', 'x', 'u', 'r', 'n', 'h',
#     '5', '4', '6m', '51','4f', '4c', '4b', '3z', '3y', '3s', '3p', '3m', '3h', '36',
#     '2u', '25', '1q', '1m', '1l', '1h','1b', '1a', '14', 'q', 'd', '6', '3', '5m',
#     '5y', '63', '60', '5z', '5t', '5s', '5q', '5o', '5n','5j', '5e', '5a', '54', '53',
#     '4v','4u','4q','4o','4m','48','43','3u','3j','33','31','2p','2n','2c','1g',
#     '16','s','o','g','f','2','hd','sub','2j','4g','66','69','6a','70','71','72',
#     '73','74','75','76','7k','7l','7m','7n','7o','7p','7q','7r','7s','7x']

#384
finish_list=['hd', 'sub', '1bc', 'yz', '3q', '8q', 'ap', '8y', '29', '8w', 'au',
 'nc', 'ee', '19o', '7z', 'bk', '17g', '6p', 'eu', 'xx', 'jm', 'vr', 'bd', 'vn',
 '164', 'ui', 'u4', '1cu', 'v6', 'sb', 'y2', 'pm', 'e5', 't9', '1cw', 'gc', 'wd',
 '12d', '7d', '7g', '8i', 'gre001', 'gre002', 'gre003', 'gre004', 'gre005', 'gre006',
 'gre007', 'gre008', 'gre009', 'gre010', 'gre011', 'gre012', 'gre013', 'gre014', 'gre015',
 'gre016', 'gre017', 'gre018', 'gre019', 'gre020', 'gre021', 'gre153', 'c', '2r', 'yg', '3',
 '1av', '18', '1y', 'wc', '13', 'jk', 'bm', 'r5', '18t', 'mr', 'o4', 'm8', '11x', '43', '165',
 '1a1', '12r', 'pk', '1co', '48', '9a', '3r', '5d', 'ok', 'ad', 'ct', '2e', '1d3', '8d', 'sv',
 '1bx', 'gre022', 'gre023', 'gre024', 'gre025','gre026', 'gre027', 'gre028', 'gre029', 'gre030',
 'gre031', 'gre032', 'gre033', 'gre034', 'gre035', 'gre036', 'gre037', 'gre038', 'gre039',
 'gre040', 'gre041', 'gre042', 'gre043', 'gre044', 'gre045', 'gre046', 'gre047',
 'gre048', '2', '5x', '19t', 'gv', 'mx', 'cd', '3i', 'ce', '16w', '17y', 'jg', 'qm', 'f8',
 'ab', '88', '1di', 'wz', '14', 'f7', '17h', 'du', 'hm', '1dp', 'vx', '1bu', '17i',
 'gre049', 'gre050', 'gre051', 'gre052', 'gre053', 'gre054', 'gre055', 'gre056', 'gre057',
 'gre058', 'gre059', 'gre060', 'gre061', 'gre062', 'gre063', '1da', 'zc', 'bl', '5g', '66',
 'wy', '5h', '3z', '9x', '4s', '1dd', '1b4', '17s', '199', 'mu', 'gz', 'i0', 'gre064', 'gre065',
 'gre066', 'gre067','gre068', 'gre069','gre070', 'gre071', 'gre072', 'gre073', 'gre074', 'gre075',
 'gre076', 'gre077', 'gre078', 'gre079', 'gre080', 'gre081', 'gre082', 'i', '34', '3x', '11a',
 'c2', 'v4', '5u', '11e', 'uc', '14w', '141', '110', 'kp', 'tc', 'kv', '10p', '12p',
 '124', '11p', '13a', '134', '12x', '128', '14d', '2c', '12l', '13r', '14v',
 'gre083', 'gre084', 'gre085', 'gre086', 'gre087', 'gre088', 'gre089']
undo=['4o']


def get_genre(url):
    genre_html = downloader.get_html(url)
    for genre_url in pageparser.parser_genreurl(genre_html):
        if genre_url.split('/')[-1] in finish_list:
            continue
        main(genre_url)
        print 'finish genre_url:{}'.format(genre_url)


def get_dict(url):
    """get the dict of the detail page and yield the dict"""

    url_html = downloader.get_html(url)
    for detail_url in pageparser.parser_homeurl(url_html):
        try:
            detail_page_html = downloader.get_html(detail_url)
            dict_jav = pageparser.parser_content(detail_page_html)
        except:
            with open('fail_url.txt', 'a') as fd:
                fd.write('%s\n' % detail_url)
            print("Fail to crawl %s\ncrawl next detail page......" %
                  detail_url)
            continue
        yield dict_jav, detail_url


def join_db(url, is_uncensored):
    """the detail_dict of the url join the db"""

    for dict_jav_data, detail_url in get_dict(url):
        if controler.check_url_not_in_table(url):

            controler.write_data(dict_jav_data, is_uncensored)
            print("Crawled %s" % detail_url)
        else:
            print("it has updated over...window will be closed after 60s")
            time.sleep(60)
            exit()


def main(entrance):
    # 创建数据表
    if not os.path.exists("javbus.sqlite3.db"):
        controler.create_db()
    # 无码为1，有码为0
    is_uncensored = 1 if 'uncensored' in entrance else 0
    join_db(entrance, is_uncensored)
    print "entrance:{}".format(entrance)

    entrance_html = downloader.get_html(entrance)
    next_page_url = pageparser.get_next_page_url(entrance_html)
    while True:
        if next_page_url:
            join_db(next_page_url, is_uncensored)
        if next_page_url == None:
            break
        next_page_html = downloader.get_html(next_page_url)
        print 'next page url:{}'.format(next_page_url)
        next_page_url = pageparser.get_next_page_url(next_page_html)
        if next_page_url == None:
            break


if __name__ == '__main__':
    # main('https://www.javbus.com/')
    # main('https://www.javbus.com/uncensored')
    # get_genre('https://www.javbus.com/genre/')
    get_genre('https://www.javbus.com/uncensored/genre/')
    
    # main('https://www.javbus.com/genre/4o')
