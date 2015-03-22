#!/usr/bin/env python
# Created by: NG JIA HAO GARY (U1221954E)                                 #
# NANYANG TECHNOLOGICAL UNIVERSITY - SCE                                  #
# This program generates a testbench file based on a input verilog module #

# importing of the required libraries
import os
import sys
import re
import random

# Print Introduction 
def PrintIntroduction():
    print("\niVerilog Testbench Generator")
    print("=====================================================================")
    print("This program generate a testbench file for execution purposes.       ")
    print("Files should be saved in C:\iverilog\modules (Win) or \home\ (Linux).")
    print("=====================================================================")

# removing the comments in the modules of the verilog file 
def removeComments(textInput):
    def reConstruct(match):
        i = match.group()
        if i.startswith('/'):
            return ""
        else:
            return i
    pattern = re.compile(r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"'
                         , re.DOTALL | re.MULTILINE)
    return re.sub(pattern, reConstruct, textInput)

# Determine the OS to decide which method to execute
# For Linux Platform - Run using os.system
if sys.platform.startswith('linux'):

    # Infinite loop
    while (1):
        
        # Declaring variables to list files in directory
        filesFound = []
        listFile = []
        i = 1
        print("List of Verilog Files found to execute:")
        for root, dirs, files in os.walk('/home/'):
            for file in files:
                if file.endswith('.v') and not file.endswith('tb.v'):
                    listFile = file
                    filesFound.append(file)
                    print(str(i) + '.' , filesFound)
                    i += 1
        print("\n")

        # Assumption: User will always key in integer value
        # Prompt user for input
        inputValue = int(raw_input("Please select a file: "))

        # Check if the input value is within the found file range
        while (inputValue > i-1 or inputValue <= 0):
            
            # Print out warning message
            print("Warning: Please select the file again!")
            
            # Prompt user to re-input again
            inputValue = int(raw_input("Please select a file: "))
            
        else:
            
            # open and read the contents of a verilog file
            verilogFilename = filesFound[inputValue-1]
            verilogFile = open(verilogFilename)
            print("Opening file: " + verilogFilename)
            moduleContents = verilogFile.read()
            print("Reading Contents of the file - Completed!")

            # the output file would now be free from any comments
            output_noComments = removeComments(moduleContents)
            print("Removing Comments in File - Completed!")

            # extract module declaration as section between module keyword and semicolon
            moduleDeclaration = output_noComments.split('module')[1].split(';')[0]
            print("Extracting Module Declaration - Completed!")

            # extract module name
            module_name = moduleDeclaration.split('(')[0].strip()
            print("Extracting Module Name - Completed!")

            # creating output verilog file at the specified directory
            new_tbFileName = module_name + "_tb.v"
            new_file = open(new_tbFileName, 'w') ## a will append, w will over-write
            print("\nCreating output file .....")

            # writing the testbench block
            new_file.write("module " + module_name + "_tb;\n")
            print("Writing testbench blocks .....")

            # replacing the variables: input to reg, output to wire
            inputVariables = []
            outputVariables = []

            with open(verilogFilename, 'r') as fileopen:
               fileList = [line.strip() for line in fileopen]

            # renaming the variables; input to reg, output to wire
            for line in fileList:
                if line.startswith("input"):
                    line = line.replace("input", "reg")
                    inputVariables.append(line)
                    pass
                if line.startswith("output"):
                    line = line.replace("output", "wire")
                    outputVariables.append(line)
                    break

            # writing the variables
            new_file.write("\n" + ''.join(inputVariables))
            new_file.write("\n" + ''.join(outputVariables))

             # timeVariable
            time = 50

            # writing the combinational logic
            print("Writing of Combinational Logic .....")
            new_file.write("\n\ninitial")
            new_file.write("\nbegin")
            new_file.write("\n\t$dumpfile(\"" + module_name + "_tb.dump" + "\"" + ");")
            new_file.write("\n\t$dumpvars;")

            # Replacing the ';' to ''
            module_ports = []
            fileList = inputVariables 
            for line in fileList:
                if line.endswith(';'):
                    line = line.replace(';','')
                    module_ports.append(line)
                    
            # Obtaining the width, MSB index, LSB index of the variables
            for a in module_ports:
               a_split = a.split()
               assignVariable = a_split[2]

               # Assigning values to the variables
               for a_split[2] in inputVariables:
                   if any(a_split[2] in x for x in inputVariables):
                       if(a_split[1].endswith(']') == True):
                           # Extract two numbers separated by colon surrounded by square brackets
                           bits = [int(x) for x in a_split[1].split('[')[1].split(']')[0].split(':')]
                           bit_width = abs(bits[0]-bits[1])+1
                       else:
                           bit_width = 1
                               
               for x in range (0,2):
                   startpoint = 0
                   endpoint = (2**bit_width)-1
                   inputVar = random.randint(startpoint,endpoint)
                   charFormat = '#0' + str(bit_width+2) + 'b'
                   binaryValue = format(inputVar, charFormat)
                   #print(assignVariable + " Bit width is : " + str(bit_width) + " Value is : " +  str(inputVar) + "  Binary Value is: " + str(bit_width) + "'" + str(binaryValue)[1:])
                   new_file.write("\n\t#" + str(time) + " " + assignVariable + " = " + str(bit_width) + "'" + str(binaryValue)[1:] + ";")
                   #new_file.write("\n" + assignVariable + " = " + str(bit_width) + "'" + str(binaryValue)[1:] + ";")

            new_file.write("\n\t#" + str(time) + " $finish;")
            new_file.write("\nend")
            new_file.write("\n\n" + module_name + " " + module_name[0] + " " + output_noComments.split(module_name)[1].split(';')[0] + ";")
            new_file.write("\n\nendmodule")
            print("Writing of Combinational Logic - Completed!")

            # ending the writing task once completed
            new_file.close()
            print("Writing of output file completed!")
            print("\n")

            # ending the writing task once completed
            new_file.close()
            break # Run once and stop
            #pass - Run infinitely

