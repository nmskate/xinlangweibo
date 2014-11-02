#!/usr/bin/env python3
# coding=utf-8

from utils import HttpUtils
from model import MicroBlogModel
import datetime
import Configuration
import urllib
import time


#抓数据主函数
def fetch_weibo(sheet_item):
    weibo_data_all = []
    for data_item in sheet_item.data_items:
        weibo_data = MicroBlogModel.MicroBlogHome()
        weibo_data.name = data_item.bozhu_name
        weibo_data.bozhu_excel_name = data_item.bozhu_excel_name
        weibo_data.data_status = MicroBlogModel.MicroBlogHome.DATA_STATUS_OK
        if data_item.status_code == MicroBlogModel.MicroBlogHome.DATA_STATUS_OK:
            weibo_data.home_url = data_item.link
            weibo_data.per_zhuanfa_num = data_item.per_zhuanfa_num
            weibo_data.fensi_num = int(data_item.fensi_num)
            weibo_data.num = data_item.num
        else:
            try:
                #如果excel中的链接地址不为空，校验链接的有效性和博主是否改名了，如果改名了就跳过这条博客。如果链接地址为空，根据博主名，查询链接地址
                if data_item.link.strip() != "":
                    weibo_data.home_url = data_item.link.strip()
                    if not HttpUtils.correct_weibo_head(weibo_data.home_url):
                        weibo_data.data_status = MicroBlogModel.MicroBlogHome.DATA_STATUS_URL_ERROR
                        raise Exception
                else:
                    html_contain_real_home_url = HttpUtils.crawl_weibo(__gen_name_url(data_item.bozhu_name))
                    #用户的微博主页地址
                    real_home_url = __get_real_home_url(data_item.bozhu_name, html_contain_real_home_url)
                    weibo_data.home_url = real_home_url

                html_weibo_home = HttpUtils.crawl_weibo(weibo_data.home_url)
                weibo_data.guanzhu_num = __get_home_guanzhu_num(html_weibo_home)
                weibo_data.fensi_num = __get_home_fensi_num(html_weibo_home)
                weibo_data.weibo_num = __get_home_weibo_num(html_weibo_home)
                #微博主页中的'微博'标签页地址
                real_weibo_url = __get_real_weibo_url(html_weibo_home)

                domain_id = __get_domain_id_from_real_url(real_weibo_url)
                user_id = __get_user_id_from_real_url(real_weibo_url)

                #解析'微博'标签页中的数据，默认请求７天内的数据
                weibo_data.latest_weibo = __fetch_all_data(domain_id, user_id, real_weibo_url)
            except:
                if weibo_data.data_status != MicroBlogModel.MicroBlogHome.DATA_STATUS_OK:
                    weibo_data.data_status = MicroBlogModel.MicroBlogHome.DATA_STATUS_ERROR
                weibo_data.latest_weibo = []
                print(data_item.bozhu_excel_name, "的微博信息获取失败，跳过该博客")
            else:
                print(weibo_data.name, weibo_data.home_url, len(weibo_data.latest_weibo))

        weibo_data_all.append(weibo_data)
        time.sleep(1)

    return weibo_data_all


#生成按名字搜索的页面地址
def __gen_name_url(name):
    if name == '':
        raise Exception
    return Configuration.BASE_URL_NAME_SEARCH + urllib.parse.quote(urllib.parse.quote(name))


