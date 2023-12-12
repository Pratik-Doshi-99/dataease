from de_grammar import de_lexer, tokens
from ply import yacc as yacc
import argparse



ast_cache = {

}

class ASTNode:
    def __init__(self, node_type, node_value, unique_key = ''):
        self.node_type = node_type
        self.unique_key = unique_key
        self.children = []
        self.node_value = node_value
    
    def add_child(self, child):
        self.children.append(child)

    def add_children(self, children):
        self.children += children

    def get_children(self):
        return self.children
    


###########################################################################
#               CODE FOR PARSER
###########################################################################


def p_program(p):
    '''
    program : command_list
    '''
    node = ASTNode('program','')
    node.add_children(p[1])
    p[0] = node


def p_command_list(p):
    '''
    command_list : command_list command 
            | command'''
    
    command_list = []
    for i in range(1, len(p)):
        if type(p[i]) == type(ASTNode('','')):
            command_list.append(p[i])
        else:
            command_list += p[i]

    p[0] = command_list

    # print('Command List',end=': ')
    # for e in p:
    #     print(e,end=' , ')
    # print()

def p_command(p):
    '''
    command : ACTION OBJECT TEXT COLON options_list
    '''
    node = ASTNode('command','')
    node.add_child(ASTNode('action',p[1]))
    node.add_child(ASTNode('object',p[2]))
    node.add_child(ASTNode('text',p[3]))
    options_node = ASTNode('options-list','')
    options_node.add_children(p[5])
    node.add_child(options_node)


    p[0] = node
    # print('Command',end=': ')
    # for e in p:
    #     print(e,end=' , ')
    # print()


def p_option_list(p):
    '''
    options_list : options_list c_option
                | c_option
    '''
    option_list = []
    for i in range(1, len(p)):
        if type(p[i]) == type(ASTNode('','')):
            option_list.append(p[i])
        else:
            option_list += p[i]

    p[0] = option_list

    # print('Options List',end=': ')
    # for e in p:
    #     print(e,end=' , ')
    # print()
    # print(p)
    #p[0] = ASTNode(p,)
    




def p_option(p):
    '''
    c_option : OPTION VERB COLON value_list
    '''
    
    
    node = ASTNode('option','')
    node.add_child(ASTNode('verb',p[2]))
    value_node = ASTNode('value-list','')
    value_node.add_children(p[4])
    node.add_child(value_node)
    
    p[0] = node



def p_option_text(p):
    '''
    c_option : OPTION TEXT COLON value_list
    '''
    node = ASTNode('option','')
    node.add_child(ASTNode('text',p[2]))
    value_node = ASTNode('value-list','')
    value_node.add_children(p[4])
    node.add_child(value_node)
    
    p[0] = node



def p_value_list(p):
    '''
    value_list : value_list COMMA value
            | value
    '''
    
    #print(p[-1])

    value_list = []
    for i in range(1, len(p),2):
        if type(p[i]) == type(ASTNode('','')):
            value_list.append(p[i])
        else:
            value_list += p[i]

    p[0] = value_list

    # print('Value List',end=': ')
    # for e in p:
    #    print(e,end=' , ')
    # print()
    

def p_number(p):
    '''
    value : NUMBER
    '''
    # print('Value',end=': ')
    # for e in p:
    #    print(e,end=' , ')
    # print()
    p[0] = ASTNode('number',p[1])

def p_text(p):
    '''
    value : TEXT 
    '''
    # print('Value',end=': ')
    # for e in p:
    #    print(e,end=' , ')
    # print()
    p[0] = ASTNode('text',p[1])


def p_constant(p):
    '''
    value : CONSTANT 
    '''
    # print('Value',end=': ')
    # for e in p:
    #    print(e,end=' , ')
    # print()
    p[0] = ASTNode('constant',p[1])

def p_literal(p):
    '''
    value : LITERAL 
    '''
    # print('Value',end=': ')
    # for e in p:
    #    print(e,end=' , ')
    # print()
    p[0] = ASTNode('literal',p[1])


def p_error(p):
    raise Exception(p)

de_parser = yacc.yacc(debug=True)


def print_ast(node, level = 0, left_index = 0, parent=None):
    print('\t'*level + '<%s,%s>'%(node.node_type,node.node_value))
    for c in node.children:
        print_ast(c, level + 1, left_index = 1, parent = node)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description='A language for Machine Learning that compiles into Python')
    arg_parser.add_argument('source_file', metavar='-s', type=str,
                   help='The source code to compile')
    
    args = arg_parser.parse_args()
    src = args.source_file

    source = ''
    with open(src,mode='r') as f:
        source = f.read()

    program = de_parser.parse(source, lexer=de_lexer)
    print_ast(program)

