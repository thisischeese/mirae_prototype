from streamlit_agraph import agraph, Node, Edge, Config, TripleStore
import networkx as nx
from gensim.models import Word2Vec
import os

def create_graph(model_name,word,n1=5,n2=5):
    model_path = os.path.join('model',model_name)
    model = Word2Vec.load(model_path)
    simWords = model.wv.most_similar(word, topn=n1)

    G=nx.Graph()
    for (w2,wgt) in simWords:
        G.add_edge(word,w2,weight=wgt)

    for (w2,wgt) in simWords:
        simWords2 = model.wv.most_similar(w2, topn=n2)
        #simWords2 = [(w3, wgt) for (w3, wgt) in simWords2 if w3 in (nq_code)]
        for (w3,wgt) in simWords2:
            G.add_edge(w2,w3,weight=wgt)

    return G

# 노드 색상을 지정
def set_color(Graph,nq_code,kor_code):
    nodes_color = []
    for node in Graph.nodes():
        if node in nq_code:
            nodes_color.append('#F58220')
        elif node in kor_code:
            nodes_color.append('#043B72')
        else:
            nodes_color.append('#84888B')

    return nodes_color
