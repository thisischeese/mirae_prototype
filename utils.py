from streamlit_agraph import agraph, Node, Edge, Config, TripleStore
import networkx as nx
from gensim.models import Word2Vec
import os
import pandas as pd

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

def get_ticker(word,nq_code_name,kor_code_name):
    kor_code, nq_code = get_codelist(word,nq_code_name,kor_code_name)
    if word in nq_code:
        nq_df = pd.read_csv(nq_code_name)
        return "NASDAQ "+nq_df.loc[nq_df['Symbol_kor']==word,'Symbol'].iloc[0]
    elif word in kor_code:
        kr_df = pd.read_csv(kor_code_name)
        return 'KRX '+kr_df.loc[kr_df['종목명']==word,'종목코드'].iloc[0]
    else:
        return None

def get_codelist(word,nq_code_name,kor_code_name):
    # 주식회사명 리스트 생성
    kor_code_df = pd.read_csv(kor_code_name)
    nq_code_df = pd.read_csv(nq_code_name)
    kor_code = [item[0] for item in kor_code_df[['종목명']].values.tolist()]
    nq_code = list(set([item[0] for item in nq_code_df[['Symbol_kor']].values.tolist()]) ^ set([item[0] for item in nq_code_df[['Symbol']].values.tolist()]))
    return kor_code, nq_code