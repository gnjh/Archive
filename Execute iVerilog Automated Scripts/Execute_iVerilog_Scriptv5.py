#!/usr/bin/env python
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
    print("=====================================================================")
    print("This program takes in verilog files to generate a output waveform.   ")
    print("Files should be saved in C:\iverilog\modules (Win) or \home\ (Linux).")
    print("=====================================================================")

# Determine the OS to decide which method to execute
# For Linux Platform - Run using os.system
if sys.platform.startswith('linux'):
    
    # Declaring variables to list files in directory
    filesFound = []
    i = 1
    PrintIntroduction();
    print("List of Verilog Files found to execute:")
    for root, dirs, files in os.walk('/home/'):
        for file in files:
            if file.endswith('.v') and not file.endswith('tb.v'):
                filesFound = file
                print(str(i) + '.' , filesFound)
                i += 1
    print("\n")
    verilogFile    = input("Please enter the name of the verilog file: ")
    verilogTB      = verilogFile.strip() + "_tb"

    executionCommandStr = "iverilog " + verilogFile.strip() + ".v " + verilogTB.strip() + ".v -o " +  verilogTB.strip() + ".vvp"
    generateWaveStr = "\nvvp " + verilogTB.strip() + ".vvp"
    openWaveStr = "\ngtkwave " + verilogTB.strip() + ".dump"
    command = executionCommandStr + generateWaveStr + openWaveStr;
    p = os.system('echo %s|sudo -S %s' % ('',command))
    print(p)
    
# For Windows Platform - Run using .bat file    
if sys.platform.startswith('win'):
    
    PrintIntroduction();
    # Declaring variables to list files in directory
    filesFound = []
    i = 1
    print("List of Verilog Files found to execute:")
    for root, dirs, files in os.walk('C://iverilog/Output/'):
        for file in files:
            if file.endswith('.v') and not file.endswith('tb.v'):
                filesFound.append(file)
                print(str(i) + "." , file)
                i += 1
                
    print("\n")

    # Assumption: User will always key in integer value
        # Prompt user for input
    inputValue = int(input("Please select a file: "))

    # Check if the input value is within the found file range
    while (inputValue > i-1 or inputValue <= 0):
        
        # Print out warning message
        print("Warning: Please select the file again!")
        
        # Prompt user to re-input again
        inputValue = int(input("Please select a file: "))
        
    else:
        # open and read the contents of a verilog file
        verilogFilename = filesFound[inputValue-1][:-2]
        verilogTB      = verilogFilename.strip() + "_tb"
        
        # Creating iVerilog Command to generate batchfile to be executed
        echoOffStr = "echo off\ncls\n"
        setDirectoryStr = "cd c://iverilog/Output/"
        executionCommandStr = "\niverilog " + verilogFilename.strip() + ".v " + verilogTB.strip() + ".v -o " +  verilogTB.strip() + ".vvp"
        generateWaveStr = "\nvvp " + verilogTB.strip() + ".vvp"
        openWaveStr = "\ngtkwave " + verilogTB.strip() + ".dump"
        newBatchStr = echoOffStr + setDirectoryStr + executionCommandStr + generateWaveStr + openWaveStr

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

