"""
model_gen.py ver.1.0.

Copyright 2024 Kazuma Ikesaka.
All rights reserved.
"""

BIN_OPERATION = ["seq", "struct", "par", "alt"]
UN_OPERATION = ["loopS"]

life_line = ["l1","l2","l3"]
message = ["m1","m2","m3"]
depth = 7

class node :
    def __init__(self):
        global config
        self.is_action = False
        self.is_bin_operation = False
        self.is_un_operation = False
        self.action = ""
        self.bin_operation = ""
        self.un_operation = ""
        self.next_node1 = None
        self.next_node2 = None
        self.depth = 1