app_category_file = "G:\\datasource\\rawappcategory.txt"

app_first_category_file = "G:\\datasource\\appname.txt"

file_path = "C:\\Users\\befy\\Desktop\\appcategory.txt"

# with open(app_first_category_file,"r") as f:
#     print(f.readline(3))



import pymysql
import pymysql.cursors as cursors

connectConfig = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'db': 'bigdata',
    'charset': 'utf8mb4',
    'cursorclass': cursors.DictCursor
}


def do_select():
    dbConns = pymysql.connect(**connectConfig)
    with dbConns.cursor() as cursor:
        query = "select package, name ,maincategory, secondary from rawappcategory limit 1;"
        temp = cursor.execute(query)
        print(temp)
        app_category = cursor.fetchmany(temp)
        app_categorys = {}
        print(app_category)
        for index in range(len(app_category)):
            print(index)
            print(app_category[index]["package"])
            temp = app_category[index]
            app_categorys[temp["package"]] = [temp["name"], temp["maincategory"], temp["secondary"]]
    print(app_categorys)


# do_select()


def do_insert():
    dbConns = pymysql.connect(**connectConfig)
    with dbConns.cursor() as cursor:
        with open(file_path, encoding="utf-8") as f:
            for line in f:
                print(line)
                sql_line = line.rstrip("\n")
                sql_list = sql_line.split("\t")

                insert_value_str = "\"" + sql_list[0] + "\",\"" + sql_list[1] + "\",\"" + sql_list[2] + "\",\"" + \
                                   sql_list[3] + "\""
                print(insert_value_str)

                sql_isert = "insert into rawappcategory(package, name,maincategory,secondary ) values(" + insert_value_str + ")"

                try:
                    cursor.execute(sql_isert)
                    dbConns.commit()
                except (pymysql.err.DataError, pymysql.err.ProgrammingError) as ex:
                    print("something bad happens ", ex)
                    continue


do_insert()
