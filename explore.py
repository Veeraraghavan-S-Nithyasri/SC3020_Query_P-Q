# IMPORTING neccessary packages
import psycopg2

import sqlparse
from sqlparse.sql import IdentifierList
from sqlparse.sql import Identifier

import os.path
import re # Need for get_tabs() in ParseSQL
import os
import pandas
import itertools

from sqlparse.tokens import Keyword
from sqlparse.tokens import DML
import re

# CONNECTION TO DATABASE
class Conn:
    # constructor that extablishes connection to DB
    def __init__ (self, hst = '', prt = 5432, db = 'tpch', uname = '', pwd = ''): 
        self.db_conn = psycopg2.connect(hst = hst, prt = prt, db = db, usr = usr, pwd = pwd)
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
        self.sq = self.splitq() # split query
        self.select_cols = self.get_attcol() # get attribute columns
        self.tabs = self.get_tabs() # get tables
        self.toks = sqlparse.parse(self.q)[0].tokens # token keywords

    # UTILITY FUNCTIONS:
    # 1. Take the raw SQL query as input and output a clean query
    def query(self, sql_q):
        final_q = ''

        stmt = sqlparse.split(sql_q)[0]
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

    def get_all_attribs(self, tabs):
        ans = []
        for tab in tabs:
            with open(f"tables/{tab}.txt") as f:
                cols = f.read().replace("\n", ",")
                ans += cols.split(",")
                f.close()
        return [i for i in ans if i != ""]
    # 3. Retreive attribute columns
    def get_attcol(self):
        
        i = self.q.find("SELECT")
        j = self.q.find("FROM")
        cols = self.q[i+6:j].replace(" ", "")
        cols = cols.split(",")
        ans = []
        for col in cols:
            if col == '*':
                i = self.q.find("WHERE")
                tabs = self.q[j+4:i].replace(" ", "")
                ans += self.get_all_attribs(tabs.split(","))
                return ans
            
            elif col.find(".") < len(col):
                ans.append(col[col.find(".")+1:])
            else:
                ans.append(col)
        return ans
    # 4. Get the tables

    def get_tabs(self):
        
        tabs_arr = []
        stmt = list(sqlparse.parse(self.q))
	for x in stmt:
            s_type = stmt.get_type
            if s_type != 'UNKNOWN':
                from_token = self.get_FROM(stmt)

                # this piece of code gets the indentifiers in the table
                for x in from_token:
                    
                    if isinstance(x, IdentifierList):
                        for ID in x.get_identifiers():
                            ans = ID.value.replace('"', '').lower() 
                            yield ans

                    # if not an instance of IdentifierList but is of Indentifier
                    elif isinstance(x, Identifier):
                        
                        ans = x.ans.replace('"', '').lower() 
                        yield ans
                tabs_arr.append(set(list(ans)))
                
                final_tabs_arr = []
                temp = list(itertools.chain(*tabs_arr))
                for t in temp:
                    check = re.compile('[@_#^&*()<>!?/\|%$}{~:]').search(t)
                    if  check is None:
                        tab = t.split(' ') 
                        final_tabs_arr.append(tabs[0])
                        # to list
                final_tabs_arr = list(set(final_tabs_arr))
                return final_tabs_arr                    

         # EXTRA UTIL FN

        def get_FROM(self, parsed): # used within get_tabs() and takes a parsed SQL query as argument
            flag_from = False
            for x in parsed.tokens:
                if x.is_group:
                    for t in self.get_FROM(x):
                        yield t
                # if a 'from' is detected
                if flag_from:
                    if self.bool_select_nested(x): # this is to check if it's a select within a select
                        
                        for t in self.get_FROM(x):
                            yield t
                            
                    elif x.ttype is Keyword and x.value.upper() in ['ORDER', 'GROUP', 'BY', 'HAVING', 'GROUP BY']:
                        flag_from = False
                        StopIteration
                    else:
                        yield x
                if x.ttype is Keyword and x.value.upper() == 'FROM':
                    flag_from = True

        
   

    def bool_select_nested(self, parsed): # util fn for get_FROM
            if not parsed.is_group:
                return 0
            for x in parsed.tokens:
                if x.ttype is DML and x.value.upper() == 'SELECT':
                    return 1
            return 0
        
