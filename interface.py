
'''Streamlit interface test demo'''

import streamlit as st
import graphviz
from explore import Conn
from explore import ParseSQL
import pandas as pd

class dbGUI:
    def __init__(self):
        self.query_output = pd.DataFrame()
        st.title('SC3020 Project 2')
        st.markdown('''
                    This interface is designed for visualisation of SQL query execution & exploration.
                    ''')
        self.queryInput()
        self.tab1, self.tab2 = st.tabs(["Query Execution Plan", "Data Output"])
        with self.tab1:
            self.qepDisplay()
        with self.tab2:
            self.diskAccessVisual(self.query_output)


    # SQL query input section
    def queryInput(self):
        st.header('Query Input')
        query = self.inputBox = st.text_area("Key in your SQL query into the box below, and click on the Execute button.", height=100)
        if st.button("Execute"):
            if query != "":
                conn = Conn()
                parsed = ParseSQL(query)
                try:
                    self.query_output = conn.retreive_stats(parsed.q, conn.db_conn)
                except:
                    st.toast('Invalid query!')
            else:
                st.toast('Missing query!')


    
    # Visualisation of disk blocks accessed
    def diskAccessVisual(self):
        st.header('Disk blocks accessed')

    def diskAccessVisual(self, data):
        st.dataframe(data)


    # QEP display
    def qepDisplay(self):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("Planning Time: -")
            st.markdown("Execution Time: -")
        with col2:
            graph = graphviz.Graph("QEP viz")
            graph.node('1', 'Hash join on c=h')
            graph.node('2', 'Index nested loop join on g=a')
            graph.node('3', "Selection on w.id='abc'")
            graph.node('4', 'W')
            graph.node('5', 'Sort-merge join on d=f')
            graph.node('6', 'R')
            graph.node('7', "Selection on d='Hello' AND e='World'")
            graph.node('8', 'U')
            graph.node('9', 'S')
            graph.edges(['12', '13', '25', '26', '34', '57', '58', '79'])
            st.graphviz_chart(graph)
            


    



if __name__ == '__main__':
    gui = dbGUI()