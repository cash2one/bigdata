class AppInfo():
    """
    记录app的相关信息
    """

    def __init__(self, package, app_name, developer, update_time, rate_count, mean_rate):
        """
        初始化时提供 package名称 ，app名称，
        开发者，更新时间，评价数量，打分次数，平均分值
        """
        self.package = package
        self.app_name = app_name
        self.developer = developer
        self.update_time = update_time
        self.rate_count = rate_count
        self.mean_rate = mean_rate

    def __init__(self):
        """
        提供一个空白的appIno构造函数，在后面补充信息
        """

    def set_package_name(self, package):
        self.package = package
        return self

    def set_app_name(self, app_name):
        self.app_name = app_name
        return self

    def set_developer(self, developer):
        self.developer = developer
        return self

    def set_update_time(self, update_time):
        self.update_time = update_time
        return self

    def set_rate_count(self, rate_count):
        self.rate_count = rate_count
        return self

    def set_mean_rate(self, mean_rate):
        self.mean_rate = mean_rate
        return self

    # def parse_from_dict(self, info_dict):
    #     """
    #     从字典中获取信息，并初始化得到一个appinfo实例
    #     :param info_dict:
    #     :return:
    #     """
    #     try:
    #         package = d
