
file_dir = "G:\\datasource\\0604\\user"

file_name = "\\vivoY37.txt"

from utils import db
def write_to_database():
    """
    将数据保存到数据库中
    c: ['2016-04-07', '00:01:33', '868964028397048', 'com.tencent.mm', '微信', '32221']

    :return:
    """
    db_config = db.get_default_config()
    db_conns = db.get_db_connections(db_config)

    with db_conns.cursor() as cursor:
        model_list = ["Y37"]

        for model in model_list:
            file_name = "\\vivo" + model + ".txt"
            model_index_count = 0

            print(file_name)
            if model == "X6D":
                model = "x6"
            elif model == "X6PlusD":
                model = "x6plus"
            with open(file_dir + file_name, "r", encoding="utf-8") as f:
                file_23 = open(file_dir + file_name + "_23.txt", "w", encoding="utf-8")
                file_24 = open(file_dir + file_name + "_24.txt", "w", encoding="utf-8")
                file_25 = open(file_dir + file_name + "_25.txt", "w", encoding="utf-8")
                file_26 = open(file_dir + file_name + "_26.txt", "w", encoding="utf-8")
                file_27 = open(file_dir + file_name + "_27.txt", "w", encoding="utf-8")
                file_28 = open(file_dir + file_name + "_28.txt", "w", encoding="utf-8")

                pre_user_info = []

                for line in f:
                    line_split = line.rstrip("\n").split("\t")
                    # print(line_split)
                    date = line_split[0][0:10]

                    if date == "2016-05-23":
                        file_23.writelines(line)
                    elif date == "2016-05-24":
                        file_24.writelines(line)
                    elif date == "2016-05-25":
                        file_25.writelines(line)
                    elif date == "2016-05-26":
                        file_26.writelines(line)
                    elif date == "2016-05-27":
                        file_27.writelines(line)
                    elif date == "2016-05-28":
                        file_28.writelines(line)
    db_conns.close()


write_to_database()