#获取按名字搜索页面中的真实地址
def __get_real_home_url(name, real_home_html):
    try:
        name_start = 0
        title = ""
        while title.strip() != name.strip() and name_start != -1:
            name_start_1 = real_home_html.find('star_name', name_start + 1)
            name_start_2 = real_home_html.find('person_name', name_start + 1)
            name_start = name_start_1 if 0 < name_start_1 < name_start_2 else name_start_2
            title_start = real_home_html.find('title', name_start)
            title_end = real_home_html.find(' ', title_start + 1)
            title_all = real_home_html[title_start:title_end]
            title = eval("u'" + (title_all[title_all.find('=') + 1:]).replace("\\\"", "") + "'").encode('utf-8')

        if name_start == -1:
            return ""
        else:
            href_start = real_home_html.find('href', name_start)
            href_end = real_home_html.find(' ', href_start + 1)
            href_all = real_home_html[href_start:href_end]
            return (href_all[href_all.find('=') + 1:]).replace("\\", '').strip("=\"")
    except:
        raise Exception


#获取用于微博主页的'微博'标签页地址
def __get_real_weibo_url(real_name_url):
    try:
        start = real_name_url.find('pftb_itm S_line1')
        end = real_name_url.find('主页', start)
        tmp = real_name_url[(start + 1):end]
        real_weibo_url = ''
        for i in range(100):
            start = tmp.find('pftb_itm S_line1')
            if start == -1:
                href = tmp[tmp.find('href'):end]
                href = href[href.find('='):href.find(' ')]
                real_weibo_url = Configuration.BASE_URL + href.replace("\\", '').strip("=\"")
                break
            else:
                tmp = tmp[(start + 1):end]
        real_weibo_url = real_weibo_url.replace('home', 'weibo')
        real_weibo_url = real_weibo_url[0:real_weibo_url.find('#')]
        return real_weibo_url
    except:
        raise Exception


