#%%
import json
import pandas as pd


DATA_PATH= "D:\\KnowledgeGraph\\Academic-Knowledge-Graph\\data\\"
#%%


with open(DATA_PATH+"treeData.json",\'r\',encoding=\'utf8\')as fp:
    json_data = json.load(fp)
    # print(\'这是文件中的json数据：\',json_data)
    print(\'这是读取到文件数据的数据类型：\', type(json_data))
    print(\'json_list_length\', len(json_data))
    print("json_list[0]", json_data[0])
    print("json_list[0] type", type(json_data[0]))
    print("json_list[0] key", json_data[0].keys())
    print("json_data[i][\'connections\'])[0] len:", len(json_data[0][\'connections\']) )

df = pd.DataFrame(columns=[\'e_1\', \'e_2\', \'r\'])
print(df)
for i in range(len(json_data)):
    e1 = json_data[i][\'name\']
    for j in range(len(json_data[i][\'connections\'])):
        e2=json_data[i][\'connections\'][j][\'name\']
        r=json_data[i][\'connections\'][j][\'relationship\']
        # df.append([e1, e2, r]
        df.loc[len(df)] = [e1, e2, r]
        # print(e1, e2, r)

# print(df)
df.to_csv(DATA_PATH+"AKG.csv", header=True, index=False)
