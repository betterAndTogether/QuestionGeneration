# coding: utf-8
# created by Pengpeng on 2020/7/14

from utils.path_util import from_project_root
from utils import json_util
import numpy as np
import random

def question_generate(sentence, triplet, entity, wrong_answer):
    """
    :param sentence:
    :param triplet:
    :param entity: 考点
    :param wrong_answer:
    :return:
    """
    queAndAnswer = {}
    # entity1
    queAndAnswer['question'] = sentence.replace(entity, "____")
    queAndAnswer['correct'] = entity
    selected_wrong = np.random.choice(wrong_answer, 3, False)
    selected_items = []
    selected_items.extend(selected_wrong)
    selected_items.append(entity)
    queAndAnswer["items"] = selected_items

    return queAndAnswer


def generatorBytriplet(triplet2content, triplet):
    """
    :param triplet2content:
    :param triplet:
    :return: 可以出两道题目
    """
    """
        抽取题干 
    """
    content = triplet2content[triplet]
    triplet_units = triplet.split("#")
    # print(triplet_units)
    sentences = content.split("。")
    selected_sentences = []
    for sentence in sentences:
        if triplet_units[0] in sentence and triplet_units[2] in sentence:
            selected_sentences.append(sentence)
            break

    if len(selected_sentences) == 0:
        print("检索不到素材，请补充[{}]素材".format(triplet))
        return []

    """
        检索备选答案 
    """
    wrong_answer = {'entity1':[], 'entity2':[]}
    triplet_keys = triplet2content.keys()
    for key in triplet_keys:
        key_units = key.split("#")
        if triplet_units[1] in key_units[1]:
            if triplet_units[0] != key_units[0]:
                wrong_answer["entity1"].append(key_units[0])
            if triplet_units[2] != key_units[2]:
                wrong_answer['entity2'].append(key_units[2])

    questions = []
    for sentence in selected_sentences:
        question1 = question_generate(sentence, triplet_units, triplet_units[0], wrong_answer["entity1"])
        question2 = question_generate(sentence, triplet_units, triplet_units[2], wrong_answer["entity2"])

        questions.append(question1)
        questions.append(question2)

    # 随机打乱题目
    questions = random_answers(questions)
    return questions

def random_answers(questions):
    """
    :param questions: json格式
    :return:
    """
    for q in questions:
        tags = ["A", "B", "C", "D"]
        random.shuffle(q["items"])
        index = q['items'].index(q['correct'])
        items = []
        for i,it in enumerate(q["items"]):
            items.append(tags[i]+": "+ it)
        correct = tags[index]
        q["correct"] = correct
        q["items"] = items

    return questions


def generatorByEntity(triplet2content, entity):
    """
    :param triplet2content:
    :param triplet:
    :return: 可以出两道题目
    """
    related_triplet = []
    triplets = triplet2content.keys()
    for triplet in triplets:
        triplet_units = triplet.split("#")
        if entity in triplet_units:
            related_triplet.append(triplet)

    questions = []

    for triplet in related_triplet:
        question = generatorBytriplet(triplet2content, triplet)
        questions.extend(question)

    return questions


def main():

    # 加载数据
    triplet2content_url = from_project_root("processed_data/triplet2contents.csv")
    triplet2content = json_util.load(triplet2content_url)
    # print(triplet2content.keys())
    # exit()
    # triplet = "红楼梦#作者#曹雪芹"
    # # triplet = "水浒传#创作年代#元末明初"
    # questions = generatorBytriplet(triplet2content, triplet)
    # print(questions)

    entity = "红楼梦"
    questions = generatorByEntity(triplet2content, entity)

    print(questions)



if __name__ == '__main__':
    main()