#获取微博的数据
def __fetch_latest_data(html_weibo):
    latest_weibo = []
    #使用BeautifulSoup, lxml总出问题, 好吧, 还是分割字符串吧
    start = html_weibo.find('WB_feed_type SW_fun S_line2')
    while start > 0:
        div_index_start = html_weibo.rfind('div', 0, start)
        div_index_end = html_weibo.find('>', start)
        feedtype_index = html_weibo.find('feedtype', div_index_start, div_index_end)
        if feedtype_index < 0:
            weibo_item = MicroBlogModel.WeiboItem()
            next_start = html_weibo.find('WB_feed_type SW_fun S_line2', start + 1)
            next_start = next_start if next_start > 0 else len(html_weibo)

            wb_handle_index = html_weibo.rfind('WB_handle', start, next_start)

            zan_start = html_weibo.find('<a', wb_handle_index)
            zan_end = html_weibo.find('/a>', zan_start)
            zan_end = html_weibo.rfind(')', zan_start, zan_end)
            zan_start = html_weibo.rfind('(', zan_start, zan_end)
            zan = html_weibo[zan_start + 1:zan_end]

            zhuanfa_start = html_weibo.find('<a', zan_end)
            zhuanfa_end = html_weibo.find('/a>', zhuanfa_start)
            zhuanfa_end = html_weibo.rfind(')', zhuanfa_start, zhuanfa_end)
            zhuanfa_start = html_weibo.rfind('(', zhuanfa_start, zhuanfa_end)
            zhuanfa = html_weibo[zhuanfa_start + 1:zhuanfa_end]

            shoucang_start = html_weibo.find('<a', zhuanfa_end)
            shoucang_end = html_weibo.find('/a>', shoucang_start)

            pinglun_start = html_weibo.find('<a', shoucang_end)
            pinglun_end = html_weibo.find('/a>', pinglun_start)
            pinglun_end = html_weibo.rfind(')', pinglun_start, pinglun_end)
            pinglun_start = html_weibo.rfind('(', pinglun_start, pinglun_end)
            pinglun = html_weibo[pinglun_start + 1:pinglun_end]

            weibo_item.zan_num = int(zan)
            weibo_item.zhuanfa_num = int(zhuanfa)
            weibo_item.pinglun_num = int(pinglun)

            wb_from_index = html_weibo.rfind('WB_from', start, next_start)

            send_date_start = html_weibo.find('<a', wb_from_index)
            send_date_end = html_weibo.find('/a>', send_date_start)
            send_date_end = html_weibo.rfind('<', send_date_start, send_date_end)
            send_date_start = html_weibo.rfind('>', send_date_start, send_date_end)
            send_date = html_weibo[send_date_start + 1:send_date_end].strip()

            #ajax请求的数据中是unicode字符串,需要替换unicode字符串
            if send_date.find('分钟') >= 0:
                weibo_item.send_date = datetime.datetime.now() + datetime.timedelta(minutes=int(send_date[0:send_date.find('分钟')]) * (-1))
            elif send_date.find('今天') >= 0:
                weibo_item.send_date = datetime.datetime.strptime(send_date.replace('今天', datetime.datetime.now().strftime('%Y-%m-%d')), '%Y-%m-%d %H:%M')
            elif send_date.find('\\u4eca\\u5929') >= 0:
                weibo_item.send_date = datetime.datetime.strptime(send_date.replace('\\u4eca\\u5929', datetime.datetime.now().strftime('%Y-%m-%d')), '%Y-%m-%d %H:%M')
            elif send_date.find('月') >= 0:
                weibo_item.send_date = datetime.datetime.strptime(str(datetime.datetime.now().year) + '-' + send_date.replace('月', '-').replace('日', ''), '%Y-%m-%d %H:%M')
            elif send_date.find('\u6708') >= 0:
                weibo_item.send_date = datetime.datetime.strptime(str(datetime.datetime.now().year) + '-' + send_date.replace('\u6708', '-').replace('\u65e5', ''),'%Y-%m-%d %H:%M')
            else:
                weibo_item.send_date = datetime.datetime.strptime(send_date, '%Y-%m-%d %H:%M')

            send_type_start = html_weibo.find('<a', send_date_end)
            send_type_end = html_weibo.find('/a>', send_type_start)
            send_type_end = html_weibo.rfind('<', send_type_start, send_type_end)
            send_type_start = html_weibo.rfind('>', send_type_start, send_type_end)
            send_type = html_weibo[send_type_start + 1:send_type_end].strip()
            if send_type.find('Android') >= 0:
                weibo_item.send_type = MicroBlogModel.WeiboItem.SEND_TYPE_ANDRIOD
            elif send_type.find('weibo') >= 0:
                weibo_item.send_type = MicroBlogModel.WeiboItem.SEND_TYPE_WEIBO
            elif send_type.find('360安全浏览器') >= 0:
                weibo_item.send_type = MicroBlogModel.WeiboItem.SEND_TYPE_360BROWSER
            elif send_type.find('搜狗高速浏览器') >= 0:
                weibo_item.send_type = MicroBlogModel.WeiboItem.SEND_TYPE_SOUGOUBROWSER
            elif send_type.find('iPhone 5s') >= 0:
                weibo_item.send_type = MicroBlogModel.WeiboItem.SEND_TYPE_IPHNOE_5S
            elif send_type.find('iPhone') >= 0:
                weibo_item.send_type = MicroBlogModel.WeiboItem.SEND_TYPE_IPHNOE
            elif send_type.find('定时showone') >= 0:
                weibo_item.send_type = MicroBlogModel.WeiboItem.SEND_TYPE_SHOWONE

            latest_weibo.append(weibo_item)

        start = html_weibo.find('WB_feed_type SW_fun S_line2', start + 1)

    return latest_weibo


#获取微博主页的关注数
def __get_home_guanzhu_num(html_weibo):
    guanzhu_start = html_weibo.find('pf_head_pic')
    if guanzhu_start >= 0:
        guanzhu_start = html_weibo.find('<strong', guanzhu_start)
        guanzhu_end = html_weibo.find('/strong>', guanzhu_start)
        guanzhu_start = html_weibo.rfind('>', guanzhu_start, guanzhu_end)
        guanzhu_end = html_weibo.rfind('<', guanzhu_start, guanzhu_end)
        return int(html_weibo[guanzhu_start + 1:guanzhu_end])
    else:
        return 0


