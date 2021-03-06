#!/usr/bin/env python
# Created by: NG JIA HAO GARY (U1221954E)                                 #
# NANYANG TECHNOLOGICAL UNIVERSITY - SCE                                  #
# This program generates a testbench file based on a input verilog module #

# importing of the required libraries
import os
import sys
import re
import random

# timeVariable
time = 10

# Print Introduction 
def PrintIntroduction():
    print("\niVerilog Testbench Generator")
    print("=====================================================================")
    print("This program generate a testbench file for execution purposes.       ")
    print("Files should be saved in C:\iverilog\modules (Win) or \home\ (Linux).")
    print("=====================================================================")

# Print Test Scenarios 
def PrintTestScenario():
    print("\nTest Scenarios Available:")
    print("========================")
    print("1. Random Testing"       )
    print("2. Ascending Order"      )
    print("3. Descending Order"     )
    print("4. Exhaustive Testing"   )
    print()

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

        PrintIntroduction()
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

        PrintIntroduction()
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
            print(moduleDeclaration)

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
            newPortList = []

            # Check if moduleDeclaration contains the variable declaration
            portList = moduleDeclaration.split('(')[1].strip()[:-1]
            if(portList.startswith("input") or portList.startswith("output") ):

                # Module ports are section within brackets, separated by comma
                # Remove whitespace and strip reg from output declaration
                module_ports = moduleDeclaration.split('(')[1].split(')')[0].split(',')
                ports = [a.strip().replace(' reg ',' ').replace(' wire ',' ') for a in module_ports]

                # Remove superfluous spaces in port index
                ports_a = [re.sub(r'\[\s*(\d+)\s*:\s*?(\d+)\s*\]\s*(.)', r'[\1:\2] \3', a) for a in ports]
                #print(str(ports_a))

                for x in ports_a:
                    if x.find("input"):
                        outputVariables.append(x)
                    else:
                        inputVariables.append(x)

                
                print("1. Input Variables: " + str(inputVariables))
                print("1. Output Variables: " + str(outputVariables))
            else:
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

                print("2. Input Variables: " + str(inputVariables))
                print("2. Output Variables: " + str(outputVariables))
            
            # writing the variables
            new_file.write("\n" + ''.join(inputVariables))
            new_file.write("\n" + ''.join(outputVariables))

            # writing the combinational logic
            print("Writing of Combinational Logic .....")
            print("Determine of Test Cases to be used .....")
            
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

            # Assumption: User will always key in integer value
            # Prompt user for test input
            PrintTestScenario()
            i = 4
            startpoint = 0
            inputValue = int(input("Please select a test scenario: "))

            # Check if the input value is within the test range
            while (inputValue > 4 or inputValue <= 0):

                # Print out warning message
                print("Error: Wrong Input Value!")

                # Prompt user to re-input again
                inputValue = int(input("Please select a test scenario: "))
            
            else:
                if inputValue == 1:
                    print("You have selected: Random Testing\n")
                    
                    for x in range (startpoint,i+1):
                        endpoint = (2**bit_width)
                        inputVar = random.randint(startpoint,endpoint)
                        charFormat = '#0' + str(bit_width+2) + 'b'
                        binaryValue = format(inputVar, charFormat)
                        print("Variable: " + assignVariable + ", Assigned Binary Value is: " + str(bit_width) + "'" + str(binaryValue)[1:])
                        new_file.write("\n\t#" + str(time) + " " + assignVariable + " = " + str(bit_width) + "'" + str(binaryValue)[1:] + ";")
                    
                elif inputValue == 2:
                    print("You have selected: Ascending Testing\n")
                    
                    endpoint = (2**bit_width)
                    for x in range (0, endpoint):
                        charFormat = '#0' + str(bit_width+2) + 'b'
                        binaryValue = format(x, charFormat)
                        print("Variable: " + assignVariable + ", Value: " + str(x) + ", Assigned Binary Value is: " + str(bit_width) + "'" + str(binaryValue)[1:])
                        new_file.write("\n\t#" + str(time) + " " + assignVariable + " = " + str(bit_width) + "'" + str(binaryValue)[1:] + ";")
                    
                elif inputValue == 3:
                    print("You have selected: Descending Testing\n")
                    
                    endpoint = (2**bit_width)-1
                    for x in range (endpoint, startpoint-1, -1):
                        charFormat = '#0' + str(bit_width+2) + 'b'
                        binaryValue = format(x, charFormat)
                        print("Variable: " + assignVariable + ", Value: " + str(x) + ", Assigned Binary Value is: " + str(bit_width) + "'" + str(binaryValue)[1:])
                        new_file.write("\n\t#" + str(time) + " " + assignVariable + " = " + str(bit_width) + "'" + str(binaryValue)[1:] + ";")
                    
                elif inputValue == 4:
                    print("You have selected: Exhaustive Testing")
                    print("Exhaustive Testing from 1 to N.......")
                    
                    possibleValue = 2**bit_width-1
                    inputNvalue = int(input("Please enter a N value to test: "))
                    
                    # Check if the input N value will exceed the possible value to be tested
                    while (inputNvalue > 2**bit_width or inputNvalue < 1):
                        if(inputNvalue > 2**bit_width):
                            print("Error! Input value of " + str(inputNvalue) + " exceed the possible test value!")
                        else:
                            print("Error! Input value of " + str(inputNvalue) + " is less than 1!")
                        print("Exhaustive Test from 1 to the max possible value of N will be done instead!")

                        endpoint = (2**bit_width)
                        for x in range (startpoint+1, endpoint):
                            charFormat = '#0' + str(bit_width+2) + 'b'
                            binaryValue = format(x, charFormat)
                            print("Variable: " + assignVariable + ", Value: " + str(x) + ", Assigned Binary Value is: " + str(bit_width) + "'" + str(binaryValue)[1:])
                            new_file.write("\n\t#" + str(time) + " " + assignVariable + " = " + str(bit_width) + "'" + str(binaryValue)[1:] + ";")
                        break
                    else:
                        endpoint = inputNvalue+1
                        for x in range (startpoint, endpoint):
                            charFormat = '#0' + str(bit_width+2) + 'b'
                            binaryValue = format(x, charFormat)
                            print("Variable: " + assignVariable + ", Value: " + str(x) + ", Assigned Binary Value is: " + str(bit_width) + "'" + str(binaryValue)[1:])
                            new_file.write("\n\t#" + str(time) + " " + assignVariable + " = " + str(bit_width) + "'" + str(binaryValue)[1:] + ";")

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
