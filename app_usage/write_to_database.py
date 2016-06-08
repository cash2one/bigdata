
from utils import db

config = db.get_default_config()
conns = db.get_db_connections(config=config)
file_dir = "G:\\datasource\\0604\\user"

file_name = "\\vivoY37.txt"

def write_file_datebase(file_name, database, model, batch = 1000):
    """
    从配置的文件中读取数据，写入到指定的database中
    :param file_name:
    :param database:
    :return:
    """
    print(file_name, database)
    db_conf = db.get_default_config()
    db_conns = db.get_db_connections(db_conf)
    error_count = 0
    with db_conns.cursor() as cursor:
        record_list = []

        with open(file_name, "r", encoding="utf-8") as f:
            for line in f:

                line_split = line.rstrip("\n").split("\t")
                # print(line_split)
                time = line_split[0][11:]
                imei = line_split[1]
                package = line_split[2]
                if len(package) > 100 or len(package)< 2:
                    # print("package name is too long or to short , pass this record", package)
                    error_count += 1
                    continue

                duration = line_split[4]
                if len(duration) < 2:
                    error_count += 1
                    continue

                record_list.append((imei, time, package, duration))
                if len(record_list) > batch:
                    record_list_str = str(record_list)
                    insert_sql = "insert into " + database + "(imei, t_time,package,duration) values " + \
                                 record_list_str[1:len(record_list_str) - 1]
                    # print(insert_sql)
                    record_list.clear()
                    cursor.execute(insert_sql)
                    db_conns.commit()

        # 将没能凑够一次batch的数据输入到数据库中
        record_list_str = str(record_list)
        insert_sql = "insert into " + database + "(imei, t_time,package,duration) values " + \
                     record_list_str[1:len(record_list_str) - 1]
        record_list.clear()
        cursor.execute(insert_sql)
        db_conns.commit()

    print(error_count)

trail_file_name = file_dir + file_name + "_27.txt"
write_file_datebase(trail_file_name, "app_usage_y37_27", "y37")
