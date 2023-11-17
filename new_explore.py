import psycopg2
import json
import os
import sqlparse
from sqlparse.tokens import Keyword, DML
from sqlparse.sql import Identifier, IdentifierList


def get_all_tables():
    query = """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_type='BASE TABLE'
            and table_schema='public'
    """
    conn = DBConn()
    results = conn.execute_query(query)
    return [result[0] for result in results]


class DBConn:
    def __init__(self, host="localhost", port=5432, database="tpch", user="postgres", password="password"):
        self.conn = psycopg2.connect(host=host, port=port, database=database, user=user, password=password)
        self.cursor = self.conn.cursor()
    
    def execute_query(self, query):
        self.cursor.execute(query)
        res = self.cursor.fetchall()
        column_names = tuple([desc[0] for desc in self.cursor.description])
        res = [column_names] + res
        return res
    
    def gen_qep(self, query):
        res = self.execute_query('EXPLAIN (ANALYZE, COSTS, VERBOSE, BUFFERS, FORMAT JSON ) ' + query)
        return res

    def disconnect(self):
        self.conn.close()
    

class ParseSQL:
    def __init__(self, query):
        self.query = self.clean_query(query)
        self.tokens = sqlparse.parse(self.query)[0].tokens
        #self.tables = self.extract_tables_from_query()
        #self.columns = self.get_attcols()
        
    def extract_all_tables(self):
        stm = sqlparse.parse(self.query)
        tables = []
        for i in stm:
            e = self.extractNested(i)
            for j in e:
                if isinstance(j, IdentifierList):
                    for l in j.get_identifiers():
                        l = l.value.replace('"', '').lower()
                        tables.append(l)
                if isinstance(j, Identifier):
                    l = j.value.replace('"', '').lower()
                    tables.append(l)
        return tables
    
    def extract_all_table_names(self):
        stm = sqlparse.parse(self.query)
        tables = []
        for i in stm:
            e = self.extractNested(i)
            for j in e:
                if isinstance(j, IdentifierList):
                    for l in j.get_identifiers():
                        k = l.get_name()
                        l = l.value.replace('"', '').lower()
                        tables.append(k)
                if isinstance(j, Identifier):
                    k = j.get_name()
                    l = j.value.replace('"', '').lower()
                    tables.append(k)
        return tables

    def extractNested(self, statement):
        upper_lvl = False
        for i in statement.tokens:
            if i.is_group:
                for j in self.extractNested(i):
                    yield j
            if upper_lvl:
                if self.isNested(i):
                    for j in self.extractNested(i):
                        yield j
                elif i.ttype is Keyword and i.value.upper() in ["ORDER BY", "GROUP BY", "HAVING", "ORDER", "BY"]:
                    upper_lvl = False
                    StopIteration
                else:
                    yield i
            if i.ttype is Keyword and i.value.upper() == "FROM":
                upper_lvl = True
    
    def clean_query(self, sql):
        statements = sqlparse.split(sql)
        statement = statements[0]
        cleaned = sqlparse.format(statement, reindent=True, keyword_case='upper')
        cleaned = cleaned.splitlines()

        cleaned_query = ''
        for item in cleaned:
            cleaned_query += ' {}'.format(item.strip())
        return cleaned_query
    

    def isNested(self, statement):
        '''
            checks whehter the parsed statement of a SQL query is nested (subqueries) or not

        '''
        if not statement.is_group:
            return False
        
        for st in statement.tokens:
            if st.ttype is DML and (st.value.upper() == "SELECT" or st.value.upper() == "select"):
                return True
        return False
        
    def filter_columns(self, table_name):
        query = f"""
            SELECT 
                column_name, data_type
            FROM 
                information_schema.columns
            WHERE 
                table_name = '{table_name}'
                AND data_type IN (
                    'bigint', 'integer',
                    'double precision', 'real',
                    'character', 'character varying', 'text',
                    'date', 'timestamp without time zome', 'timestamp with time zone'
                )
        """
        conn = DBConn()
        res = conn.execute_query(query)
        dtype_list = []
        for column_name, dtype in res:
            dtype_list.append({
                "col": column_name,
                "dtype": dtype
            })
        result_list = []

        for item in dtype_list:
            if item['dtype'] in ['character', 'character varying', 'text']:
                query = f"""
                    SELECT count(*)
                    FROM {table_name}
                    WHERE {item['column_name']} ~ '^.*[^A-Za-z0-9 .-].*$'
                """
                
                res2 = conn.execute_query(query)
                non_alpha = res2[0][0]
                if non_alpha != 0:
                    continue
                
            result_list.append(item)
        
        query = f"""
            SELECT
                kcu.column_name
            FROM 
                information_schema.table_constraints AS tc 
                JOIN information_schema.key_column_usage AS kcu
                ON tc.constraint_name = kcu.constraint_name
                AND tc.table_schema = kcu.table_schema
                JOIN information_schema.constraint_column_usage AS ccu
                ON ccu.constraint_name = tc.constraint_name
                AND ccu.table_schema = tc.table_schema
            WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name={table_name};
        """
        res3 = conn.execute_query(query)
        fk = []
        for item in res3:
            fk.append(item[0])
        conn.disconnect()

        filtered_attribs = result_list - fk
        return filtered_attribs
        
    def get_columns(self, table_name):
        if os.path.exists(f"tables/{table_name}.txt"):
            with open(f"table{table_name}", "r") as f:
                attribs = f.read()
                return attribs.split("\n")
        attribs = self.filter_columns(table_name)
        with open(f"tables/{table_name}.txt", 'w') as f:
            f.writelines([a+"\n" for a in attribs])
            f.close()
        return attribs
        #'EXPLAIN (ANALYZE, COSTS, VERBOSE, BUFFERS, FORMAT JSON ) ' + 


    
