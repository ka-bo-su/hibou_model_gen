"""
model_gen.py ver.1.0.

Copyright 2024 Kazuma Ikesaka.
All rights reserved.
"""

config = {
        "node_type":{
            "action":1,
            "bin_operation":5,
            "un_operation":1
        },
        "bin_operation":{
            "seq":10,
            "struct":10,
            "par":1,
            "alt":1
        },
        "un_operation":{
            "loopS":1
        },
        "life_line":{
            "l1":1,
            "l2":1,
            "l3":1
        },
        "message":{
            "m1":1,
            "m2":1,
            "m3":1
        }
    }

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
        self.select = select()

        
class select:
    def __init__(self):
        global config
        self.config = config

    def node_type(self):
        tmp_action = config["node_type"]["action"]
        tmp_bin_operation = config["node_type"]["bin_operation"]
        tmp_un_operation = config["node_type"]["un_operation"]
        tmp = tmp_action + tmp_bin_operation + tmp_un_operation
        random_number = random.randint(1,tmp)
        if random_number <= tmp_action:
            return "action"
        elif random_number <= tmp_action + tmp_bin_operation:
            return "bin_operation"
        else:
            return "un_operation"
        
    def bin_operation(self):
        tmp_seq = config["bin_operation"]["seq"]
        tmp_struct = config["bin_operation"]["struct"]
        tmp_par = config["bin_operation"]["par"]
        tmp_alt = config["bin_operation"]["alt"]
        tmp = tmp_seq + tmp_struct + tmp_par + tmp_alt
        random_number = random.randint(1,tmp)
        if random_number <= tmp_seq:
            return "seq"
        elif random_number <= tmp_seq + tmp_struct:
            return "struct"
        elif random_number <= tmp_seq + tmp_struct + tmp_par:
            return "par"
        else:
            return "alt"
        
    def un_operation(self):
        tmp_loopS = config["un_operation"]["loopS"]
        tmp = tmp_loopS
        random_number = random.randint(1,tmp)
        if random_number <= tmp_loopS:
            return "loopS"
        
    def life_line(self):
        tmp_l1 = config["life_line"]["l1"]
        tmp_l2 = config["life_line"]["l2"]
        tmp_l3 = config["life_line"]["l3"]
        tmp = tmp_l1 + tmp_l2 + tmp_l3
        random_number = random.randint(1,tmp)
        if random_number <= tmp_l1:
            return "l1"
        elif random_number <= tmp_l1 + tmp_l2:
            return "l2"
        else:
            return "l3"
        
    def message(self):
        tmp_m1 = config["message"]["m1"]
        tmp_m2 = config["message"]["m2"]
        tmp_m3 = config["message"]["m3"]
        tmp = tmp_m1 + tmp_m2 + tmp_m3
        random_number = random.randint(1,tmp)
        if random_number <= tmp_m1:
            return "m1"
        elif random_number <= tmp_m1 + tmp_m2:
            return "m2"
        else:
            return "m3"
