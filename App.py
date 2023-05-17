import streamlit as st
from streamlit_ace import st_ace
from translator import Translator
from checker import checkError
import nltk
import re
st.set_page_config(layout="wide")
st.markdown('## Java To Python Translator')

def trans(sentence):
    t=Translator()
    t.startTranslate(sentence=sentence)
    t.saveFile()
    return t.getTranslatedText()

global filePath
global c1
global contents
global index
index=False
filePath=""
first,second,third=st.columns(3)
with second:
    func=st.button("Translate")
    load=st.button("Load File And Translate")
    uploaded_file = st.file_uploader("Add text file !",type="txt")
    if uploaded_file: 
        filePath=uploaded_file.name
with first:
    st.markdown("Java Code")
    if load:
        with open(filePath, encoding='UTF8') as f:
            contents = f.read()
            index=True
        c2=st_ace(language="java",value=contents,auto_update=True,height=350,font_size=16)
        check=checkError()
        if check.runChecker(c2)=="Clear":
            with third:
                st.markdown("Python Code")
                st_ace(value=trans(c2),language="python",readonly=True,height=350,font_size=16,auto_update=True)
            with second:
                st.success('Translated Done', icon="✅")
                st.text("Saved in output.txt")  
        else:
            with second:
                st.error(check.runChecker(c2), icon="🚨")    
    else:
        c1=st_ace(language="java",auto_update=True,height=350,font_size=16)

if func:
    check=checkError()
    if check.runChecker(c1)=="Clear":
        with third:
            st.markdown("Python Code")
            st_ace(value=trans(c1),language="python",readonly=True,height=350,font_size=16,auto_update=True)
        with second:
                st.success('Translation Done', icon="✅")  
                st.text("Saved in output.txt")  
    else:
        with second:
            st.error(check.runChecker(c1), icon="🚨")  




    


    
  