#-------------------------------------------------------------------------#

# For Windows Platform - Run using .bat file    
if sys.platform.startswith('win'):

    # Infinite loop
    while (1):
    
        # Declaring variables to list files in directory
        filesFound = []
        listFile = []
        i = 1
        print("List of Verilog Files found:")
        for root, dirs, files in os.walk('C://iverilog/modules/'):
            for file in files:
                if file.endswith('.v') and not file.endswith('tb.v'):
                    listFile = file
                    filesFound.append(file)
                    print(str(i) + '.' , listFile)
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
            os.chdir("C://iverilog/modules/")
            verilogFilename = filesFound[inputValue-1]
            verilogFile = open(verilogFilename)
            print("Opening file: " + verilogFilename)
            moduleContents = verilogFile.read()
            print("Reading Contents of the file - Completed!")
            
            # the output file would now be free from any comments
            output_noComments = removeComments(moduleContents)
            print("Removing Comments in File - Completed!")

            # extract module declaration as section between module keyword and semicolon
            moduleDeclaration = output_noComments.split('module')[1].split(';')[0]
            print("Extracting Module Declaration - Completed!")

            # extract module name
            module_name = moduleDeclaration.split('(')[0].strip()
            print("Extracting Module Name - Completed!")

            # creating output verilog file at the specified directory
            os.chdir("C:\iVerilog\Output")
            new_tbFileName = module_name + "_tb.v"
            new_file = open(new_tbFileName, 'w') ## a will append, w will over-write
            print("\nCreating output file .....")

            # writing the testbench block
            new_file.write("module " + module_name + "_tb;\n")
            print("Writing testbench blocks .....")

            # replacing the variables: input to reg, output to wire
            inputVariables = []
            outputVariables = []

            os.chdir("C://iverilog/modules/")
            with open(verilogFilename, 'r') as fileopen:
               fileList = [line.strip() for line in fileopen]

            # renaming the variables; input to reg, output to wire
            for line in fileList:
                if line.startswith("input"):
                    line = line.replace("input", "reg")
                    inputVariables.append(line)
                    pass
                if line.startswith("output"):
                    line = line.replace("output", "wire")
                    outputVariables.append(line)
                    break

            # writing the variables
            new_file.write("\n" + ''.join(inputVariables))
            new_file.write("\n" + ''.join(outputVariables))

             # timeVariable
            time = 50

            # writing the combinational logic
            print("Writing of Combinational Logic .....")
            
            new_file.write("\n\ninitial")
            new_file.write("\nbegin")
            new_file.write("\n\t$dumpfile(\"" + module_name + "_tb.dump" + "\"" + ");")
            new_file.write("\n\t$dumpvars;")

            # Replacing the ';' to ''
            module_ports = []
            fileList = inputVariables 
            for line in fileList:
                if line.endswith(';'):
                    line = line.replace(';','')
                    module_ports.append(line)
                    
            # Obtaining the width, MSB index, LSB index of the variables
            for a in module_ports:
               a_split = a.split()
               assignVariable = a_split[2]

               # Assigning values to the variables
               for a_split[2] in inputVariables:
                   if any(a_split[2] in x for x in inputVariables):
                       if(a_split[1].endswith(']') == True):
                           # Extract two numbers separated by colon surrounded by square brackets
                           bits = [int(x) for x in a_split[1].split('[')[1].split(']')[0].split(':')]
                           bit_width = abs(bits[0]-bits[1])+1
                       else:
                           bit_width = 1
                               
               for x in range (0,2):
                   startpoint = 0
                   endpoint = (2**bit_width)-1
                   inputVar = random.randint(startpoint,endpoint)
                   charFormat = '#0' + str(bit_width+2) + 'b'
                   binaryValue = format(inputVar, charFormat)
                   #print(assignVariable + " Bit width is : " + str(bit_width) + " Value is : " +  str(inputVar) + "  Binary Value is: " + str(bit_width) + "'" + str(binaryValue)[1:])
                   new_file.write("\n\t#" + str(time) + " " + assignVariable + " = " + str(bit_width) + "'" + str(binaryValue)[1:] + ";")
                   #new_file.write("\n" + assignVariable + " = " + str(bit_width) + "'" + str(binaryValue)[1:] + ";")

            new_file.write("\n\t#" + str(time) + " $finish;")
            new_file.write("\nend")
            new_file.write("\n\n" + module_name + " " + module_name[0] + " " + output_noComments.split(module_name)[1].split(';')[0] + ";")
            new_file.write("\n\nendmodule")
            print("Writing of Combinational Logic - Completed!")

            # ending the writing task once completed
            new_file.close()
            print("Writing of output file completed!")
            os.chdir("C:\iVerilog\Output")
            print("Output File Directory: " + os.getcwd())
            print("\n")
            break # Run once and stop
            #pass - Run infinitely
