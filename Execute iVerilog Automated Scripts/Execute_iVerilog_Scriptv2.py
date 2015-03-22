# Created by: NG JIA HAO GARY (U1221954E)                                       #
# NANYANG TECHNOLOGICAL UNIVERSITY - SCE                                        #
# This program automate the process to generate a waveform using iVerilog tools #

# importing of the required libraries
import os
import sys
import subprocess
import textwrap

def PrintIntroduction():
    print("\niVerilog Automated Script Program Execution")
    print("========================================================================================")
    print("This program takes in verilog module and testbench to generate a output waveform file.  ")
    print("Verilog files to be run should be saved in the folder of directory: C:\iverilog\modules ")
    print("========================================================================================")

# Prompt the user for input
PrintIntroduction()
verilogFile    = input("Please enter the name of the verilog file: ")
verilogTB      = verilogFile.strip() + "_tb"

# Creating iVerilog Command to generate batchfile to be executed
echoOffStr = "echo off\ncls\n"
setDirectoryStr = "cd c://iverilog/modules/"
executionCommandStr = "\niverilog " + verilogFile.strip() + ".v " + verilogTB.strip() + ".v -o " +  verilogTB.strip() + ".vvp"
generateWaveStr = "\nvvp " + verilogTB.strip() + ".vvp"
openWaveStr = "\ngtkwave " + verilogTB.strip() + ".dump"
newBatchStr = echoOffStr + setDirectoryStr + executionCommandStr + generateWaveStr + openWaveStr

# Determine the OS to decide which method to execute
# For Linux Platform - Run using subprocess.Popen
if sys.platform == 'linux':
    linuxBatchStr = executionCommandStr + generateWaveStr + openWaveStr
    output = subprocess.Popen(['sudo', linuxBatchStr])
    print(output)
    
# For Windows Platform - Run using .bat file    
if sys.platform == 'win32':
    # create a batch file with some commands in it
    batch_filename = 'commands.bat'
    with open(batch_filename, "wt") as batchfile:
          batchfile.write(textwrap.dedent(newBatchStr))

    # execute the batch file as a separate process and echo its output
    dictionary = dict(stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                  universal_newlines=True)
    with subprocess.Popen(batch_filename, **dictionary).stdout as output:
        for line in output:
            print(line)

    # clean up/ removing the batch file created
    try: os.remove(batch_filename)
    
    # ignore if there is any OS error
    except os.error: pass

else:
    print("Error: This script is not support in this OS. =(")
    print("Please use either Windows or Linux to run the script!")
