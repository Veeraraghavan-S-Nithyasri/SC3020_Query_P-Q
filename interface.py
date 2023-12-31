import streamlit as st
import graphviz
from explore import DBConn
from explore import queryDiskBlocks
import pandas as pd
import sys

class dbGUI:
    def __init__(self):
        self.query_output = pd.DataFrame()
        self.query_outputB =  pd.DataFrame()
        self.qep = {}                                                       #JSON object containing the QEP plan of the SQL query
        self.planTime = 0                                                   #Variable containing the planning time of the SQL query
        self.execTime = 0                                                   #Variable containing the execution time of the SQL query
        self.graph = graphviz.Graph("QEP viz",node_attr={'color':"red3"})   #graphviz.graph object that displays a QEP tree
        self.optIndex = 0                                                   #Operator counter
        self.relIndex = 0                                                   #Relation counter

        self.titleDisplay()

        self.sideBar()

        self.queryInput()

        self.tab1, self.tab2 = st.tabs(["Query Execution Plan", "Data Output"])
        with self.tab1:
            self.qepDisplay()
        with self.tab2:
            self.diskAccessVisual(self.query_outputB)


    #Title section displaying information about the web application
    def titleDisplay(self):
        st.title('SC3020 Project 2')
        st.markdown('''
                    This interface is designed for visualisation of SQL query execution & exploration.\n
                    The "Query Execution Plan" tab shows the query execution plan while the "Data Output" tab shows the tuples retrieved.\n
                    How to use:\n
                    1. Enter your user credentials (host, port, database, user, password) in the fields provided in the sidebar.\n
                    2. Enter the query that you want to run.\n
                    3. Press the "execute" button and wait for the results.
                    ''')


    #Sidebar section for users to enter their credentials
    def sideBar(self):
        st.sidebar.title("User Credentials")
        st.sidebar.text_input("Host", key="host")
        st.sidebar.text_input("Port", key="port")
        st.sidebar.text_input("Database", key="database")
        st.sidebar.text_input("User", key="user")
        st.sidebar.text_input("Password", key="password")


    # SQL query input section
    def queryInput(self):
        st.header('Query Input')
        query = self.inputBox = st.text_area("Key in your SQL query into the box below, and click on the Execute button.", height=100, key="queryInput")
        if st.button("Execute"):
            print("\n\n\n\n\n\n\n\n\n\n\n\n\n____________________\nStart execution")
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
                    return

                try:
                    #queryDiskBlocks(query)
                    self.query_outputB = conn.execute_query(queryDiskBlocks(query))
                except:
                    print(error)
                    st.toast('Disk block visualization error!')

                try:
                    self.qep = (conn.gen_qep(query))[0][0][0]
                    self.planTime = self.qep["Planning Time"]
                    self.execTime = self.qep["Execution Time"]
                except:
                    try:
                        self.qep = (conn.gen_qep(query))[1][0][0]
                        self.planTime = self.qep["Planning Time"]
                        self.execTime = self.qep["Execution Time"]
                    except Exception as error:
                        st.toast("QEP error!")
                        print("Exception: ", error)
            else:
                st.toast('Missing query!')

        def on_click():
            st.session_state.queryInput = ""
            print("Query input cleared")
        
        st.button("Reset", on_click=on_click)


    # Visualisation of disk blocks accessed
    def diskAccessVisual(self, data):
        if len(data) > 0:
            data = pd.DataFrame(data)
            new_header = data.iloc[0]
            data = data[1:]
            data.columns = new_header
            print("Data size: ", sys.getsizeof(data))
            st.markdown('''Summary of disk blocks accessed''')
            for col in data:
                if "ctid_blocknumber" in col:
                    blockData = pd.DataFrame(data[col].unique(), columns=[col])
                    tableName = col.replace('_ctid_blocknumber', '')
                    st.markdown("Blocks accessed for table " + tableName)
                    st.dataframe(blockData, hide_index=True)
            st.markdown('''Data output''')
            if sys.getsizeof(data) < 642243305:
                st.dataframe(data)
            else:
                st.markdown('''Data is too large to be displayed fully!
                            The data below only shows the first 5 tuples retrieved.''')
                st.dataframe(data.head(10))
        else:
            st.markdown("No data available!")


    # QEP display
    def qepDisplay(self):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("Planning Time: " + str(self.planTime))
            st.markdown("Execution Time: " + str(self.execTime))

        with col2:
            #st.json(self.qep)
            st.markdown('''
                        QEP visualisation tree\n
                        NOTE: The numbers at the bottom of each tree node are for mapping purposes and do not indicate any order of execution.
                        ''')
            if self.qep != {}:
                nodes = self.qepViz(self.qep["Plan"])
                #print(nodes)
                self.qepGraph(nodes)
                st.graphviz_chart(self.graph)


    #Function used to extract out relevant information from the QEP JSON retrieved
    def qepViz(self, plan):
        operator = ""
        if "Join Type" in plan:
            operator += (str(plan["Join Type"]) + " ")
        operator += str(plan["Node Type"])
        if "Hash Cond" in plan:
            operator += (" on " + str(plan["Hash Cond"]))
        if "Index Cond" in plan:
            operator += (" on " + str(plan["Index Cond"]))
        operator +=  ("\nBuffers - shared hit=" + str(plan["Shared Hit Blocks"]) + ", read=" + str(plan["Shared Read Blocks"]))
        output = [operator + "\n[" + str(self.optIndex) + "]"]
        self.optIndex += 1

        if "Plans" in plan:
            for subPlan in plan["Plans"]:
                subOutput = [self.qepViz(subPlan)]
                output += subOutput
        else:
            relation = [plan["Relation Name"]]
            relation[0] += "\n{" + str(self.relIndex) + "}"
            output += relation
            self.relIndex += 1
        
        #print(output)
        return output


    #Function used for adding operators/relations as nodes to the QEP tree
    def qepGraph(self, nodes):
        for node in nodes[1:]:
            if type(node) == list:
                self.graph.edge(nodes[0], node[0])
            else:
                self.graph.edge(nodes[0], node)
        
        for node in nodes[1:]:
            if type(node) == list:
                self.qepGraph(node)
            


if __name__ == '__main__':
    gui = dbGUI()