#获取微博主页的粉丝数
def __get_home_fensi_num(html_weibo):
    fensi_start = html_weibo.find('pf_head_pic')
    if fensi_start >= 0:
        fensi_start = html_weibo.find('<strong', fensi_start)
        fensi_start = html_weibo.find('<strong', fensi_start + 1)
        fensi_end = html_weibo.find('/strong>', fensi_start)
        fensi_start = html_weibo.rfind('>', fensi_start, fensi_end)
        fensi_end = html_weibo.rfind('<', fensi_start, fensi_end)
        return int(html_weibo[fensi_start + 1:fensi_end])
    else:
        return 0


#获取微博主页的微博数
def __get_home_weibo_num(html_weibo):
    weibo_start = html_weibo.find('pf_head_pic')
    if weibo_start >= 0:
        weibo_start = html_weibo.find('<strong', weibo_start)
        weibo_start = html_weibo.find('<strong', weibo_start + 1)
        weibo_start = html_weibo.find('<strong', weibo_start + 1)
        weibo_end = html_weibo.find('/strong>', weibo_start)
        weibo_start = html_weibo.rfind('>', weibo_start, weibo_end)
        weibo_end = html_weibo.rfind('<', weibo_start, weibo_end)
        return int(html_weibo[weibo_start + 1:weibo_end])
    else:
        return 0


#获取domain_id
def __get_domain_id_from_real_url(real_url):
    domain_start = real_url.find('page_')
    domain_end = real_url.find('&', domain_start)
    if domain_end < 0:
        domain_end = real_url.find('#', domain_start)
    return real_url[domain_start + len('page_'):domain_end]


#获取用户id
def __get_user_id_from_real_url(real_url):
    real_url_tmp = real_url.lstrip('abcdefghijklmnopqrstuvwxyz:/.')
    return real_url_tmp[0: real_url_tmp.find('/')]


#滚动页面的ajax请求地址,一共有两次滚动,所以roll_num只能取0, 1
def __first_roll_ajax_url(domain_id, page_num, roll_num, user_id):
    return 'http://weibo.com/p/aj/mblog/mbloglist?domain=' + str(domain_id) + '&pre_page=' + str(page_num) + '&page=' + str(page_num) + '&pagebar=' + str(roll_num) + '&id=' + str(user_id)


#获取最近7天内的所有微博
def __fetch_all_data(domain_id, user_id, weibo_url):
    curr_date = datetime.datetime.now()
    page_num = 1
    latest_weibo_data = []
    while True:
        if len(latest_weibo_data) > 0 and (
            curr_date - latest_weibo_data[len(latest_weibo_data) - 1].send_date).days > 7:
            break;
        #生成第i页地址
        page_weibo_url = weibo_url + "&page=" + str(page_num)
        #先检测微博页面地址是否正确
        if HttpUtils.correct_weibo_head(page_weibo_url):
            try:
                #先解析页面上有的数据
                latest_weibo_data = latest_weibo_data + __fetch_latest_data(HttpUtils.crawl_weibo(page_weibo_url))
                #再发ajax请求, 解析第i页剩下的数据, 一共需要发2次ajax请求
                first_ajax_html = HttpUtils.crawl_weibo(__first_roll_ajax_url(domain_id, page_num, 0, user_id))
                second_ajax_html = HttpUtils.crawl_weibo(__first_roll_ajax_url(domain_id, page_num, 1, user_id))
                first_ajax_data = __fetch_latest_data(first_ajax_html)
                second_ajax_data = __fetch_latest_data(second_ajax_html)
                latest_weibo_data = latest_weibo_data + first_ajax_data
                latest_weibo_data = latest_weibo_data + second_ajax_data
            except:
                raise Exception
                break
        else:
            raise Exception
            break

        page_num += 1
    return latest_weibo_data
