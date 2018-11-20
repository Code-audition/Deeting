# -*- coding: utf-8 -*-

import json
import sys
import os

contaminated_variable = [
    "_GET",
    "_POST",
    "_COOKIE",
]
dangerous_function_list = [
    "system",
    "assert",
    "readfile",
    "file_get_contents",
]

found = False
def is_param_contaminated(data, depth=0):
    global found
    if type(data) is list:
        for i in data:
            is_param_contaminated(i, depth=depth+1)
    elif type(data) is dict:
        if "nodeType" in data.keys():
            node_type = data["nodeType"]
            if node_type == "Expr_FuncCall":
                function_name = data["name"]["parts"][0]
                start_line = data["name"]["attributes"]["startLine"]
                end_line = data["name"]["attributes"]["endLine"]
                print "%s[%s:%d-%d] %s" % (" " * depth, filename, start_line, end_line, str(function_name))
        for k, v in data.items():
            is_param_contaminated(v, depth=depth+1)
    else:
        if str(data) in contaminated_variable:
            print "%s%s" % (" " * depth, str(data))
            found = True

def audit(data, depth=0):
    global found
    if type(data) is list:
        for i in data:
            audit(i, depth=depth+1)
    elif type(data) is dict:
        if "nodeType" in data.keys():
            node_type = data["nodeType"]
            if node_type == "Expr_FuncCall":
                function_name = data["name"]["parts"][0]
                start_line = data["name"]["attributes"]["startLine"]
                end_line = data["name"]["attributes"]["endLine"]
                if function_name in dangerous_function_list:
                    print "[%s:%d-%d] %s" % (filename, start_line, end_line, str(function_name))
                '''
                if str(function_name) in dangerous_function_list:
                    # Start from here
                    print "[%s:%d-%d] %s" % (filename, start_line, end_line, str(function_name))
                    found = False
                    is_param_contaminated(data["args"])
                    # print "contaminated: %s" % (found)
                '''
        # except Exception as e:
        #     exc_type, exc_obj, exc_tb = sys.exc_info()
        #     fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        #     print(exc_type, fname, exc_tb.tb_lineno)
        for k, v in data.items():
            audit(v, depth=depth+1)
    else:
        # print data
        pass

filename = sys.argv[1]

def check():
    os.system("php parser.php %s > data.json" % (filename))
    data = json.load(open("data.json"))
    audit(data)

check()
