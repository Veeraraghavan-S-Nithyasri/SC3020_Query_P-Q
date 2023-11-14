
'''Streamlit interface test demo'''

import streamlit as st
import graphviz
from explore import Conn
from explore import ParseSQL
from new_explore import DBConn
from new_explore import gen_qep
import pandas as pd
import pyautogui

class dbGUI:
    def __init__(self):
        self.query_output = pd.DataFrame()
        self.qep = {}
        self.planTime = 0
        self.execTime = 0

        st.title('SC3020 Project 2')
        st.markdown('''
                    This interface is designed for visualisation of SQL query execution & exploration.
                    ''')
        st.sidebar.title("User Credentials")
        st.sidebar.text_input("Host", key="host")
        st.sidebar.text_input("Port", key="port")
        st.sidebar.text_input("Database", key="database")
        st.sidebar.text_input("User", key="user")
        st.sidebar.text_input("Password", key="password")

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
                try:
                    conn = DBConn(st.session_state.host, st.session_state.port, st.session_state.database, st.session_state.user, st.session_state.password)
                except:
                    st.toast('Invalid credentials!')
                    return
                try:
                    self.query_output = conn.execute_query(query)
                    self.qep = (conn.gen_qep(query))[1][0][0]
                    self.planTime = self.qep["Planning Time"]
                    self.execTime = self.qep["Execution Time"]
                except:
                    st.toast('Invalid query!')
            else:
                st.toast('Missing query!')
        if st.button("Reset"):
            pyautogui.hotkey("ctrl", "F5")


    
    # Visualisation of disk blocks accessed
    def diskAccessVisual(self):
        st.header('Disk blocks accessed')

    def diskAccessVisual(self, data):
        st.dataframe(data)


    # QEP display
    def qepDisplay(self):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("Planning Time: " + str(self.planTime))
            st.markdown("Execution Time: " + str(self.execTime))
        with col2:
            st.json(self.qep)
            graph = graphviz.Graph("QEP viz")
            if self.qep != {}:
                print("\n\n\n\n\n")
                self.qep_viz(self.qep["Plan"])
            """
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
            """
            st.graphviz_chart(graph)

    def qep_viz(self, plan):
        output = [plan["Node Type"]]

        if "Plans" in plan:
            for subPlan in plan["Plans"]:
                subOutput = [self.qep_viz(subPlan)]
                output += subOutput
        else:
            output += [plan["Relation Name"]]
        print('________________________')
        print(output)
        return output
            


    



if __name__ == '__main__':
    gui = dbGUI()