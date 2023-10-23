# IMPORTING neccessary packages
import pyscopg2
import itertools
import os.path
import database
import sqlparse
# import re
import os

# CONNECTION TO DATABASE
class Conn:
    # constructor that extablishes connection to DB
    def __init__ (self, hst = '', prt = 5432, db = 'tpch', uname = '', pwd = ''): 
        self.db_conn = pyscopg2.connect(hst = hst, prt = prt, db = db, usr = usr, pwd = pwd)
    # PS: We need to set up the DB locally on our comps with PGAdmin with the same usrname, pwd and fill in here
    
    # for disconnection
    def disconn(self):
        self.db_conn.close()

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

# 4. Get the tables

def get_tabs(self):


# EXTRACTION OF ATTRIBUTES
'''Note: We need to create a folder called tables and store the attribute/column names
    of the tables given in requirements as a text file'''
class Extract:
    
    # constructor to initialize table name and table attributes
    def __init__(self, tab):
        self.tab = tab
        self.attribs = None

    def dtype(self):
        # retreives the datatypes of the attributes of the relation
    
    def fkeys(self):
        # retreives the foreign keys of relation
    
    def rid_nallowed_strs(self):
        # to get rid of strings that non-allowed
    
    def att_cols(self):
        # get the columns that are selectable

    def write_txt(self):
        # store into text file

    def get_attribs(self): # function that reads table and returns its attributes

        # check if table exists - Note: Tables are stored as text files
        if os.path.isfile('tables/{}.txt'.format(self.tab)):
            self.attribs = self.read_txt() # reads the attribs from the table's txt file
        
        # if table doesn't exist
        else:
            self.dtype() # retreives the datatypes of the attributes of the relation
            
            self.fkeys() # retreives the foreign keys of relation
            self.rid_nallowed_strs() # to get rid of strings that non-allowed
            self.att_cols() # get the columns that are selectable
            
            self.write_txt() # store into text file
        
        return self.attribs
    
# CONVERSION OF SQL QUERY

def nested_to_temp(nested_q):
    # converts a nested query into its template

def temp_to_nested(nested_tok):
    # converts template to nested tokens

def query_to_queryTemplate(q):
    # converts a SQL query into its corresponding template
    
    q_parsed = ParseSQL(q)
    temp = []

def bracket(str):
    # Get the string containing the key:value pair bracket_level : the string's content

# QUERY EXECUTION PLAN AND OPERATOR TREE

# QUERY OPTIMIZED SELECTION









