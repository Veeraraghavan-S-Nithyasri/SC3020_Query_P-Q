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