def gen_qep(query):
    conn = DBConn()
    res = conn.execute_query('EXPLAIN (ANALYZE, COSTS, VERBOSE, BUFFERS, FORMAT JSON ) ' + query)
    return res


# adds ctid with block number column to sql query
def queryDiskBlocks(query):
    parsed = ParseSQL(query)
    stm = sqlparse.parse(query)
    tokens = parsed.tokens

    querySplitA = ""
    querySplitB = ""
    querySplitBstr = []

    select_end = False

    # splits the SELECT clause from the rest of the SQL query. The entire SELECT clause is stored in a single string.
    for token in tokens:
        #print(token)
        if token.match(sqlparse.tokens.Keyword, ["from", "FROM"]):
            select_end = True
        if not select_end:
            querySplitA += str(token)
        else:
            if isinstance(token, IdentifierList):
                for idfr in token:
                    querySplitBstr.append(str(idfr))
            else:
                querySplitBstr.append(str(token))
            

    print(querySplitA)
    print(querySplitBstr)

    # extracts all table identifiers used in the SQL query.
    tableNames = parsed.extract_all_tables()
    print(tableNames)

    # modified version of extract_all_tables, it instead extracts the current names of the tables, which is either an alias or its real name.
    tableNames_current = parsed.extract_all_table_names()
    print(tableNames_current)

    # partial query modifier; to account for any nested queries, it adds tables in those queries into the upper level FROM clause.
    for table in tableNames:
        table_included = False
        for s in querySplitBstr:
            if s.casefold() == table.casefold():
                table_included = True
        if not table_included:
            querySplitBstr.insert(1, ' ')
            querySplitBstr.insert(2, table)
            querySplitBstr.insert(3, ',')

    querySplitB = ''.join(querySplitBstr)
    print(querySplitB)



    # modifies the SELECT clause from earlier to also select the block numbers from the ctid attribute.
    for item in tableNames_current:
        print(item)
        querySplitA += ", (" + item + ".ctid::text::point)[0]::bigint as " + item + "_ctid_blocknumber "

    
    newquery = querySplitA + querySplitB
    print(newquery)
    
    return newquery


