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
    print("\nTest Scenarios Available:"          )
    print("=====================================")
    print("1. Random Testing"                    )
    print("2. Ascending Exhaustive Testing"      )
    print("3. Descending Exhaustive Testing"     )
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

            # extract module declaration as section between module keyword and semicolon
            moduleDeclaration = output_noComments.split('module')[1].split(';')[0]
            
            # extract module name
            module_name = moduleDeclaration.split('(')[0].strip()

            # creating output verilog file at the specified directory
            os.chdir("C:\iVerilog\Output")
            new_tbFileName = module_name + "_tb.v"
            new_file = open(new_tbFileName, 'w') ## a will append, w will over-write

            # writing the testbench block
            new_file.write("module " + module_name + "_tb;\n")

            # replacing the variables: input to reg, output to wire
            inputVariables_dict = dict()
            outputVariables_dict = dict()
            listofVariables = []

            # Check if moduleDeclaration contains the variable declaration
            portList = moduleDeclaration.split('(')[1].strip()[:-1]
            if(portList.startswith("input") or portList.startswith("output") ):

                print("Removing Comments in File - Completed!")
                print("Extracting Module Name - Completed!")
                print("\nCreating output file .....")
                print("Writing testbench blocks .....")

                # Removing the comma and replacing it with ' '
                for newPortList in portList:
                    newPortList = portList.replace(',','')
                newPortList = newPortList.split()

                # Looping through the moduleDeclaration to extract the data
                for x in range(len(newPortList)):
                    if newPortList[x] == "input":
                        typeOfVariable = newPortList[x]
                        if(newPortList[x+1].startswith('[') == True):
                            bitPort = newPortList[x+1]
                            
                            # Extract two numbers separated by colon surrounded by square brackets
                            bits = [int(x) for x in newPortList[1].split('[')[1].split(']')[0].split(':')]
                            bit_width = abs(bits[0]-bits[1])+1
                        else:
                            bit_width = 1
                            bitPort = ''
                    elif newPortList[x] == "output":
                        typeOfVariable = newPortList[x]
                        if(newPortList[x+1].startswith('[') == True):
                            bitPort = newPortList[x+1]
                            
                            # Extract two numbers separated by colon surrounded by square brackets
                            bits = [int(x) for x in newPortList[1].split('[')[1].split(']')[0].split(':')]
                            bit_width = abs(bits[0]-bits[1])+1
                        else:
                            bit_width = 1
                    elif (newPortList[x].startswith('[') == False):
                        
                        # Extract variables without the keywords or bitwidth
                        value = newPortList[x]
                        # writing the variables
                        # renaming the variables; input to reg, output to wire
                        if(typeOfVariable == "input"):
                            new_file.write(str("\nreg " + str(bitPort) + " " + value + ";"))
                            print(str("Input Variables: reg " + str(bitPort) + " " + value + ";"))
                            listofVariables.append(value)
                            
                        else:
                            new_file.write(str("\nwire " + str(bitPort) + " " + value + ";"))
                            print(str("Output Variables: wire " + str(bitPort) + " " + value + ";"))
                            listofVariables.append(value)
                        
                        # Sorting the variables respecting into input and output 
                        if (typeOfVariable == "input"):
                            inputVariables_dict[value] = bit_width
                        else:
                            outputVariables_dict[value] = bit_width
                            
                # Sorting the variables based on their bits width 
                flipped = {}
                for key, value in inputVariables_dict.items():
                    if value not in flipped:
                        flipped[value] = [key]
                    else:
                        flipped[value].append(key)                    

            else:
                # reject all unsupported format error message
                print("\nError: File format not supported by the script!")
                print("This script only accept the following format:\n")
                print("module exampleFormat(input [3:0] A, B, input C, output [3:0] D);")
                print("\t// mix up the input bits")
                print("\tassign B = { A[0], A[2], A[1], A[3] };")
                print("endmodule")
                break;
               

            # writing the combinational logic
            print("Writing of Combinational Logic .....")
            print("Determine of Test Cases to be used .....")
            
            new_file.write("\n\ninitial")
            new_file.write("\nbegin")
            new_file.write("\n\t$dumpfile(\"" + module_name + "_tb.dump" + "\"" + ");")
            new_file.write("\n\t$dumpvars;")

            # Assumption: User will always key in integer value
            # Prompt user for test input
            PrintTestScenario()
            i = 3
            startpoint = 0
            inputValue = int(input("Please select a test scenario: "))

            # Check if the input value is within the test range
            while (inputValue > i or inputValue <= 0):

                # Print out warning message
                print("Error: Wrong Input Value!")

                # Prompt user to re-input again
                inputValue = int(input("Please select a test scenario: "))
            
            else:
                if inputValue == 1:
                    print("You have selected: Random Testing\n")
                    for x in flipped.keys():
                        assignVariable = flipped[x]
                        bit_width = x
                        
                        for x in range (startpoint,i+1):
                            endpoint = (2**bit_width-1)
                            inputVar = random.randint(startpoint,endpoint)
                            charFormat = '#0' + str(bit_width+2) + 'b'
                            binaryValue = format(inputVar, charFormat)
                            
                            print("Variable: " + ','.join(map(str, assignVariable)) + ", Assigned Binary Value is: " + str(bit_width) + "'" + str(binaryValue)[1:])
                            new_file.write("\n\t#" + str(time) + " assign {" + ','.join(map(str, assignVariable)) + "} = " + str(bit_width) + "'" + str(binaryValue)[1:] + ";")         
                        
                elif inputValue == 2:
                    print("You have selected: Ascending Exhaustive Testing\n")
                    print("Exhaustive Testing from 0 to N.......")
                    for x in flipped.keys():
                        assignVariable = flipped[x]
                        bit_width = x                      
                        possibleValue = 2**bit_width-1
                        inputNvalue = int(input("Please enter a N value to test: "))
                        
                        # Check if the input N value will exceed the possible value to be tested
                        while (inputNvalue > 2**bit_width or inputNvalue < 1):
                            if(inputNvalue > 2**bit_width):
                                print("Error! Input value of " + str(inputNvalue) + " exceed the possible test value!")
                            else:
                                print("Error! Input value of " + str(inputNvalue) + " is less than 1!")
                            print("Ascending Exhaustive Test from 0 to the max possible value of N will be done instead!")

                            endpoint = (2**bit_width)
                            for x in range (startpoint, endpoint):
                                charFormat = '#0' + str(bit_width+2) + 'b'
                                binaryValue = format(x, charFormat)
                                print("Variable: " + ','.join(map(str, assignVariable)) + ", Assigned Binary Value is: " + str(bit_width) + "'" + str(binaryValue)[1:])
                                new_file.write("\n\t#" + str(time) + " assign {" + ', '.join(map(str, assignVariable)) + "} = " + str(bit_width) + "'" + str(binaryValue)[1:] + ";")                                   
                            break
                        else:
                            endpoint = inputNvalue
                            for x in range (startpoint, endpoint):
                                charFormat = '#0' + str(bit_width+2) + 'b'
                                binaryValue = format(x, charFormat)
                                print("Variable: " + ','.join(map(str, assignVariable)) + ", Assigned Binary Value is: " + str(bit_width) + "'" + str(binaryValue)[1:])
                                new_file.write("\n\t#" + str(time) + " assign {" + ', '.join(map(str, assignVariable)) + "} = " + str(bit_width) + "'" + str(binaryValue)[1:] + ";")         

                elif inputValue == 3:
                    print("You have selected: Descending Exhaustive Testing\n")
                    print("Exhaustive Testing from 0 to N.......")
                    for x in flipped.keys():
                        assignVariable = flipped[x]
                        bit_width = x                      
                        possibleValue = 2**bit_width-1
                        inputNvalue = int(input("Please enter a N value to test: "))
                        
                        # Check if the input N value will exceed the possible value to be tested
                        while (inputNvalue > 2**bit_width or inputNvalue < 1):
                            if(inputNvalue > possibleValue):
                                print("Error! Input value of " + str(inputNvalue) + " exceed the possible test value!")
                            else:
                                print("Error! Input value of " + str(inputNvalue) + " is less than 1!")
                            print("Descending Exhaustive Test from the max possible value N to 0 will be done instead!")

                            endpoint = possibleValue
                            for x in range (endpoint, startpoint-1, -1):
                                charFormat = '#0' + str(bit_width+2) + 'b'
                                binaryValue = format(x, charFormat)
                                print("Variable: " + ','.join(map(str, assignVariable)) + ", Assigned Binary Value is: " + str(bit_width) + "'" + str(binaryValue)[1:])
                                new_file.write("\n\t#" + str(time) + " assign {" + ', '.join(map(str, assignVariable)) + "} = " + str(bit_width) + "'" + str(binaryValue)[1:] + ";")                                   
                            break
                        else:
                            endpoint = inputNvalue
                            for x in range (endpoint-1, startpoint-1, -1):
                                charFormat = '#0' + str(bit_width+2) + 'b'
                                binaryValue = format(x, charFormat)
                                print("Variable: " + ','.join(map(str, assignVariable)) + ", Assigned Binary Value is: " + str(bit_width) + "'" + str(binaryValue)[1:])
                                new_file.write("\n\t#" + str(time) + " assign {" + ', '.join(map(str, assignVariable)) + "} = " + str(bit_width) + "'" + str(binaryValue)[1:] + ";")         
                            
            new_file.write("\n\t#" + str(time) + " $finish;")
            new_file.write("\nend")
            new_file.write("\n\n" + module_name + " " + module_name[0] + " (" + ', '.join(map(str, listofVariables)) + ");")
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
