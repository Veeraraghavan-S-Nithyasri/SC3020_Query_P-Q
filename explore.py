# IMPORTING neccessary packages
import pyscopg2
import database
import sqlparse
import os.path
import re # Need for get_tabs() in ParseSQL
#import json
import os
import pandas
import itertools

# Notes to self: 
''' To do for ParseSQL: get_attcol(), get_tabs()
    To do for Extract: rid_nallowed_str(), attcols()
    To do for Conversion: query_to_queryTemplate

   Need to think: In the query_to_queryTemplate() - need an execution() function ???
'''

# CONNECTION TO DATABASE
class Conn:
    # constructor that extablishes connection to DB
    def __init__ (self, hst = '', prt = 5432, db = 'tpch', uname = '', pwd = ''): 
        self.db_conn = pyscopg2.connect(hst = hst, prt = prt, db = db, usr = usr, pwd = pwd)
    # PS: We need to set up the DB locally on our comps with PGAdmin with the same usrname, pwd and fill in here
    
    # for disconnection
    def disconn(self):
        self.db_conn.close()

    # STATISTICS OF THE DATABASE
    ''' Note: Learnt this technique of extracting statistical summaries using pandas from ChatGPT 
        https://chat.openai.com/share/e33e40f4-bc7c-46a0-b38d-42268ef55be3 '''
    
    # This function is to be used by GUI part as well as in Query to Query Template Conversion
    def retreive_stats(query, db_conn):
        # this function takes the query and database connection object as arguments
        
        db = pandas.read_sql_query(query, db_conn)

        stats = db.describe()
        # save as a csv file
        stats.to_csv('statistical_summaries.csv')
        db_conn.close()

# PARSING OF THE SQL QUERY

class ParseSQL:
    # constructor
    def __init__(self, q):
        self.q = self.query(q) # clean query
        self.sq = self.splitq(q) # split query
        self.select_cols = self.get_attcol() # get attribute columns
        self.tabs = self.get_tabs() # get tables
        self.toks = sqlparse.parse(self.q)[0].tokens # token keywords

# UTILITY FUNCTIONS:
# 1. Take the raw SQL query as input and output a clean query
def query(self, sql_q):
    
    final_q = ''

    stmt = sqlparse.split(sql_q)
    s = stmt[0]
    parsed_q = sqlparse.format(s, reindent = True) # PS. need to decide if case must be UPPER, LOWER?
    split_p_q = parsed_q.splitlines()
    
    for i in split_p_q:
        final_q += ' {}'.format(i.strip())

    return final_q

# 2. Get the split
def splitq(self):
    stmt = sqlparse.split(self.q)
    s = stmt[0]
    parsed_q = sqlparse.format(s, reindent = True) # PS. need to decide if case must be UPPER, LOWER?
    split_p_q = parsed_q.splitlines()

    return split_p_q

# 3. Retreive attribute columns

def get_attcol(self):
    ''' Need to do'''

# 4. Get the tables

def get_tabs(self):
    
    tabs_arr = []
    stmt = list(sqlparse.parse(q))

    for x in stmt:
        s_type = stmt.get_type
        if s_type != 'UNKNOWN':

    ''' Need to do '''



# EXTRA UTIL FNS

def get_FROM(self, p_query): # used within get_tabs() and takes a parsed SQL query as argument
    # Gets 'FROM' from query

    ''' Need to do '''



# EXTRACTION OF ATTRIBUTES
    '''Note: We need to create a folder called tables and store the attribute/column names
    of the tables given in requirements as a text file'''

class Extract:
    
    # constructor to initialize table name and table attributes
    def __init__(self, tab):
        self.tab = tab
        self.atts = None

    def dtype(self):
        # retreives the datatypes of the attributes of the relation and store as a list/dict

        sql = """SELECT column_name, data_type FROM information_schema.columns WHERE table_name = {tab} AND data_type 
        IN ('integer', 'double precision', 'real', 'character', 'character varying', 'text', 'date', 'bigint', 'timestamp 
        with time zone', 'timestamp without time zone')"""

        sql = sql.format(tab = self.tab)

        # Here need to insert code that will actually connect to db and execute the query and do extraction ???

    
    def rid_nallowed_strs(self):
        # to get rid of strings that are non-allowed
        # basically non-alphanumeric cannot be there in the attributes

        ''' Need to do '''

    def att_cols(self):
        # get the columns that are selectable
        ''' Need to do '''

    def write_txt(self):
        # store into text file: 2 cases - dir exists vs doesn't exist

        # does dir exist? yes then write into
        if os.path.exists('tables'):
            with open('tables/{}.txt'.format(self.tab), 'w') as filehandle:
                for x in self.atts:
                    filehandle.write('{}\n'.format(x))
        
        # dir doesn't exist, create, then write into
        elif not os.path.exists('tables'):
            # create
            os.makedirs('tables')
            # write
            with open('tables/{}.txt'.format(self.tab), 'w') as filehandle:
                for x in self.atts:
                    filehandle.write('{}\n'.format(x))

    def get_attribs(self): # function that reads table and returns its attributes

        # check if table exists - Note: Tables are stored as text files
        if os.path.isfile('tables/{}.txt'.format(self.tab)):
            self.attribs = self.read_txt() # reads the attribs from the table's txt file
        
        # if table doesn't exist
        else:
            self.dtype() # retreives the datatypes of the attributes of the relation
            
            self.rid_nallowed_strs() # to get rid of strings that non-allowed
            self.att_cols() # get the columns that are selectable
            
            self.write_txt() # store into text file
        
        return self.attribs
    
# CONVERSION OF SQL QUERY

# For Brackets '(' and ')' in the queries
def bracket(str):
    # Get the string containing the key:value pair bracket_level : the string's content
    arr = []
    for x, token in enumerate(str): # token is extracting the brackets or paranthesis
        
        # Opening bracket
        if token == '(':
            arr.append(x)
        
        # Closing Bracket
        elif token == ')':
            first = arr.pop()
            arr_len = len(arr)
            yield (arr_len, str[first + 1: x]) # returns the value

# Needed in the scenario where there is a subquery
def temp_to_nested(nested_tok):
    # converts template to nested tokens
    flag_brackets = False
    q = nested_tok.value

    for i in list(bracket(q)):
        if 'select' in i[1].lower():
            flag_bracket = True

            ans = query_to_queryTemplate(i[1])
            q = q.replace(i[1], ans)
    # need to return the flag var as well as q
    return flag_brackets, q 

# Needed in the scenario where there is a subquery
def query_to_queryTemplate(q):
    # converts a SQL query into its corresponding template
    
    q_parsed = ParseSQL(q)
    temp = []
    ''' Need to do'''

def nested_to_temp(nested_q):
    tok = nested_q
    # converts a nested query into its template
    for j in list(bracket(nested_q)):
        
        c = j[1]
        if 'select' in c.lower():
            
            buf = ParseSQL(c)
            tok = tok.replace(j[1], query_to_queryTemplate(c))
    
    return tok


# QUERY EXECUTION PLAN AND OPERATOR TREE

# QUERY OPTIMIZED SELECTION









