from bs4 import BeautifulSoup

import urllib.request

from crawler import mi_config
from crawler.app_info import AppInfo
from selenium import webdriver

import time

def get_app_detail(app_url, output_file_path , category = "unknow"):
    """
    输入app的url, 在文件中写入app的详细信息:
    名称, 包名, 开发者/开发公司, 评分次数,平均评分, 软件版本, 更新时间
    权限情况 应用简介
    :param app_url
    :return: 讲上树信息按照字典的形式反悔
    """

    if app_url is None:
        return "the input url is None, please check"

    result = {}
    result["category"] = category               # 默认设置为unknow
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {"User-Agent": user_agent}
    print(app_url)
    req = urllib.request.Request(app_url, data= None, headers= headers)

    try :
        with urllib.request.urlopen(req) as response:
            web_page = response.read()
            soup = BeautifulSoup(web_page,"html.parser")
            developer = soup.select(".intro-titles p")
            name = soup.select(".intro-titles h3")
            package = soup.select(".cf .special-li")
            permissions = soup.select(".details .second-ul li")
            category = soup.select(".intro-titles ")
            perm_list = []
            for i in range(len(permissions)):
                perm_list.append(permissions[i].string)
            result["developer"] = developer[0].string
            result["name"] = name[0].string
            result["package"] = package[0].string
            result["permission"] = perm_list
            # result["category"] =
    except urllib.error.URLError :
        current_time = time.localtime()
        hour = current_time[3]
        minute = current_time[4]
        with open("error.log","w+") as f:
            f.writelines(str(hour)+":"+ str(minute)+  "\turl:"+app_url)

        raise Exception

    with open(output_file_path, "a", encoding="utf-8") as f:
        line_list = []
        line_list.append(result["name"])
        line_list.append(result["package"])
        line_list.append(result["developer"])
        line_list.append(mi_categorys[result["category"]][0])
        print(line_list)
        f.write(",".join(line_list))
        f.write("\n")
    return result


# def get_url_pipeline():
#     """
#     返回当前等待爬去的url
#     :return:
#     """
#     return mi_app_url_stack
#
#
# def push_url(url):
#     """
#     在url列表中插入新的url
#     :param url:
#     :return:
#     """
#     mi_app_url_stack.append(url)
#
#
# def pop_url(url):
#     """
#     从URL列表中删除当前的url
#     :param url:
#     :return:
#     """
#     return mi_app_url_stack.pop()


base_url = "http://app.mi.com"
category = "/category/"
web_url = base_url+ category+ str(1)
print(web_url)
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {"User-Agent":user_agent}
req = urllib.request.Request(web_url, headers)
mi_app_url_stack = []
app_list = []

mi_categorys = mi_config.mi_category_list
browser = webdriver.Firefox()

for category in mi_categorys:
    web_url = base_url+ "/category/" + str(category)
    max_page = mi_categorys[category][1]
    for index in range(max_page):
        web_url = base_url+ "/category/" + str(category) + "#page=" + str(index)
        print(web_url)
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = {"User-Agent": user_agent}
        req = urllib.request.Request(web_url, data=None, headers=headers)

        browser.get(web_url)
        web_page = browser.page_source
        soup = BeautifulSoup(web_page, "html.parser")
        applist = soup.select("#all-applist li h5 a")
        print("applist is " + str(len(applist)))
        # browser.quit()
        for i in range(len(applist)):
            app_url = base_url + applist[i]["href"]
            try:
                app_detail = get_app_detail(app_url, "app_detail.txt", category=category)
            except Exception:
                print("spc")
                continue
            app = AppInfo()
            app.set_app_name(app_name=app_detail['name'])
            print(app)
            app_list.append(app)
