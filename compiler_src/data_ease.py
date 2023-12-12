from de_parser import de_parser, print_ast
from de_grammar import de_lexer
import py_conversion as conv
import argparse



#hardcode the conversions: i.e. directly code what the final python file will be without looking up grammar.json

output_file = ''
output_str = ''

import_lines = [
    'import numpy as np',
    'import pandas as pd',
    'import matplotlib.pyplot as plt',
    'import seaborn as sns',
]





def parse_options(options_node):
    options_dict = {}
    for c in options_node.children:
        arg_name = c.children[0].node_value
        arg_values = []
        for v in c.children[1].children:
            arg_values.append(v.node_value)
        options_dict[arg_name] = arg_values
    
    return options_dict


objects_labels = {
    #key is object_label, value is the instance of the object
}

def get_object(object_type, label):
    obj = objects_labels.get(object_type + "_" + label)    
    if obj:
        return obj

    if object_type == "model":
        obj = conv.Model(label)
        objects_labels["model_" + label] = obj
    elif object_type == "metrics":
        obj = conv.Metrics(label)
        objects_labels["metrics_" + label] = obj
    elif object_type == "dataset":
        obj = conv.DataSet(label)
        objects_labels["dataset_" + label] = obj
    else:
        raise Exception("Unknown object encountered: {obj}".format(obj=object_type))


    return obj
        




def parse_command(command_node):
    action_node = command_node.children[0]
    object_node = command_node.children[1]
    label_node = command_node.children[2]
    options_node = command_node.children[3]
    options_dict = parse_options(options_node)
    print(action_node, object_node, label_node)
    print(options_dict)
    print('_'*15)

    obj = get_object(object_node.node_value, label_node.node_value)

    conversions = {
        ''
    }

    


    



def parse_program(program):
    for c in program.children:
        parse_command(c)




if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description='A language for Machine Learning that compiles into Python')
    arg_parser.add_argument('source_file', metavar='-s', type=str,
                   help='The source code to compile')
    
    arg_parser.add_argument('output_file', metavar='-o', type=str,
                   help='The output file to write to with the .py extension')
    
    args = arg_parser.parse_args()
    src = args.source_file
    output_file = args.output_file


    source = ''
    with open(src,mode='r') as f:
        source = f.read()

    program = de_parser.parse(source, lexer=de_lexer)
    parse_program(program)