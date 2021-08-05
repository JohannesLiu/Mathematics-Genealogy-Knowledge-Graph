from py2neo import Graph
graph = Graph(
    "http://192.168.2.130:7475",
    # database="mathematics-genealogy-knwoledge-graph",
    username="neo4j",
    password="Kddir@123456&"
)
CA_LIST = {"Paper":0,"Person":1,"University":2,"Country":3}
similar_words = {
    "作者":"Authorof",
    "作品":"Workof",
    "单位":"Starfof",
    "位于":"locate_in"
}
