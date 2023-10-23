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
