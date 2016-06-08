from app_usage.user_usage import UserUsage
from utils import db
import unittest

from tablib import Databook
from tablib import Dataset


config = db.get_default_config()
conns = db.get_db_connections(config=config)
file_dir = "G:\\datasource\\0604\\user"
file_name = "\\vivoY37.txt"
default_database = "app_usage_y37_27"


database_list = ["app_usage_y37_23","app_usage_y37_24","app_usage_y37_25","app_usage_y37_26","app_usage_y37_27","app_usage_y37_28"]


def get_user_list (database, limit = "all"):
    """
    输入机型名称，
    :return:
    """
    imei_list = []
    if limit == "all":
        query = "select distinct imei from "+ database
    elif type(limit) == int:
        query = "select distinct imei from " + database + " limit " +  str(limit)
    else:
        print("the input limit is not avaliable, please check", limit)
        return None

    try:
        with conns.cursor() as cursor:
            temp = cursor.execute(query)
            result = cursor.fetchmany(temp)
            for temp in result:
                imei_list.append(temp["imei"])
    except Exception as ex:
        print("error information,  please check ", ex)
        return None
    if 111111111111111 in imei_list:
        imei_list.remove(111111111111111)
    if 123456789012345 in imei_list:
        imei_list.remove(123456789012345)
    return imei_list


def get_user_usage(database, imei ,limit = "all"):
    """
    获取特定imei码在分日期数据上的使用记录
    :param database: 数据库名称
    :param imei: 用户对应的 imei
    :return: 详细的使用记录
    """
    if limit == "all":
        query = "select package,t_time,duration from " + database + " where imei = " + str(imei)
    elif type(limit) == int:
        query = "select package,t_time,duration from " + database + " where imei = " + str(imei) + " limit "+ str(limit)
    else :
        print("the input limit is not avaliable, please check", limit)
        return None
    usage_detail = []
    try:
        print(query)
        with conns.cursor() as cursor:
            temp = cursor.execute(query)
            result = cursor.fetchmany(temp)
    except Exception as ex :
        print("error info:", ex)
        return None
    return result

# get_user_usage(default_database,867838020061714)

# uu = UserUsage(get_user_usage(default_database, 867838020061714), imei= 867838020061714)
# print(uu.package_set)
# print(len(uu.package_set))
# print(uu.is_dial())
# print(uu.get_total_usage_time())


def get_package_name(package):

    return  None

book = Databook()


for database in database_list:
    package_active= {}

    user_dataset = Dataset()
    package_dateset = Dataset()

    user_headers = ('imei',"总使用时长","总使用应用数")
    package_headers =("package", "应用名称","总使用时长","总使用人数","人均使用时长","日活跃率")

    user_data = []
    package_data = []

    user_list = get_user_list(database)
    total_user = len(user_list)

    for imei in user_list:
        uu = UserUsage(get_user_usage(database,imei),imei=imei )
        for package in uu.get_active_packages():
            try:
                package_active[package]["users"].add(uu.imei)
                package_active[package]["duration_time"] += uu.get_package_use_time(package)
            except KeyError:
                package_active[package] = {
                    "users": {uu.imei},
                    "duration_time":uu.get_package_use_time(package)
                }

        user_data.append((uu.imei,uu.get_total_usage_time(),uu.get_active_package_number()))

    user_dataset = Dataset(*user_data, headers= user_headers, title="test")
    with open(database + "_user.xls","wb") as f:
        f.write(user_dataset.xls)

    for package in package_active:
        name = get_package_name(package)
        use_time = package_active[package]["duration_time"]
        user_num = len(package_active[package]["users"])
        package_data.append((package, name, use_time, user_num, use_time / user_num, user_num / total_user))

    package_dateset = Dataset(*package_data, headers= package_headers, title=database)
    with open(database+ "package.xls","wb") as f:
        f.write(package_dateset.xls)

    print("-----"*10)
    # write to excel


def get_active_app(date, model):
    """
    获取当日活跃app，以及其活跃次数
    :param model: 确定机型名称
    :type date: 确定日期名称
    :return:  返回一个列表，包含一个包名，对应的当日活跃用户数量
    """
    return  ""


class my_test(unittest.TestCase):
    database_name = "app_usage_y37_27"

    def test_user_list(self):
        self.assertIsNotNone(get_user_list(database= self.database_name))


if __name__ == "__main_":
    unittest.main()









