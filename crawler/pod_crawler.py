base_url = "http://www.wandoujia.com/category/app"

from bs4 import BeautifulSoup

import urllib.request


with urllib.request.urlopen(base_url) as response:
    category_list = response.read()

    soup = BeautifulSoup(category_list, "html.parser")
    # print(soup.prettify())
    parent_cate = soup.select("li.parent-cate .cate-link")

    print(parent_cate)
    print(type(parent_cate))
    print(len(parent_cate))

    t1 = parent_cate[1]
    for i in range(len(parent_cate)):
        child_cate = soup.select("li.child-cate a")
        for id in range(len(child_cate)):
            child1 = child_cate[id]
            print(child_cate[id].string)
            child_url = child1["href"]
            child_title = child1["title"]
            ## 一个tag的姿态个

        print(parent_cate[i].string)



print("dadaj")