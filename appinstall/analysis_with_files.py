input_dir_path = "/Volumes/data/datasource/0518/ins/"
output_dir_path = "/Volumes/data/datasource/0518/out/"

import os
def get_user_packages():
    """
    整理原始文本格式,整理后格式为:
    每行格式为:
    user,appinstallNum,packages_detail
    :return:
    """
    input_file_list = os.listdir(input_dir_path)
    for file_name in input_file_list:
        if file_name[0] == ".":
            continue
        with open(input_dir_path + file_name, "r") as f:
            line_count = 0
            name ,ext = os.path.splitext(file_name)
            refined_file = open(output_dir_path + name + "_user_packages.txt", "w")  # 整理后写入的文件
            user_packages = {}
            for line in f:
                line_count += 1
                user, package = line.rstrip("\n").split("\t")
                try:
                    user_packages[user].append(package)
                except KeyError:
                    user_packages[user] = [package]
            for key in user_packages:
                line_list = [str(key), str(len(user_packages[key]))]
                line_list.extend(user_packages[key])
                write_line = ",".join(line_list)
                refined_file.write(write_line + "\n")
            refined_file.close()


def get_package_users():
    input_file_list = os.listdir(input_dir_path)

    for file_name in input_file_list:
        if file_name[0] == ".":
            continue
        with open(input_dir_path + file_name, "r") as f:
            name,ext = os.path.splitext(file_name)
            refined_file = open(output_dir_path + name + "_package_users.txt", "w")  # 保存一个应用对应着多少个用户

            package_users = {}
            for line in f:
                user, package = line.rstrip("\n").split("\t")
                try:
                    package_users[package].append(user)
                except KeyError:
                    package_users[package] = [user]

            for package in package_users:
                line_list = [package,str(len(package_users[package]))]
                line_list.extend(package_users[package])
                write_line = ",".join(line_list)
                refined_file.write(write_line+ "\n")
            refined_file.close()


X6D_package_users = {}
Y37_package_users = {}
X6PlusD_package_users = {}
Xplay5A_package_users = {}

Y37_user_packages = {}
X6D_user_packages = {}
X6PlusD_user_packages = {}
Xplay5A_user_packages = {}


def load_data():
    """
    从文本文件中加载所需要的数据
    :return:
    """
    with open(output_dir_path + "Y37_package_users.txt", "r") as f:
        Y37_package_users = f.readlines()

    with open(output_dir_path + "X6D_package_users.txt", "r") as f:
        X6D_package_users = f.readlines()

    with open(output_dir_path + "X6PlusD_package_users.txt", "r") as f:
        X6PlusD_package_users = f.readlines()
    with open(output_dir_path + "Xplay5A_package_users.txt", "r") as f:
        Xplay5A_package_users = f.readlines()

    with open(output_dir_path + "Y37_user_packages.txt", "r") as f:
        Y37_user_packages = f.readlines()

    with open(output_dir_path + "X6D_user_packages.txt", "r") as f:
        X6D_user_packages = f.readlines()

    with open(output_dir_path + "X6PlusD_user_packages.txt", "r") as f:
        X6PlusD_user_packages = f.readlines()
    with open(output_dir_path + "Xplay5A_user_packages.txt", "r") as f:
        Xplay5A_user_packages = f.readlines()


load_data()


def parse_command(input_command ="help"):
    """
    解析输入的结果
    :param input_command:
    :return: 如果命令解析成功 则返回success，否则返回命令解析失败和对应的error_code
    """
    help_str = """
    1. 独立用户数量 需再次输入机型名称；
    2. 特定应用在 各个机型上的安装数量和比例；
    3. 一串包名 在各个机型上的独立用户数量和比例
    4. 查看内置特定类别应用
    exit: 退出
    """
    if input_command == "help":
        return help_str
    elif input_command == '1':
        return ""





while True:
    command = input('请输入要执行的命令，输入help查看帮助，退出请输入exit;')
    command_striped = command.rstrip().strip("\"")
    if command_striped == "exit":
        print("程序退出")
        break
    parse_result = parse_command(command_striped)
    print(parse_result)
