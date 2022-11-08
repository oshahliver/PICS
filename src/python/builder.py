#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 17:51:31 2021

@author: os18o068
"""

import numpy.f2py
import argparse
import sys
import os
import subprocess
import time

parser = argparse.ArgumentParser(description="Build fortplanet.")

parser.add_argument('-fcheck', type=bool, default=False, help="If true, fcheck is turned on. This option is used for debugging.")
parser.add_argument('-fbacktrace', type=bool, default=False, help="If true, fbacktrace is turned on. This optino is used for debugging.")
parser.add_argument('-fPIC', type=bool, default=True, help="If true, position independant code is generated. Use this for linking shared libraries.")
parser.add_argument('-entry', type=int, default=0, help="Specifies the entry point for the compilation. This can be used if not all libraries have to be re-compiled")

args = parser.parse_args()
args_dict = vars(args)

#pre-defined argument options for compiler flags
flags = ['-fcheck=all', 
'-fbacktrace', 
'-fpic']

#pre-defined hirarchy of the modules that need to be linked
mods = ["run_params",
"constants", 
"LinAlg",
"class_table_new",
"phase",
"my_types", 
"eosfort", 
"functions", 
"eosmat", 
"fortshell", 
"fortlayer", 
"fortplanet"]

#file name of the main routine
main = "eosfort_wrapper"
exe = "fortfunctions"

mod_command = ["gfortran", "-Og", "-c"]
main_command = ["python3", "-m", "numpy.f2py", "--opt='-O3'", "--f90flags='-Wtabs'"]

for mod in mods:
  main_command.append(mod+".o")

main_command.append("-c")
main_command.append(main+".f95")
main_command.append("-m")
main_command.append(exe)

arg_count = 0
for arg in args_dict:
  #Only the first three arguments contain specifications for compiler flags
  #The subsequent arguments must be omitted in the final command
  if arg_count == 3:
    break
  if args_dict[arg]:
    mod_command.append(flags[arg_count])

  else:
     pass
  arg_count += 1

t0 = time.time()

print ("building shared libraries...")
for mod in mods:
  mod_command.append(mod+'.f95')
  print ('executing:', mod_command)
  subprocess.call(mod_command)
  mod_command.pop(-1)

print ("building main...")

print ("executing:", main_command)

subprocess.call(main_command)

print ("Complete")

t=time.time()

print ('Elapsed time for compilation: ', round((t-t0),3), 'sec')