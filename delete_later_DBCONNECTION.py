# CONNECTION TO DATABASE
class Conn:
    # constructor that extablishes connection to DB
    def __init__ (self, hst = '', prt = 5432, db = 'tpch', uname = '', pwd = ''): 
        self.db_conn = pyscopg2.connect(hst = hst, prt = prt, db = db, usr = usr, pwd = pwd)
    # PS: We need to set up the DB locally on our comps with PGAdmin with the same usrname, pwd and fill in here
    
    # for disconnection
    def disconn(self):
        self.db_conn.close()