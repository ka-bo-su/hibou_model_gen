"""
refactoring.py ver.1.0.

Copyright 2024 Kazuma Ikesaka.
All rights reserved.
"""

######TODO######
# 1. ローカルトレースを作成する関数を作成する。
# 2. ローカルトレースの順番に合わせてプレフィックスをつける関数を作成する。

import random
import sys
from time import sleep
import io
import os
import subprocess
from graphviz import Digraph
import re

DEFORLT_DIR_PATH = "output/test/hibou_para_test_traces/tracegen_hibou_para/"

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.setrecursionlimit(10000)

class node :
    def __init__(self):
        self.is_operation = False
        self.info = []

    def __str__(self):
        string = ""
        if self.is_operation:
            string += self.info[0]
            string += "("
            if len(self.info) > 2:
                for i in range(1, len(self.info)-1):
                    string += self.info[i] + ","
            string += self.info[-1] + ")"
        else:
            for info in self.info:
                string += info
        return string
    
    def __lt__(self, other):
        if not self.is_operation:
            return self.info < other.info
        else:
            return self < other
    
    def __gt__(self, other):
        if not self.is_operation:
            return self.info > other.info
        else:
            return self > other

    def __eq__(self, other):
        if not self.is_operation:
            return self.info == other.info
        else:
            return self == other

    def get_node_info(self):
        tmp = []
        if self.is_operation:
            for i in range(1, len(self.info)):
                tmp.extend(self.info[i].get_node_info())
            return tmp
        return tmp.extend(self.info)
    
    def add_node(self, node):
        self.info.append(node)
    
    def add_operation(self, operation, args):
        self.is_operation = True
        self.info.append(operation)
        tmp = node()
        if len(args) > 2:
            self.info.append(args.pop(0))
            tmp.add_operation(operation, args)
            self.info.append(tmp)
        elif len(args) == 2:
            self.info.append(args.pop(0))
            self.info.append(args.pop(0))
        else:
            self.info.append(args.pop(0))

class tree :
    def __init__(self):
        self.is_leaf = False
        self.node = node()
        self.child = [] 
        self.depth = 0
        self.traces = []
        self.multi_traces = {}

    def __str__(self):
        string = ""
        string = self.node
        for child in self.child:
            string += child.__str__()
        return string
    
    def add_trace_to_tree(self, trace):
        if len(trace) == 0:
            child = tree()
            child.depth = self.depth + 1
            child.node.add_node("leaf")
            self.child.append(child)
        else:
            self.traces.append(trace)
            if self.depth == 0 and self.node.info == []:
                self.node.add_node("root")
            for child in self.child:
                if child.node == trace[0]:
                    child.add_trace_to_tree(trace[1:])
                    return
            child = tree()
            child.depth = self.depth + 1
            child.node = trace[0]
            child.add_trace_to_tree(trace[1:])
            self.child.append(child)

    def add_node_fig(self, fig, node_num_prefix, file_name):
        if self.depth == 0:
            node_num = "0"
            fig.node(node_num, self.node.__str__())
            if len(self.child) > 0:
                for i in range(len(self.child)):
                    self.child[i].add_node_fig(fig, node_num + str(i), file_name)
                    fig.edge(node_num, node_num + str(i))
                fig.render(file_name)
                subprocess.run(["rm", file_name])
        else:
            node_num = node_num_prefix 
            fig.node(node_num, self.node.__str__())
            if len(self.child) > 0:
                for i in range(len(self.child)):
                    self.child[i].add_node_fig(fig, node_num + str(i), file_name)
                    fig.edge(node_num, node_num + str(i))

    def get_n_th_child_node(self, n):
        nodes = []
        if len(self.child) > 0:
            for child in self.child:
                    if child.depth == n:
                        nodes.append(child.node)
                    else:
                        nodes.extend(child.get_n_th_child_node(n))
        return nodes
    
    def get_count_of_child(self):
        cnt_list = []
        depth = 1
        while True:
            cnt_child = len(self.get_n_th_child_node(depth))
            if cnt_child == 0:
                break
            cnt_list.append(cnt_child)
            depth += 1
        cnt_list.pop(-1)
        return cnt_list
    
    def get_length_of_path(self):
        length_list = []
        if len(self.traces) != 0:
            for trace in self.traces:
                length_list.append(len(trace))
        return length_list


