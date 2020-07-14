# coding: utf-8
# created by Pengpeng on 2020/7/14
from utils.path_util import from_project_root
from utils import json_util

def keepEntityAndSentences(init_urls, save_url):
    """
    :param init_urls: 原来目标文件路径
    :param save_url: 处理完的文件路径
    :return:
    """
    json_data = {}
    for init_url in init_urls:
        file = open(init_url, 'r', encoding='utf-8')
        for line in file:
            data_units = line.split('\t')
            if data_units[0] not in json_data.keys():
                json_data[data_units[0]] = data_units[2]
    json_util.dump(json_data, save_url)

def triplet2content_fn(triplets_url, entity2contents_url, save_url):
    """
    :param triplets_url:
    :param entity2contents_url:
    :param data_json_url:
    :return:
    """
    entity2content = json_util.load(entity2contents_url)
    triplet_file = open(triplets_url, 'r', encoding="utf-8")
    triplet2centent = {}
    for line in triplet_file:
        triplet = line.strip().split(' ')
        entity1 = triplet[0]
        relation = triplet[1]
        entity2 = triplet[2]
        # print(entity1)
        # print(entity2)
        # print(entity2content[entity1])
        # exit()
        if entity1 in entity2content[entity1] and entity2 in entity2content[entity1]:
            key = entity1+"#"+relation+"#"+entity2
            if key not in triplet2centent.keys():
                triplet2centent[key] = entity2content[entity1]

    json_util.dump(triplet2centent, save_url)


def main():
    """
        生成素材json文件，key: value
        表示的是: key=知识点实体， value=素材文本
    """
    # 只保留原来实体 和 对应的句子
    init_urls = ["名人.txt", "名著.txt", "地名.txt"]
    entity2contents_url = from_project_root("processed_data/entity2contents.json")
    abs_urls = [from_project_root("data/"+url) for url in init_urls]
    keepEntityAndSentences(abs_urls, entity2contents_url)

    """
        三元组对应素材,以头实体为检索点
        检索条件：
            1. 实体对是否均存于素材文本中
    """
    triplets_url = from_project_root("data/triples.txt")
    data_json_url = from_project_root("processed_data/triplet2contents.csv")
    triplet2content_fn(triplets_url, entity2contents_url, data_json_url)


if __name__ == '__main__':
    main()