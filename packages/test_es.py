import qelasticsearch
from elasticsearch import Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
from excel import exporter

es=qelasticsearch.connect(
    host="localhost",
    port=9200
)
print(es)
