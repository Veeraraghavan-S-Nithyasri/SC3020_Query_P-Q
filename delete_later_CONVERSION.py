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