def marge_trace(traces): #すべてのトレースは同じ長さと想定
    traces_len = []
    for trace in traces:
        traces_len.append(len(trace))

    for i in range(min(traces_len)):
        if i == 0:
            tmp = traces[0][i]        
        for trace in traces:
            if tmp != trace[i]:
                branch_depth = i
                break
    traces_branch = []
    for trace in traces:
        traces_branch.append(trace[branch_depth-1:])

    traces_content = []
    for i in range(len(traces)):
        tmp = []
        for j in range(traces_len[i]-branch_depth):
            tmp.extend(traces[i][j+branch_depth].get_node_info())
        tmp.sort()
        traces_content.append(tmp)

    for i in range(len(traces_content)):
        if i == 0:
            tmp = traces_content[i]
        if tmp != traces_content[i]:
            print("error")
            exit()
    tmp = tmp[branch_depth-1:branch_depth-1+len(branch_depth)]
    tmp.sort()
    merged_node = node()
    merged_node.add_operation("seq", tmp)
    return traces[0][:branch_depth-1].append(merged_node)

def load_traces(dir_path=DEFORLT_DIR_PATH):
    traces = []
    files_list = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
    for file in files_list:
        file_path = dir_path + file
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                trace_read = f.readlines()
                trace = trace_read[1].split(" ")[1][:-1]
                trace_list = trace.split(".")
                traces.append(trace_list)
    return traces

def create_multi_traces(global_traces):
    multi_traces = {}
    for trace in global_traces:
        multi_trace = {}
        if len(trace) != 1:
            for action in trace:
                action_split = re.split("[?!]", action)
                if action_split[0]  not in multi_trace and action_split[0] != "root" and action_split[0] != "leaf":
                    multi_trace[action_split[0]] = []
                multi_trace[action_split[0]].append(action)
            for key in multi_trace.keys():
                if key  not in multi_traces:
                    multi_traces[key] = []
                if multi_trace[key] not in multi_traces[key]:
                    multi_traces[key].append(multi_trace[key])
    return multi_traces

def add_order_label_to_traces(global_traces, multi_traces):
    key_count = {}
    for trace in global_traces:
        for key in multi_traces.keys():
            key_count[key] = 0
        for i in range(len(trace)):
            action_split = re.split("[?!]", trace[i])
            key_count[action_split[0]] += 1
            # trace[i] = f"{key_count[action_split[0]]}_{trace[i]}"
            if "!" in trace[i]:
                trace[i] = f"{action_split[0]}_{key_count[action_split[0]]}!{action_split[1]}"
            elif "?" in trace[i]:
                trace[i] = f"{action_split[0]}_{key_count[action_split[0]]}?{action_split[1]}"
    return global_traces

def traces_content_to_node(traces):
    traces_with_node = []
    for trace in traces:
        trace_with_node = []
        for action in trace:
            tmp = node()
            tmp.add_node(action)
            trace_with_node.append(tmp)
        traces_with_node.append(trace_with_node)
    return traces_with_node

def setup_traces_from_file(dir_path=DEFORLT_DIR_PATH):
    traces = load_traces(dir_path)
    multi_traces = create_multi_traces(traces)
    traces = add_order_label_to_traces(traces, multi_traces)
    traces = traces_content_to_node(traces)
    return traces

def make_tree_from_traces(traces):
    trace_tree = tree()
    trace_tree_inv = tree()
    graph_image_name = "sample"
    traces.sort()
    for i in range(len(traces)):
            trace_tree.add_trace_to_tree(traces[i])
    trace_tree.add_node_fig(Digraph(format='png'), "0", graph_image_name)
    trace_tree_inv.add_node_fig(Digraph(format='png'), "0", graph_image_name + "_inv")
    return trace_tree

def main():
    traces = setup_traces_from_file()
    trace_tree = make_tree_from_traces(traces)

if __name__ == "__main__":
    main()