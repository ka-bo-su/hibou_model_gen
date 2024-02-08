"""
make_trace_tree.py ver.1.0.

Copyright 2024 Kazuma Ikesaka.
All rights reserved.
"""

import random
import sys
from time import sleep
import io
import os
import subprocess
from graphviz import Digraph
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.setrecursionlimit(10000)

class tree :
    def __init__(self):
        self.is_leaf = False
        self.node = ""
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
            child.node = "leaf"
            self.child.append(child)
        else:
            self.traces.append(trace)
            if self.depth == 0:
                self.node = "root"
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
        flg = False
        if file_name == "sample_merged":
            flg = True
        if self.depth == 0:
            if flg:
                print("====================================")
            node_num = "0"
            fig.node(node_num, self.node)
            if len(self.child) > 0:
                for i in range(len(self.child)):
                    self.child[i].add_node_fig(fig, node_num + str(i), file_name)
                    fig.edge(node_num, node_num + str(i))
                fig.render(file_name)
                subprocess.run(["rm", file_name])
        else:
            node_num = node_num_prefix 
            fig.node(node_num, self.node)
            if flg:
                print("====================================")
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
    
    def get_length_of_path(self): #same in lengeth of traces
        length_list = []
        if len(self.traces) != 0:
            for trace in self.traces:
                length_list.append(len(trace))
        return length_list

    # def remove_n_th_child(self, n):
    #     for i in range(n, len(self.child)-1):
    #         self.child[i] = self.child[i+1]
    #     self.child.pop(n)

    def create_multi_traces(self):
        if len(self.traces) != 0:
            for trace in self.traces:
                multi_trace = {}
                if len(trace) != 1:
                    for action in trace:
                        action_split = re.split("[?!]", action)
                        if action_split[0]  not in multi_trace and action_split[0] != "root" and action_split[0] != "leaf":
                            multi_trace[action_split[0]] = []
                        multi_trace[action_split[0]].append(action)
                    for key in multi_trace.keys():
                        if key  not in self.multi_traces:
                            self.multi_traces[key] = []
                        self.multi_traces[key].append(multi_trace[key])

    def some_funtion(self):
        similarlity = []
        same_depth = []
        for i in range(len(self.traces)):
            trace_A = self.traces[i]
            similarlity_list = []
            for j in range(len(self.traces)):
                trace_B = self.traces[j]
                loop_len = min(len(trace_A), len(trace_B))
                for k in range(loop_len):
                    if trace_A[k] != trace_B[k]:
                        k -= 1
                        break
                if k+1 == len(trace_A):
                    similarlity_list.append(-1)
                elif i<j:
                    similarlity_list.append(k+1)
                    if k+1 not in same_depth:
                        same_depth.append(k+1)
                else:
                    similarlity_list.append(0)
            similarlity.append(similarlity_list)
        same_depth.sort(reverse=True)
        if len(same_depth) == 0:
            print("トレースが一個しかない")
            return
        depth = max(same_depth)
        remove_list = []
        for i in range(len(similarlity)):
            tmp = []
            tmp.append(self.traces[i])
            for j in range(len(similarlity[i])):
                if similarlity[i][j] == depth:
                    tmp.append(self.traces[j])
                    # self.traces.pop(j)
                    if i not in remove_list:
                        remove_list.append(i)
                    if j not in remove_list:
                        remove_list.append(j)
            if len(tmp) > 1:
                merge = marge_trace(tmp)
                self.traces.append(merge)
        remove_list.sort(reverse=True)
        for i in remove_list:
            self.traces.pop(i)
        traces_tmp = self.traces
        traces_tmp.sort()
        self.__init__()
        for i in range(len(traces_tmp)):
            self.add_trace_to_tree(traces_tmp[i])
        return traces_tmp


    def make_tree_from_exist_traces(self):
        graph_image_name = "sample_seq"
        self.traces.sort()
        # for i in range(len(self.traces)):
        #     self.add_trace_to_tree(self.traces[i])
        G = Digraph(format='png')
        trace_tree.add_node_fig(G, "0", graph_image_name)
        return trace_tree


def marge_trace(traces): #すべてのトレースは同じ長さと想定
    tmp = []
    tmp2 = []
    for i in range(len(traces[0])):
        tmp.append([])
    for i in range(len(traces)):
        for j in range(len(traces[i])):
            if traces[i][j] not in tmp[j]:
                tmp[j].append(traces[i][j])
    i = 0
    while i < len(tmp):
        if len(tmp[i]) > 1:
            if sorted(tmp[i]) not in tmp2:
                tmp2.append(tmp[i])
        if len(tmp[i]) == 1 and len(tmp2)>0:
            ans = traces[0][:i-len(tmp2)-1]
            tmp2 = strict_to_seq(tmp2)
            ans.append(tmp2)
            ans.extend(traces[0][i:])
            tmp2 = []
        i += 1
    return ans

def strict_to_seq(trace_a): #現状は構成要素は同じと仮定（altは考えない）
    ans = "seq"
    for i in trace_a:
        ans += str(i)
    return ans

def make_tree_from_traces():
    trace_tree = tree()
    trace_tree_inv = tree()
    traces = []
    traces_inv = []
    dir_path = "output/test/hibou_para_test_traces/tracegen_hibou_para/"
    graph_image_name = "sample"
    files_list = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
    for file in files_list:
        file_path = dir_path + file
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                trace_read = f.readlines()
                trace = trace_read[1].split(" ")[1][:-1]
                trace_list = trace.split(".")
                trace_list_inv = list(reversed(trace_list))
                traces.append(trace_list)
                traces_inv.append(trace_list_inv)
    traces.sort()
    traces_inv.sort()
    for i in range(len(traces)):
            trace_tree.add_trace_to_tree(traces[i])
            trace_tree_inv.add_trace_to_tree(traces_inv[i])
    trace_tree.add_node_fig(Digraph(format='png'), "0", graph_image_name)
    trace_tree_inv.add_node_fig(Digraph(format='png'), "0", graph_image_name + "_inv")
    return trace_tree

def make_tree_from_trace_list(traces):
    trace_tree = tree()
    graph_image_name = "sample"
    traces.sort()
    for i in traces:
        print(i)
    for i in range(len(traces)):
            trace_tree.add_trace_to_tree(traces[i])
    print(trace_tree)
    trace_tree.add_node_fig(Digraph(format='png'), "0", graph_image_name+"_merged")
    return trace_tree



if __name__ == "__main__":
    trace_tree = make_tree_from_traces()
    merged_trace_list = trace_tree.some_funtion()
    merged_trace = make_tree_from_trace_list(merged_trace_list)
    # print("---------------------------")
    # print(len(trace_tree.traces))
    # for i in trace_tree.traces:
    #     print(i)
    # print("---------------------------")
    # trace_tree.make_tree_from_exist_traces()
    # trace_tree.some_funtion()
    # print("---------------------------")
    # print(len(trace_tree.traces))
    # for i in trace_tree.traces:
    #     print(i)
    # print("---------------------------")
    # trace_tree.make_tree_from_exist_traces()
    # trace_tree.create_multi_traces()
