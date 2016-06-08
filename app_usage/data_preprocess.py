file_dir = "G:\\datasource\\0604\\user"

file_name = "\\vivoX6D.txt"

# # with open( file_dir + file_name ,"r", encoding="utf-8") as f:
# #     for line in f:
# #         print(line.rstrip("\n"))
# #         c = line.rstrip("\n").split("\t")
# #
# #         print("c:",c)
#
# with open(file_dir + file_name, "r", encoding="utf-8") as f:
#     for line in f:
#         print(line.rstrip("\n").split("\t"))
#
#
#
#

from utils import db

config = db.get_default_config()
conns = db.get_db_connections(config=config)






def write_to_database():
    """
    将数据保存到数据库中
    c: ['2016-04-07', '00:01:33', '868964028397048', 'com.tencent.mm', '微信', '32221']

    :return:
    """
    db_config = db.get_default_config()
    db_conns = db.get_db_connections(db_config)

    with db_conns.cursor() as cursor:
        model_list = ["Y37", "X6D", "X6PlusD", "Xplay5A"]

        for model in model_list:
            file_name = "\\vivo" + model + ".txt"
            model_index_count = 0

            print(file_name)
            if model == "X6D":
                model = "x6"
            elif model == "X6PlusD":
                model = "x6plus"

            index = [23,24,25,26,27,28]
            suffix = ["_23.txt","_24.txt","_25.txt","_26.txt","_27.txt","_28.txt"]
            for i in index:

                with open(file_dir + file_name+ "_"+str(i)+".txt" , "r", encoding="utf-8") as f:
                    pre_user_info = []
                    for line in f:
                        try:
                            line_split = line.rstrip("\n").split("\t")
                            # print(line_split)
                            date = line_split[0][0:10]
                            time = line_split[0][11:]
                            imei = line_split[1]
                            package = line_split[2]
                            if len(package) > 50:
                                print("package name is too long, pass this record", package)
                                continue
                            duration = line_split[4]
                            if len(line_split) == 8:
                                if pre_user_info == line_split[5:]:
                                    # print("the same user ")
                                    pass
                                else:
                                    gender = line_split[5]
                                    age = line_split[6]
                                    city = line_split[7]
                                    insert_user_info = "insert into user_info(imei, gender,age,city,model) VALUES ('%s','%s','%s','%s','%s')" % (
                                    imei, gender, age, city, model)
                                    cursor.execute(insert_user_info)
                                    db_conns.commit()
                                    pre_user_info = line_split[5:]
                        except IndexError as iderr:
                            print(iderr)
                            continue
                        insert_sql = "insert into app_usage_" + model +"_"+ str(i)+ "(imei, t_time, duration, package) VALUES('%s','%s','%s','%s')" % (
                        imei, time, duration, package)
                        # print(insert_sql)
                        cursor.execute(insert_sql)
                        db_conns.commit()
                        model_index_count += 1;
    db_conns.close()

# 这个函数执行 数据库的写入 默认不执行
write_to_database()


