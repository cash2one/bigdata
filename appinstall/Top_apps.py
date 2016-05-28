import pymysql
import pymysql.cursors as cursors

from tablib import Databook
from tablib import Dataset

phone_model = ["Y37", "X6D", "X6PlusD", "Xplay5A"]
phone_model_user_number = {
    "Y37": 100000,
    "X6D": 100000,
    "X6PlusD": 98243,
    "Xplay5A": 75305
}

package_name_path = "G:\\datasource\\appname.txt"

user_packages = {}
package_users = {}
package_category = {}
package_ranks = {}

package_name = {}  ## 保留最全面的应用报名

pre_stall_list = [
    'com.bbk.appstore', 'com.vivo.browser', 'com.vivo.game', 'com.chaozh.iReader', 'com.android.browser',
    'com.vivo.space',
    'com.google.android.syncadapters.calendar', 'com.vivo.easyshare',
    'com.vlife.vivo.wallpaper', 'com.android.bbk.lockscreen3', 'com.bbk.iqoo.feedback', "com.vivo.abe"]

pre_stall_y37_always = ['com.tencent.mm', 'com.tencent.mobileqq', 'com.qiyi.video', 'com.autonavi.minimap',
                        'com.baidu.searchbox', 'com.netease.newsreader.activity', 'com.sankuai.meituan',
                        'com.achievo.vipshop',
                        'com.netease.cloudmusic'
                        ]

pre_stall_y37_once = pre_stall_list + pre_stall_y37_always + ['com.tencent.qqlive', 'ctrip.android.view']
pre_stall_x6d_always = ['com.tencent.mm', 'com.tencent.mobileqq', 'com.sina.weibo', 'com.qiyi.video',
                        'com.autonavi.minimap',
                        'com.baidu.searchbox', 'com.sankuai.meituan', 'com.achievo.vipshop'
                        ]

pre_stall_x6d_once = pre_stall_list + pre_stall_x6d_always + ['com.tencent.qqlive', 'ctrip.android.view',
                                                              'com.tencent.news']
pre_stall_x6plusd_always = ['com.tencent.mm', 'com.tencent.mobileqq', 'com.qiyi.video', 'com.autonavi.minimap',
                            'com.baidu.searchbox', 'com.sankuai.meituan', 'com.achievo.vipshop', 'com.dianping.v1'
                            ]

pre_stall_x6plus_once = pre_stall_list + pre_stall_x6plusd_always + ['com.tencent.qqlive', 'ctrip.android.view',
                                                                     'com.tencent.news']
pre_stall_list_xplay5_always = ['com.tencent.mm', 'com.tencent.mobileqq', 'com.sina.weibo', 'com.qiyi.video',
                                'com.autonavi.minimap',
                                'com.baidu.searchbox', 'com.tencent.news', 'com.sankuai.meituan', 'com.achievo.vipshop',
                                'com.dianping.v1', 'ctrip.android.view'
                                ]

pre_stall_xplay5_once = pre_stall_list + pre_stall_list_xplay5_always + ['com.tencent.qqlive']
# pre_stall_list_Y37 = list(pre_stall_list)

# pre_stall_list_Y37.remove("com.tencent.news")
# pre_stall_list_Y37.remove("com.ifeng.news2")
# pre_stall_list_Y37.remove("com.eg.android.AlipayGphone")
#
# pre_stall_list_Xplay5A = list(pre_stall_list)
# pre_stall_list_X6D = list(pre_stall_list)
# pre_stall_list_X6PlusD = list(pre_stall_list)
# pre_stall_list_Xplay5A.remove("com.ss.android.article.news")
# pre_stall_list_X6D.remove("com.ss.android.article.news")
# pre_stall_list_X6PlusD.remove("com.ss.android.article.news")


pre_stall_list = {
    "Y37": {
        "once": pre_stall_y37_once,
        "always": pre_stall_y37_always
    },
    "X6D": {
        "once": pre_stall_x6d_once,
        "always": pre_stall_x6d_always
    },
    "X6PlusD": {
        "once": pre_stall_x6plus_once,
        "always": pre_stall_x6plusd_always
    },
    "Xplay5A": {
        "once": pre_stall_xplay5_once,
        "always": pre_stall_list_xplay5_always
    }
}

connectConfig = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'db': 'bigdata',
    'charset': 'utf8mb4',
    'cursorclass': cursors.DictCursor
}


def load_package_name(file_path):
    """

    :return:
    """
    package_name = {}
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            templine = line.rstrip("\n")
            tem = templine.split("\t")
            package_name[tem[0]] = tem[1]
            print(line)
    return package_name


package_name = load_package_name(package_name_path)