# EXTRACTION OF ATTRIBUTES
    '''Note: We need to create a folder called tables and store the attribute/column names
    of the tables given in requirements as a text file'''

class Extract:
    
    # constructor to initialize table name and table attributes
    def __init__(self, tab):
        self.tab = tab
        self.atts = None

    def retreive_text_read(self):
        cols = []
        with open('tables/{}.txt'.format(self.table_name), 'r') as textfile:
            for x in textfile:
		# need to get rid of \n break
                cursor = x[:-1]
                cols.append(cursor)
        return cols

    def dtype(self):
        # retreives the datatypes of the attributes of the relation and store as a list/dict

        sql = """SELECT column_name, data_type FROM information_schema.columns WHERE table_name = {tab} AND data_type 
        IN ('integer', 'double precision', 'real', 'character', 'character varying', 'text', 'date', 'bigint', 'timestamp 
        with time zone', 'timestamp without time zone')"""

        sql = sql.format(tab = self.tab)

        # Here need to insert code that will actually connect to db and execute the query and do extraction ???
        con = db_conn.DBConnection()
        ans = db_conn.execute(q)
        con.close()

        ans_arr = []
        for att, datype in ans:
            ans_arr.append({"column_name": att, "data_type": datype,})
        
        # write in the ans_arr into the attributes
        self.atts = ans_arr
    
    ''' Need to remove this commented code for submission if this is not needed for 
    def rid_nallowed_strs(self):
        # to get rid of strings that are non-allowed
        # basically non-alphanumeric cannot be there in the attributes - this will make optimization faster

        lst_of_atts = []

        for att in self.atts:
            if att['data_type'] in ['text', 'character', 'character varying']:
        
        # query 
		q = "SELECT count(*) FROM {tabn} WHERE {attcoln} ~ '^.*[^A-Za-z0-9 .-].*$'".format(tabn = self.tab, attcoln=item[''])
                
                
                
                
                
                #actually connect to the DB to execute 
                
                conn = db_conn.DBConnection()
                answer = db_conn.execute(query)
                db_conn.close()

                number = answer[0][0]
                
		if number != 0:
                    continue
                
            lst_of_atts.append(att)

        self.atts = lst_of_atts
    

    def att_cols(self):
        
	if os.path.isfile('tables/{}.txt'.format(self.table_name)):
		self.atts = self.get_attribs()
         # call all the util functions to do make the query clean
	else:
            self.dtype()
            self.rid_nallowed_strs()
            
            # then we write and store into the file
            self.write_txt()
	# return the attribute columns
        return self.atts

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
            self.attribs = self.retreive_text_read() # reads the attribs from the table's txt file
        
        # if table doesn't exist
        else:
            self.dtype() # retreives the datatypes of the attributes of the relation
            
            self.rid_nallowed_strs() # to get rid of strings that non-allowed
            self.att_cols() # get the columns that are selectable
            
            self.write_txt() # store into text file
        
        return self.attribs'''
    
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

'''Needed in the scenario where there is a subquery
def query_to_queryTemplate(q):
    converts a SQL query into its corresponding template
    
    q_parsed = ParseSQL(q)
    temp = []'''

 
def nested_to_temp(nested_q):
    tok = nested_q
    # converts a nested query into its template
    for j in list(bracket(nested_q)):
        
        c = j[1]
        if 'select' in c.lower():
            
            buf = ParseSQL(c)
            #tok = tok.replace(j[1], query_to_queryTemplate(c))
	    tok = buf
    
    return tok









