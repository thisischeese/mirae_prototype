import streamlit as st
from utils import *
from streamlit_agraph import agraph, Node, Edge, Config, TripleStore
import logging
from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px

def layout(*args):
    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
      .stApp { padding-bottom: 60px; } /* Adjust padding to accommodate footer */
      .footer-container {
          position: fixed;
          left: 0;
          bottom: 0;
          width: auto;
          color: black;
          text-align: center;
          background-color: transparent; /* Make background transparent */
          padding: 10px;
          transform: translateX(9%);
      }
    </style>
    """

    style_div = styles(
        margin=px(0),
        width=percent(100),
        height="auto",
        opacity=1
    )

    body = p()
    foot = div(
        style=style_div,
        _class="footer-container"
    )(
        body
    )

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)
        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)

def footer_design():
    myargs = [

        "© Daeun"
    ]
    layout(*myargs)
def design():

    with st.sidebar:

        #st.image('https://securities.miraeasset.com/newir/publishing/pc/images/common/logo_footer_kr.png', width=200)
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
        footer_design()
        #st.markdown("### Graph Node Color Legend")
        st.markdown("<div style='background-color:#F58220; padding:5px; color:white;'>NASDAQ</div>", unsafe_allow_html=True)
        st.markdown("<div style='background-color:#043B72; padding:5px; color:white;'>KRX</div>", unsafe_allow_html=True)
        st.markdown("<div style='background-color:#84888B; padding:5px; color:white;'>Others</div>", unsafe_allow_html=True)







def initialization():
    st.set_page_config(layout="wide")
    # 단어 입력받기
    word = st.text_input("그래프를 그릴 주식명을 입력하세요")
    ticker = get_ticker(word,'data/nasdaq_code.csv','data/kor_code.csv')
    if ticker is not None:
        st.header(word + ': ' + ticker)
    else:
        st.header(word)
    design()
    return word
def draw_graph(word,model):
    # 주식회사명 리스트 생성
    kor_code, nq_code = get_codelist('data/nasdaq_code.csv','data/kor_code.csv')
    # 그래프 생성
    G = create_graph(model,word)
    # 노드 색깔 지정
    color_list = set_color(G,nq_code,kor_code)
    nodes = []
    edges = []
    i=0

    for item in G.nodes:
        nodes.append(Node(id=item, label=str(item), size=20,color=color_list[i]))
        i+=1

    for i,j in G.edges:
        if i == word:
            edges.append(Edge(source=i, target=j, type="CURVE_SMOOTH",color = '#8DC8E8',width=2))
        else:
            edges.append(Edge(source=i, target=j, type="CURVE_SMOOTH",color = '#A0A6A8'))

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

    return_value = agraph(nodes=nodes,edges=edges,config=config)

    original_ticker = get_ticker(word,'data/nasdaq_code.csv','data/kor_code.csv')
    original_fig = fetch_candlestick_chart(word,original_ticker)
    logging.info(f"original word : {word},original_ticker : {original_ticker}")
    st.sidebar.plotly_chart(original_fig)

    kor_code, nq_code = get_codelist('data/nasdaq_code.csv','data/kor_code.csv')
    if return_value in kor_code or return_value in nq_code:
        ticker = get_ticker(return_value, 'data/nasdaq_code.csv', 'data/kor_code.csv')
        if ticker:
            logging.info(f"selected_word, selected_ticker:{ticker}")
            selected_fig = fetch_candlestick_chart(return_value,ticker)
            st.sidebar.plotly_chart(selected_fig)
        else:
            logging.info(f"CAN NOT FIND TICKER")
    else:
        logging.info(f"NO RETURN VALUE EXISTS OR RETURN VALUE NOT IN CODE")


if __name__ == "__main__":
    # 초기 설정
    logging.basicConfig(filename ='history.log', level = logging.INFO, format='%(asctime)s - %(message)s')
    word = initialization()

    # 단어 존재할 경우 그래프 출력
    if word !='':
        logging.info(f"WORD:{word}")
        # 모델 설정
        model = 'word2vec_sg.model'
        logging.info(f"MODEL:{model}")
        main(word,model)
    else:
        logging.info(f"WRONG INPUT")

