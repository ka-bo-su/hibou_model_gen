"""
make_model_traces.py ver.1.0.

Copyright 2024 Kazuma Ikesaka.
All rights reserved.
"""
import sys
import subprocess
import os

args = sys.argv

subprocess.run(["python3", "model_gen.py"])
if not os.path.exists(args[1]):
    subprocess.run(["mkdir", args[1]])
hif_file = args[1] + "/hibou_para_" + args[1] + ".hif"
image_dir = args[1] + "/hibou_para_" + args[1] + "_images"
trace_dir = args[1] + "/hibou_para_" + args[1] + "_traces"

subprocess.run(["mv", "hibou_para.hif", hif_file])
subprocess.run(["./hibou_label.exe", "explore", "hibou_para.hsf", hif_file, "hibou_para.hcf"])
if os.path.exists(trace_dir):
    subprocess.run(["rm", "-r", trace_dir])
subprocess.run(["mv", "tracegen_hibou_para", trace_dir])
if not os.path.exists(image_dir):
    subprocess.run(["mkdir", image_dir])
subprocess.run(["./hibou_label.exe", "draw", "-r", "sd", "hibou_para.hsf", hif_file])
subprocess.run(["mv", "hibou_para_" + args[1] + "_repr.png", image_dir+"/hibou_para_" + args[1] + "_sd.png"])
subprocess.run(["./hibou_label.exe", "draw", "-r", "tt", "hibou_para.hsf", hif_file])
subprocess.run(["mv", "hibou_para_" + args[1] + "_repr.png", image_dir+"/hibou_para_" + args[1] + "_tt.png"])

subprocess.run(["rm", "-r", "temp"])
