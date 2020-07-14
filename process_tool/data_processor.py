# coding: utf-8
# created by Pengpeng on 2020/7/14
from utils.path_util import from_project_root
from utils import json_util

def main():

    json_url = from_project_root("processed_data/entity2contents.json")
    json_data = json_util.load(json_url)

    print(json_data["红楼梦"])
    exit()

if __name__ == '__main__':
    main()