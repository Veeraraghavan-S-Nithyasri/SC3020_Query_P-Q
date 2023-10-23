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
            from_token = self.getFROM(stmt)

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

    



                    
    ''' Need to do '''

# EXTRA UTIL FNS

def get_FROM(self, p_query): # used within get_tabs() and takes a parsed SQL query as argument
    # Gets 'FROM' from query

    ''' Need to do '''