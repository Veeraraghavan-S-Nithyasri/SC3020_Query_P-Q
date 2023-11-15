
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
        self.graph = graphviz.Graph("QEP viz",node_attr={'color':"red3"})
        self.optIndex = 0
        self.relIndex = 0

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
                except:
                    st.toast('Invalid query!')

                try:
                    self.qep = (conn.gen_qep(query))[0][0][0]
                    print(self.qep)
                    self.planTime = self.qep["Planning Time"]
                    self.execTime = self.qep["Execution Time"]
                except:
                    try:
                        self.qep = (conn.gen_qep(query))[1][0][0]
                        print(self.qep)
                        self.planTime = self.qep["Planning Time"]
                        self.execTime = self.qep["Execution Time"]
                    except Exception as error:
                        st.toast("QEP error!")
                        print("Exception: ", error)
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
            if self.qep != {}:
                print("\n\n\n\n\n")
                nodes = self.qep_viz(self.qep["Plan"])
                print(nodes)
                self.qep_graph(nodes)
            
            st.graphviz_chart(self.graph)

    def qep_viz(self, plan):
        operator = ""
        if "Join Type" in plan:
            operator += (str(plan["Join Type"]) + " ")
        operator += str(plan["Node Type"])
        if "Hash Cond" in plan:
            operator += (" on " + str(plan["Hash Cond"]))
        operator +=  ("\nBuffers - shared hit=" + str(plan["Shared Hit Blocks"]) + ", read=" + str(plan["Shared Read Blocks"]))
        output = [operator + "\n\n[" + str(self.optIndex) + "]"]
        self.optIndex += 1

        if "Plans" in plan:
            for subPlan in plan["Plans"]:
                subOutput = [self.qep_viz(subPlan)]
                output += subOutput
        else:
            relation = [plan["Relation Name"]]
            relation[0] += "\n{" + str(self.relIndex) + "}"
            output += relation
            self.relIndex += 1
        
        #print(output)
        return output
    
    def qep_graph(self, nodes):
        for node in nodes[1:]:
            if type(node) == list:
                self.graph.edge(nodes[0], node[0])
            else:
                self.graph.edge(nodes[0], node)
        
        for node in nodes[1:]:
            if type(node) == list:
                self.qep_graph(node)
            


    



if __name__ == '__main__':
    gui = dbGUI()