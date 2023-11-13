import psycopg2
import json
import os
import sqlparse


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
        return res

    def disconnect(self):
        self.conn.close()
    

class ParseSQL:
    def __init__(self, query):
        self.query = self.clean_query(query)
        self.tokens = sqlparse.parse(self.query)[0].tokens
        #self.tables = self.extract_tables_from_query()
        #self.columns = self.get_attcols()
        

    def clean_query(self, sql):
        statements = sqlparse.split(sql)
        statement = statements[0]
        cleaned = sqlparse.format(statement, reindent=True, keyword_case='upper')
        cleaned = cleaned.splitlines()

        cleaned_query = ''
        for item in cleaned:
            cleaned_query += ' {}'.format(item.strip())
        return cleaned_query
    
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

    
    
    
        


