import ply.lex as lex
import argparse


###########################################################################
#               CODE FOR LEXER
###########################################################################

keywords = {
    'load':('LOAD','ACTION'),
    'create':('CREATE','ACTION'),
    'modify': ('MODIFY','ACTION'),
    'delete': ('DELETE','ACTION'),
    'display': ('DISPLAY','ACTION'),
    'copy': ('COPY','ACTION'),
    'run': ('RUN','ACTION'),
    'preprocess':('PREPROCESS','ACTION'),
    'split':('SPLIT','ACTION'),
    'model':('MODEL','OBJECT'),
    'dataset':('DATASET','OBJECT'),
    'row':('ROW','OBJECT'),
    'col':('COL','OBJECT'),
    'chart':('CHART','OBJECT'),
    'metrics':('METRICS','OBJECT'),
    'as':('AS','VERB'),
    'from':('FROM','VERB'),
    'to':('TO','VERB'),
    'on':('ON''VERB'),
    'not':('NOT','NOT'),#not operator is a word, hence it is put in keywords
    'yes':('YES','CONSTANT'),
    'no':('NO','CONSTANT'),
}

# token dict shows all symbol like tokens (words go in keywords because they will match the regex for WORD)
token_dict = {
    'boolean_symbols' : ['GREATER','LESSER','EQUAL'],
    'general_symbols' : ['OPTION','COLON','COMMA'],
    'constants' : ['LITERAL','NUMBER'],
    'language_construct': ['WORD','TEXT','NEWLINE','WHITESPACE']
}


tokens = [t for k in token_dict for t in token_dict[k]] + list(set([keywords[k][1] for k in keywords]))
t_EQUAL = '='
t_GREATER = '>'
t_LESSER = '<'
#t_OPTION = '=>'
t_COLON = ':'
t_COMMA = ','
#t_LITERAL = r'"([^"\\]*(\\.[^"\\]*)*)"'
t_LITERAL = r'"[^"]*"'
#t_CONTEXT = ':\\n[ ]+'
t_WHITESPACE = '\ '
#t_ignore = ' '


#context_length = 0
#def t_SOPEN(t):
#    ':[ ]*\\n[ ]+'
#    t.type = 'SOPEN'
#    t.lexer.lineno += 1
#    print('Length of scope open:',len(t.value))
#    return t


# def t_WHITESPACE(t):
#    '\ '
#    #print('White space encountered')
#    #this must be defined otherwise we wont be able to track the spaces in 'OPTION'
#    t.type = 'WHITESPACE'
#    return t

    

def t_OPTION(t):
    '[ ]+=>'
    t.type = 'OPTION'
    t.indentation = len(t.value) - 2
    #print('Length of context:',len(t.value))
    return t


def t_NEWLINE(t):
    '\\n'
    #print('Line',t.lexer.lineno,'complete')
    t.lexer.lineno += 1


'''
[0-9]*[a-zA-Z]*(\/|-|.|)*([a-zA-Z]+)[0-9]*[a-zA-Z]*(\/|-|.|)*
([0-9]|[a-zA-Z]|(\/|.|-))*([a-zA-Z]+)([0-9]|[a-zA-Z]|(\/|.|-))*
'''

def t_WORD(t):
    #'(?/)([a-zA-Z])+([0-9]|[a-zA-Z]|/|.)*'
    #'^[a-zA-Z0-9/.]+$'
    #'[a-zA-Z]+[0-9]*[a-zA-Z]*'
    '([0-9]|[a-zA-Z]|(/|\.|-))*([a-zA-Z]+)([0-9]|[a-zA-Z]|(/|\.|-))*'
    if t.value.lower() in keywords:
        t.type = keywords[t.value.lower()][1]
    else:
        t.type = 'TEXT'
    return t


def t_NUMBER(t):
    '[0-9]+\.?[0-9]*'
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    
    return t
    #print(t.value)

def t_error(err):
    print(err)


class DSLexer():
    def __init__(self, lexer):
        self.lexer = lexer

    def token(self):
        t = self.lexer.token()
        while t and t.type == 'WHITESPACE':
            #print('skipping whitespace')
            t = self.lexer.token()
        return t
        

    def input(self, *args, **kwds):
        self.lexer.input(*args, **kwds)

    def __iter__(self):
        return self

    def next(self):
        t = self.token()
        if t is None:
            raise StopIteration
        return t
    
    __next__ = next


default_lexer = lex.lex()
de_lexer = DSLexer(default_lexer)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A language for Machine Learning that compiles into Python')
    parser.add_argument('source_file', metavar='-s', type=str,
                   help='The source code to compile')
    #parser.add_argument('output_file', metavar='-o', type=str,
    #               help='The target .py file')
    args = parser.parse_args()
    src = args.source_file
    #output = args.output_file

    source = ''
    with open(src,mode='r') as f:
        source = f.read()

    de_lexer.input(source)

    for tok in de_lexer:
        print(tok)
        
