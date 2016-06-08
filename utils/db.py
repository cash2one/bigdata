import pymysql
import pymysql.cursors as cursors
import unittest
import copy

connectConfig = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'db': 'bigdata',
    'charset': 'utf8mb4',
    'cursorclass': cursors.DictCursor
}


def get_db_connections(config=connectConfig):
    """
    创建一个新的数据库连接，并返回
    :type config:默认使用给定的配置，也可以输入特别的配置
    :return:
    """
    return pymysql.connect(**config)


def get_default_config():
    """
    获取db模块的默认数据库配置文件，可以方便获取后修改.
    返回的是配置本身的引用，还是这个配置复制类？

    使用copy模块的浅拷贝函数copy就可以解决默认配置文件被修改的问题。
    Python 的对象之间的赋值是按引用出传递的
    :return:
    """
    return copy.copy(connectConfig)


class DbTestCase(unittest.TestCase):
    def setUp(self):
        print("setUp")

    def tearDown(self):
        print("tearDown")

    def test_defalut_connect(self):
        pass

    def test_defalut_config(self):
        default_config = get_default_config()
        self.assertEqual(default_config, connectConfig, '判断与当前连接是否相同')


if __name__ == "main":
    unittest.main()
