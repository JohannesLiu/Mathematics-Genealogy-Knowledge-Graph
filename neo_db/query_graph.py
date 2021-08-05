from neo_db.config import graph, CA_LIST, similar_words
from spider.show_profile import get_profile
import codecs
import os
import json
import base64

def query(name):
    data = graph.run(
        "match (pp:Paper)-[r1]->(ppl:Person)-[r2]->(u:University)-[r3]->(c:Country)  where ppl.name=~'(?i)%s'  \
        return  pp.paper_title, r1.relation, ppl.name,\
          r2.relation, u.name, r3.relation, c.name, labels(pp), labels(ppl), labels(u), labels(c) " % (name)
    )
    data = list(data)
    flatten_data=list()
    for i in range(len(data)):
        flatten_data.append({"p.Name":data[i][0], "r.relation":data[i][1], 'n.Name':data[i][2], 'labels(p)':data[i][7][0], 'labels(n)':data[i][8][0]})
        flatten_data.append({"p.Name":data[i][2], "r.relation":data[i][3], 'n.Name':data[i][4], 'labels(p)':data[i][8][0], 'labels(n)':data[i][9][0]})
        flatten_data.append({"p.Name":data[i][4], "r.relation":data[i][5], 'n.Name':data[i][6], 'labels(p)':data[i][9][0], 'labels(n)':data[i][10][0]})
    return get_json_data(flatten_data)

def query_random():
    data = graph.run(
    "        match (pp:Paper)-[r1]->(ppl:Person)-[r2]->(u:University)-[r3]->(c:Country) return  pp.paper_title, r1.relation, ppl.name,\
          r2.relation, u.name, r3.relation, c.name, labels(pp), labels(ppl), labels(u), labels(c)  limit 100 "
    )
    data = list(data)
    flatten_data=list()
    for i in range(len(data)):
        flatten_data.append({"p.Name":data[i][0], "r.relation":data[i][1], 'n.Name':data[i][2], 'labels(p)':data[i][7][0], 'labels(n)':data[i][8][0]})
        flatten_data.append({"p.Name":data[i][2], "r.relation":data[i][3], 'n.Name':data[i][4], 'labels(p)':data[i][8][0], 'labels(n)':data[i][9][0]})
        flatten_data.append({"p.Name":data[i][4], "r.relation":data[i][5], 'n.Name':data[i][6], 'labels(p)':data[i][9][0], 'labels(n)':data[i][10][0]})
    return get_json_data(flatten_data)

def get_json_data(data):
    json_data = {'data': [], "links": []}
    d = []

    for i in data:
        # print(i["p.Name"], i["r.relation"], i["n.Name"], i["p.cate"], i["n.cate"])
        d.append(i['p.Name'] + "@@@" + i['labels(p)'])
        d.append(i['n.Name'] + "@@@" + i['labels(n)'])
        d = list(set(d))
    name_dict = {}
    count = 0
    for j in d:
        j_array = j.split("@@@")

        data_item = {}
        name_dict[j_array[0]] = count
        count += 1
        data_item['name'] = j_array[0]
        data_item['category'] = CA_LIST[j_array[1]]
        json_data['data'].append(data_item)

    for i in data:
        link_item = {}

        link_item['source'] = name_dict[i['p.Name']]

        link_item['target'] = name_dict[i['n.Name']]
        link_item['value'] = i['r.relation']
        json_data['links'].append(link_item)
    return json_data


# f = codecs.open('./static/test_data.json','w','utf-8')
# f.write(json.dumps(json_data,  ensure_ascii=False))
def get_KGQA_answer(array):
    data_array = []
    for i in range(len(array) - 2):
        if i == 0:
            name = array[0]
        else:
            name = data_array[-1]['p.name']

        data = graph.run(
            "match(p)-[r:%s{relation: '%s'}]->(n:Person{name:'%s'}) return  p.name,n.name,r.relation,p.cate,n.cate" % (
                similar_words[array[i + 1]], similar_words[array[i + 1]], name)
        )

        data = list(data)
        print(data)
        data_array.extend(data)

        print("===" * 36)
    with open("./spider/images/" + "%s.jpg" % (str(data_array[-1]['p.name'])), "rb") as image:
        base64_data = base64.b64encode(image.read())
        b = str(base64_data)

    return [get_json_data(data_array), get_profile(str(data_array[-1]['p.name'])), b.split("'")[1]]


def get_answer_profile(name):
    with open("./spider/images/" + "%s.jpg" % (str(name)), "rb") as image:
        base64_data = base64.b64encode(image.read())
        b = str(base64_data)
    return [get_profile(str(name)), b.split("'")[1]]




