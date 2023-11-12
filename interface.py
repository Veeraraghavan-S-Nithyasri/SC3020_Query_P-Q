
'''Streamlit interface test demo'''

import streamlit as st
import graphviz

class dbGUI:
    def __init__(self):
        st.title('SC3020 Project 2')
        st.markdown('''
                    This interface is designed for visualisation of SQL query execution & exploration.
                    ''')
        self.queryInput()
        tab1, tab2 = st.tabs(["Query Execution Plan", "Data Output"])
        with tab1:
            self.qepDisplay()
        with tab2:
            self.diskAccessVisual()


    # SQL query input section
    def queryInput(self):
        st.header('Query Input')
        self.inputBox = st.text_area("Key in your SQL query into the box below, and click on the Execute button.", height=100)
        st.button("Execute")

    
    # Visualisation of disk blocks accessed
    def diskAccessVisual(self):
        st.header('Disk blocks accessed')


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