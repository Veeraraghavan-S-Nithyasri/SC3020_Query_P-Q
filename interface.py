
'''Streamlit interface test demo'''

import streamlit as st

class dbGUI:
    def __init__(self):
        st.title('SC3020 Project 2')
        st.markdown('''
                    This interface is designed for visualisation of SQL query execution & exploration.
                    ''')
        self.queryInput()
        


    # SQL query input section
    def queryInput(self):
        st.header('Query Input')
        self.inputBox = st.text_area("Key in your SQL query into the box below, and click on the Execute button.", height=100)
        st.button("Execute")

    



if __name__ == '__main__':
    gui = dbGUI()