def load_app_category():
    """
    从数据库中加载category, 并整理成
    package:[app_name,main_category, secondary]
    :return:
    """
    dbConns = pymysql.connect(**connectConfig)
    with dbConns.cursor() as cursor:
        query = "select package, name ,maincategory, secondary from rawappcategory;"
        temp = cursor.execute(query)
        print(temp)
        raw_categorys = cursor.fetchmany(temp)
        categorys = {}
        for index in range(len(raw_categorys)):
            temp_line = raw_categorys[index]
            categorys[temp_line["package"]] = [temp_line["name"], temp_line["maincategory"], temp_line["secondary"]]
    return categorys


package_category = load_app_category()


def get_cagetory(package, level=1):
    """
    返回package对应的应用类别，默认返回一级类别
    :param level:
    :return:
    """
    try:
        if level == 1:
            return package_category[package][1]
        elif level == 2:
            return package_category[package][2]
        else:
            print("the level request is not exist, please check the input value")
            return "无"
    except KeyError as ex:
        print("key errors", "the input package is", package)
        return "error"


def get_package_name(package):
    """
    输入包名，返回应用名称
    :param package:
    :return:
    """
    try:
        name = package_category[package][0]
        return name
    except KeyError as ex:
        print("key errors", "the input package is", package)
        try:
            return package_name[package]
        except KeyError:
            print("key errors  in the package_name map ", package)
            return "error"
        return "error"


def get_top_apps(pac_rank, top_n, start=0, with_pre_stall=True):
    """
    返回当前所有的app
    :param package_users:
    :param top_n:
    :return:
    """
    if top_n <= 0:
        print("the input top_n", top_n, "is less than 0")
        return None
    if with_pre_stall == True:
        return pac_rank[start:top_n]


def get_package_rank(package_users):
    """
    这个输入是单个机型的package user对应数据
    输入package_users，解析得到应用对应的详细情况，如在应用的名称，安装数量，排名，和分类情况
    :param package_users:
    :return:
    """
    package_install_num = []
    for package in package_users:
        user_num = package_users[package]["user_num"]
        package_install_num.append((package, int(user_num)))

    package_rank = sorted(package_install_num, key=lambda tuple: tuple[1], reverse=True)
    return package_rank


def is_prestall(package, model):
    """
    输入包名，判断是否为预装应用
    :param package:
    :return:
    """
    if package in pre_stall_list[model]["always"]:
        return "always"
    elif package in pre_stall_list[model]["once"]:
        return "once"
    else:
        return "FALSE"


def get_package_details(package_name, model):
    """
    输入一个package，解析得到应用对应的详细情况，如在应用的名称，安装数量，排名，和分类情况
    :param package_users:
    :return:
    """
    package_detail = {
        "package": package_name,
        "name": get_package_name(package_name),
        "numbers": package_users[model][package_name]["user_num"],
        "first_category": get_cagetory(package_name),
        "second_category": get_cagetory(package_name, level=2),
        "is_prestall": is_prestall(package_name, model)
    }
    print(package_detail)
    return package_detail


def load_data():
    """
    :return:
    """
    for model in phone_model:
        temp_user_packages = {}
        temp_package_users = {}
        with open(model + "_user_packages.txt", "r") as f:
            for line in f:
                user_packages_line = line.split(",")
                temp_user_packages[user_packages_line[0]] = {
                    "package_num": user_packages_line[1],
                    "packages": user_packages_line[2:]
                }
            user_packages[model] = temp_user_packages
        with open(model + "_package_users.txt", "r") as f:
            for line in f:
                package_users_line = line.split(",")
                temp_package_users[package_users_line[0]] = {
                    "user_num": package_users_line[1],
                    "user_list": package_users_line[2:]
                }
            package_users[model] = temp_package_users


load_data()

work_book = Databook()
TOP_N = 151
for model in package_users:
    headers = ("应用包名", "应用名称", "应用安装数量", "一级分类", "二级分类", "是否预装", "安装比率")
    data = []
    package_ranks[model] = get_package_rank(package_users[model])
    print("model is ", model)
    top_apps = get_top_apps(package_ranks[model], TOP_N, start=0)
    print(top_apps)
    for index in range(len(top_apps)):
        print()
        package_detail = get_package_details(top_apps[index][0], model)
        data.append((package_detail["package"], package_detail["name"], package_detail["numbers"],
                     package_detail["first_category"],
                     package_detail["second_category"], package_detail["is_prestall"],
                     int(package_detail["numbers"]) / phone_model_user_number[model]))
    dataset = Dataset(*data, headers=headers, title=model)
    work_book.add_sheet(dataset)
    with open(str(TOP_N) + ".xlsx", "wb") as f:
        f.write(work_book.xlsx)
