import unittest as ut


class ActivePeriod:
    """
    用来记录用户使用数据的活跃时段, 支持按照不同的时间来划分
    """

    def __init__(self):
        print("create active period")


class UserUsage:
    """
    使用user_usage来描述用户的使用行为，并给出一些统计数据
    记录数目，活跃时段，最长使用时间，总使用时间，单日使用软件数量以及相应的时间分布
    """

    def is_dial(self):
        return ("com.android.incallui" in self.package_set)

    def get_active_package_number(self):
        return len(self.package_set)

    def get_top_packages(self, top=5):
        """
        返回使用次数最高的package
        :param top:
        :return:
        """
        self.package_set
        return ("to be continued")

    def get_active_packages(self):
        """
        :return:
        """
        return set(self.package_set)

    def get_total_usage_time(self, style="default"):
        total = sum(self.duration_dist)
        seconds = int(total / 1000)
        minutes = int(seconds / 60)
        minute = minutes % 60
        second = seconds % 60
        hour = int(minutes / 60)
        print(total)
        print(seconds, minutes)
        return  "{}:{}:{}".format(hour,minute,second)
        # return (hour, minute, second)

    def get_package_use_time(self, package):
        """
        返回特定的package使用时间
        :param package:
        :return:
        """
        if package not in self.package_set:
            print(package, " is not used by", self.imei)
            return None
        return self.package_info[package]["duration_time"]

    def get_package_click_num(self, package):
        if package not in self.package_set:
            print(package, " is not used by", self.imei)
            return None
        return self.package_info[package]["click"]

    def __init__(self, record_list, imei=None, date=None):
        """
        初始化，获取使用记录，简单统计这些使用记录，以供后期存储。
        [{'package': 'com.bbk.launcher2', 'duration': 15138, 't_time': datetime.timedelta(0, 19815)}, ..., ]
        传入的使用记录如上所示
        :type date: object
        :type imei: object
        :param record_list:
        """
        self.record_list = record_list
        self.imei = imei
        self.date = date
        self.record_num = len(record_list)
        self.duration_dist = []
        self.package_info = {}

        self.package_list = []
        for record in record_list:
            # print(record)
            package_name = record["package"]
            duration_time = record["duration"]
            self.duration_dist.append(duration_time)
            try:
                self.package_info[package_name]["click"] += 1
                self.package_info[package_name]["duration_time"] += duration_time
            except KeyError:
                self.package_info[package_name] = {"click": 1}
                self.package_info[package_name] = {"duration_time": duration_time}
        #     pack = Package(package_name)
        # pack.set_duration_distribution()
        # self.package_list.append()
        self.package_set = set(self.package_info.keys())
        self.max_duration = max(self.duration_dist)

    def __str__(self):
        return "imei " + str(self.imei) + " maxduration " + str(self.max_duration) + str(self.package_set)


class Package:
    """
    记录package的使用习惯
    包名，应用名，点击次数，总使用时长，使用时长分布，使用时间列表

    """

    def __init__(self, package=None):
        self.package = package
        self.name = self.__get_name()
        self.click_num = 0
        self.use_time_dist = None
        self.duration_dist = None
        self.total_use_time = 0

    def set_name(self, package_name):
        self.name = package_name

    def set_use_time_distribution(self, distribution):
        self.use_time_dist = distribution
        self.click_num = len(distribution)

    #     self.max_time = max(distribution)
    #     self.min_time = min(distribution)
    #
    #
    # def __parse_time_dist(self):

    def set_duration_distribution(self, distribution):
        self.duration_dist = distribution
        self.total_use_time = sum(self.duration_dist)
        self.click_num = len(distribution)


class MyTest(ut.TestCase):
    @staticmethod
    def test_create():
        list1 = range(10)
        print(list1)
        uu1 = UserUsage(list1)
        print(uu1.record_list)
        print(uu1)


if __name__ == "__main__":
    ut.main()
