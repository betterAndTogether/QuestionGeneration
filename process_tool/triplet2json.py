# coding: utf-8
# created by Pengpeng on 2020/7/16
from utils import json_util
from utils.path_util import from_project_root

def transfer2json(triplet2content_file):


    triplet2content = json_util.load(triplet2content_file)

    """
        构造nodes.json
    """
    names = []
    nodes = []
    links = []
    for triplet in triplet2content.keys():
        units = triplet.split("#")
        if units[0] not in names:
            names.append(units[0])
        if units[1] not in names:
            names.append(units[2])
    for name in names:
        node = {}
        node['category'] = 0
        node['name'] = name
        nodes.append(node)
    """
        构造links  
    """
    # 保证tripelt唯一性
    triplets = []
    for triplet in triplet2content.keys():
        if triplet not in triplets:
            triplets.append(triplet)
    for triplet in triplets:
        units = triplet.split("#")
        link = {}
        link["source"] = units[0]
        link["target"] = units[2]
        link["name"] = units[1]
        links.append(link)

    # save file
    json_util.dump(nodes, from_project_root("data/analogyKG_nodes.json"))
    json_util.dump(links, from_project_root("data/analogyKG_links.json"))





def main():

    triplet2content_file = from_project_root("processed_data/triplet2contents.csv")
    transfer2json(triplet2content_file)
    pass


if __name__ == '__main__':
    main()