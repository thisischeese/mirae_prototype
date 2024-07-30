import streamlit as st
from utils import *
from streamlit_agraph import agraph, Node, Edge, Config, TripleStore
import logging
import os
import pandas as pd

def sidebox_left():
    st.markdown(
        """
        <style>
            [data-testid=stSidebar] [data-testid=stImage]{
                text-align: center;
                display: block;
                margin-left: auto;
                margin-right: auto;
                width: 100%;
            }
        </style>
        """, unsafe_allow_html=True
    )
    with st.sidebar:
        st.image('https://securities.miraeasset.com/newir/publishing/pc/images/common/logo_footer_kr.png',width = 200)
        footer_html = """<div style='text-align: center;'>
          <p>🩷PinkCoconut🥥</p>
        </div>"""
        st.markdown(footer_html, unsafe_allow_html=True)

def initialization():
    st.set_page_config(layout="wide")
    # 단어 입력받기
    word = st.text_input("그래프를 그릴 주식명을 입력하세요")
    st.title(word)
    sidebox_left()
    return word
def draw_graph(word,model):
    # 주식회사명 리스트 생성
    kor_code_df = pd.read_csv('./data/kor_code.csv')
    nq_code_df = pd.read_csv('./data/nasdaq_code.csv')
    kor_code = [item[0] for item in kor_code_df[['종목명']].values.tolist()]
    nq_code = list(set([item[0] for item in nq_code_df[['Symbol_kor']].values.tolist()]) ^ set([item[0] for item in nq_code_df[['Symbol']].values.tolist()]))

    # 그래프 생성
    G = create_graph(model,word)
    # 노드 색깔 지정
    color_list = set_color(G,nq_code,kor_code)
    nodes = []
    i=0
    for item in G.nodes:
        nodes.append(Node(id=item, label=str(item), size=20,color=color_list[i]))
        i+=1

    edges = [Edge(source=i, target=j, type="CURVE_SMOOTH") for (i,j) in G.edges]
    logging.info(f"G.NODES LABEL:{G.nodes}")
    return nodes,edges

def main(word,model):
    nodes,edges = draw_graph(word,model)
    config = Config(width=1000,
                    height=1000,
                    directed=True,
                    nodeHighlightBehavior=True,
                    color='#ECEFF4',
                    collapsible=True,
                    node={'labelProperty':'label'},
                    link={'labelProperty': 'label', 'renderLabel': True}
                    )

    return_value = agraph(nodes=nodes,
                          edges=edges,
                          config=config)


if __name__ == "__main__":
    # 초기 설정
    logging.basicConfig(filename ='history.log', level = logging.INFO, format='%(asctime)s - %(message)s')
    word = initialization()

    # 단어 존재할 경우 그래프 출력
    if word !='':
        logging.info(f"WORD:{word}")
        # 모델 설정
        model = 'word2vec_mj_extendedblog_관련주_한미.model'
        main(word,model)
    else:
        logging.info(f"WRONG INPUT")

