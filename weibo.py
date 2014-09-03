#!/usr/bin/env python
#coding=utf-8

from utils import crawl
from model import weibodata
import datetime
import config
import urllib2
import json
import re

class Weibo:

    '''抓数据主函数'''
    @classmethod
    def do_weibo(cls, names):
        weibo_data_all = []
        for name in names:
            weibo_data = weibodata.WeiboData()
            weibo_data.name = name

            #微博名的搜索地址
            name_url = cls.__gen_name_url(name)
            html_contain_real_home_url = crawl.crawl_weibo(name_url)

            #用户的微博主页地址
            real_home_url = cls.__get_real_home_url(html_contain_real_home_url)
            weibo_data.home_url = real_home_url

            html_weibo_home = crawl.crawl_weibo(real_home_url)
            weibo_data.guanzhu_num = cls.__get_home_guanzhu_num(html_weibo_home)
            weibo_data.fensi_num = cls.__get_home_fensi_num(html_weibo_home)
            weibo_data.weibo_num = cls.__get_home_weibo_num(html_weibo_home)
            #微博主页中的'微博'标签页地址
            real_weibo_url = cls.__get_real_weibo_url(html_weibo_home)

            domain_id = cls.__get_domain_id_from_real_url(real_weibo_url)

            user_id = cls.__get_user_id_from_real_url(real_weibo_url)

            html_real_weibo_url = crawl.crawl_weibo(real_weibo_url)
            #解析'微博'标签页中的数据
            latest_weibo_data = cls.__fetch_latest_data(html_real_weibo_url)

            #如果第一页中的数据不够, 发ajax请求, 请求第一页的所有数据
            weibo_data.latest_weibo = cls.__fetch_all_data(domain_id, user_id, latest_weibo_data)

            weibo_data_all.append(weibo_data)

        return weibo_data_all

    '''生成按名字搜索的页面地址'''
    @classmethod
    def __gen_name_url(cls, name):
        if name == '':
            raise Exception, '1'
        return config.BASE_URL_NAME_SEARCH + urllib2.quote(urllib2.quote(name).encode()).encode()

    '''获取按名字搜索页面中的真实地址'''
    @classmethod
    def __get_real_home_url(cls, real_home_html):
        try:
            name_start = real_home_html.find('star_name')
            if name_start < 0:
                name_start = real_home_html.find('person_name')
            href_start = real_home_html.find('href', name_start)
            href_end = real_home_html.find(' ', href_start + 1)
            href_all = real_home_html[href_start : href_end]
            return (href_all[href_all.find('=') + 1 :]).replace("\\", '').strip("=\"")
        except:
            raise Exception, '2'

    '''获取用于微博主页的'微博'标签页地址'''
    @classmethod
    def __get_real_weibo_url(cls, real_name_url):
        try:
            start = real_name_url.find('pftb_itm S_line1')
            end = real_name_url.find('主页', start)
            tmp = real_name_url[(start + 1) : end]
            real_weibo_url = ''
            for i in range(1000):
                start = tmp.find('pftb_itm S_line1')
                if start == -1:
                    href = tmp[tmp.find('href') : end]
                    href = href[href.find('=') : href.find(' ')]
                    real_weibo_url = config.BASE_URL + href.replace("\\", '').strip("=\"")
                    break
                else:
                    tmp = tmp[(start + 1) : end]
            real_weibo_url = real_weibo_url.replace('home', 'weibo')
            return real_weibo_url
        except:
            raise Exception, '3'

    '''获取微博的数据'''
    @classmethod
    def __fetch_latest_data(cls, html_weibo):
        latest_weibo = []
        #这里解析出含有数据的html片段
        start_1 = html_weibo.rfind('<script', 0, html_weibo.find('pl.content.homeFeed.index'))
        end_1 = html_weibo.find('</script>', start_1)
        html_data = html_weibo[start_1 : end_1].strip()

        #使用BeautifulSoup, lxml总出问题, 好吧, 还是分割字符串吧
        start = html_data.find('WB_feed_type SW_fun S_line2')
        while start > 0:
            div_index_start = html_data.rfind('div', 0, start)
            div_index_end = html_data.find('>', start)
            feedtype_index = html_data.find('feedtype', div_index_start, div_index_end)
            if feedtype_index < 0:
                weibo_item = weibodata.WeiboItem()
                next_start = html_data.find('WB_feed_type SW_fun S_line2', start + 1)
                next_start = next_start if next_start > 0 else len(html_data)

                wb_handle_index = html_data.rfind('WB_handle', start, next_start)

                zan_start = html_data.find('<a', wb_handle_index)
                zan_end = html_data.find('/a>', zan_start)
                zan_end = html_data.rfind(')', zan_start, zan_end)
                zan_start = html_data.rfind('(', zan_start, zan_end)
                zan = html_data[zan_start + 1 : zan_end]

                zhuanfa_start = html_data.find('<a', zan_end)
                zhuanfa_end = html_data.find('/a>', zhuanfa_start)
                zhuanfa_end = html_data.rfind(')', zhuanfa_start, zhuanfa_end)
                zhuanfa_start = html_data.rfind('(', zhuanfa_start, zhuanfa_end)
                zhuanfa = html_data[zhuanfa_start + 1 : zhuanfa_end]

                shoucang_start = html_data.find('<a', zhuanfa_end)
                shoucang_end = html_data.find('/a>', shoucang_start)

                pinglun_start = html_data.find('<a', shoucang_end)
                pinglun_end = html_data.find('/a>', pinglun_start)
                pinglun_end = html_data.rfind(')', pinglun_start, pinglun_end)
                pinglun_start = html_data.rfind('(', pinglun_start, pinglun_end)
                pinglun = html_data[pinglun_start + 1 : pinglun_end]

                weibo_item.zan_num = int(zan)
                weibo_item.zhuanfa_num = int(zhuanfa)
                weibo_item.pinglun_num = int(pinglun)

                wb_from_index = html_data.rfind('WB_from', start, next_start)

                send_date_start = html_data.find('<a', wb_from_index)
                send_date_end = html_data.find('/a>', send_date_start)
                send_date_end = html_data.rfind('<', send_date_start, send_date_end)
                send_date_start = html_data.rfind('>', send_date_start, send_date_end)
                send_date = html_data[send_date_start + 1 : send_date_end].strip()
                if send_date.find('分钟') >= 0:
                    weibo_item.send_date = datetime.datetime.now() + datetime.timedelta(minutes = int(send_date[0 : send_date.find('分钟')]) * (-1))
                elif send_date.find('今天') >= 0:
                    weibo_item.send_date = datetime.datetime.strptime(send_date.replace('今天', datetime.datetime.now().strftime('%Y-%m-%d')), '%Y-%m-%d %H:%M')
                elif send_date.find('月') >= 0:
                    weibo_item.send_date = datetime.datetime.strptime(str(datetime.datetime.now().year) + '-' + send_date.replace('月', '-').replace('日', ''), '%Y-%m-%d %H:%M')
                else:
                    weibo_item.send_date = datetime.datetime.strptime(send_date, '%Y-%m-%d %H:%M')

                send_type_start = html_data.find('<a', send_date_end)
                send_type_end = html_data.find('/a>', send_type_start)
                send_type_end = html_data.rfind('<', send_type_start, send_type_end)
                send_type_start = html_data.rfind('>', send_type_start, send_type_end)
                send_type = html_data[send_type_start + 1 : send_type_end].strip()
                if send_type.find('Android') >= 0:
                    weibo_item.send_type = weibodata.WeiboItem.SEND_TYPE_ANDRIOD
                elif send_type.find('weibo') >= 0:
                    weibo_item.send_type = weibodata.WeiboItem.SEND_TYPE_WEIBO
                elif send_type.find('360安全浏览器') >= 0:
                    weibo_item.send_type = weibodata.WeiboItem.SEND_TYPE_360BROWSER
                elif send_type.find('搜狗高速浏览器') >= 0:
                    weibo_item.send_type = weibodata.WeiboItem.SEND_TYPE_SOUGOUBROWSER
                elif send_type.find('iPhone 5s') >= 0:
                    weibo_item.send_type = weibodata.WeiboItem.SEND_TYPE_IPHNOE_5S
                elif send_type.find('iPhone') >= 0:
                    weibo_item.send_type = weibodata.WeiboItem.SEND_TYPE_IPHNOE
                elif send_type.find('定时showone') >= 0:
                    weibo_item.send_type = weibodata.WeiboItem.SEND_TYPE_SHOWONE

                latest_weibo.append(weibo_item)

            start = html_data.find('WB_feed_type SW_fun S_line2', start + 1)

        return latest_weibo

    '''获取微博主页的关注数'''
    @classmethod
    def __get_home_guanzhu_num(cls, html_weibo):
        guanzhu_start = html_weibo.find('pf_head_pic')
        if guanzhu_start >= 0:
            guanzhu_start = html_weibo.find('<strong', guanzhu_start)
            guanzhu_end = html_weibo.find('/strong>', guanzhu_start)
            guanzhu_start = html_weibo.rfind('>', guanzhu_start, guanzhu_end)
            guanzhu_end = html_weibo.rfind('<', guanzhu_start, guanzhu_end)
            return int(html_weibo[guanzhu_start + 1 : guanzhu_end])
        else:
            return 0

    '''获取微博主页的粉丝数'''
    @classmethod
    def __get_home_fensi_num(cls, html_weibo):
        fensi_start = html_weibo.find('pf_head_pic')
        if fensi_start >= 0:
            fensi_start = html_weibo.find('<strong', fensi_start)
            fensi_start = html_weibo.find('<strong', fensi_start + 1)
            fensi_end = html_weibo.find('/strong>', fensi_start)
            fensi_start = html_weibo.rfind('>', fensi_start, fensi_end)
            fensi_end = html_weibo.rfind('<', fensi_start, fensi_end)
            return int(html_weibo[fensi_start + 1 : fensi_end])
        else:
            return 0

    '''获取微博主页的微博数'''
    @classmethod
    def __get_home_weibo_num(cls, html_weibo):
        weibo_start = html_weibo.find('pf_head_pic')
        if weibo_start >= 0:
            weibo_start = html_weibo.find('<strong', weibo_start)
            weibo_start = html_weibo.find('<strong', weibo_start + 1)
            weibo_start = html_weibo.find('<strong', weibo_start + 1)
            weibo_end = html_weibo.find('/strong>', weibo_start)
            weibo_start = html_weibo.rfind('>', weibo_start, weibo_end)
            weibo_end = html_weibo.rfind('<', weibo_start, weibo_end)
            return int(html_weibo[weibo_start + 1 : weibo_end])
        else:
            return 0

    '''获取domain_id'''
    @classmethod
    def __get_domain_id_from_real_url(cls, real_url):
        domain_start = real_url.find('page_')
        domain_end = real_url.find('&', domain_start)
        if domain_end < 0:
            domain_end = real_url.find('#', domain_start)
        return real_url[domain_start + len('page_') : domain_end]

    '''获取用户id'''
    @classmethod
    def __get_user_id_from_real_url(cls, real_url):
        real_url_tmp = real_url.lstrip('abcdefghijklmnopqrstuvwxyz:/.')
        return real_url_tmp[0 : real_url_tmp.find('/')]

    '''滚动页面的ajax请求地址,一共有两次滚动,所以roll_num只能取1, 2'''
    @classmethod
    def __first_roll_ajax_url(cls, domain_id, page_num, roll_num, id):
        return 'http://weibo.com/p/aj/mblog/mbloglist?domain=' + domain_id + '&pre_page=' + page_num + '&page=' + page_num + '&pagebar=' + roll_num + '&id=' + id

    '''获取最近7天内的所有微博'''
    @classmethod
    def __fetch_all_data(cls, domain_id, user_id, latest_weibo_data):
        if len(latest_weibo_data) > 0:
            print domain_id, user_id, latest_weibo_data[len(latest_weibo_data) - 1].send_date

if __name__ == "__main__":
    Weibo.do_weibo(['英国报姐', '张伯庸'])
