import streamlit as st
import requests,json
from annotated_text import annotated_text

st.set_page_config(
    page_title='COVIDQA',layout='wide',initial_sidebar_state='expanded'
)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)    
def icon(icon_name):
    st.markdown(f'<i class="fa fa-external-link" aria-hidden="true"></i>', unsafe_allow_html=True)

remote_css("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css")

st.markdown('<h1 style="text-align: center">Covid QA</h1>',unsafe_allow_html=True)

top_k_reader = st.sidebar.slider("Max number of answers", min_value=1,max_value=10,value = 3,step =1)
top_k_retriever = st.sidebar.slider('Max number of documents to retrieve',min_value=1, max_value=10,value=3,step=1)

st.markdown('<h3>Question</h3>',unsafe_allow_html=True)
question = st.text_input("Put your query",value="What are the symptoms of Covid?")
button = st.button('Get Answer')

st.text("")
st.text("")

if button:
    headers = {
        'accept':'application/json',
        'Content-Type':'application/json'
    }
    data = {
        'question':question,'num_answers':top_k_reader,'num_docs':top_k_retriever
    }
    response = requests.post("http://localhost:8080/query",headers = headers, data = json.dumps(data))
    result = response.json()
    # print(result)
    for each in result['answer']['answers']:
        title = each['meta']['title']
        url = each['meta']['url'].split(';')[0]
        tokens = []
        tokens.append(each['context'][:each['offset_start']-1])
        tokens.append(
            (each['context'][each['offset_start']:each['offset_end']],'ANS','#faa')
        )
        tokens.append(each['context'][each['offset_end']:])
        col1,col2 = st.beta_columns([5,1])
        col1.markdown(f'<span style="font-size: 16; font-weight:bold;">{title}</span><a href={url} target="_blank"><i class="fa fa-external-link" aria-hidden="true"></i></a>', unsafe_allow_html=True)
        col2.markdown(f'<input type="button" value="Confidence: {int(each["probability"]*100)}%">', unsafe_allow_html=True)
        st.text("")
        col1, col2 = st.beta_columns([2,4])
        col1.markdown(f'<span style="font-size: 16; font-weight:bold;">Publish time: {each["meta"]["publish_time"]}\
                    <br>Authors: {each["meta"]["authors"]}</span>', unsafe_allow_html=True)
        annotated_text(*tokens)