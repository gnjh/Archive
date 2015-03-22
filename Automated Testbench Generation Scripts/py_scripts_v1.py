# Created by: NG JIA HAO GARY (U1221954E)                                 #
# NANYANG TECHNOLOGICAL UNIVERSITY - SCE                                  #
# This program generates a testbench file based on a input verilog module #

# importing of the required libraries
import os

def PrintIntroduction():
    print("\niVerilog Automated Script Program Execution")
    print("========================================================================================")
    print("This program takes in verilog module to generate a testbench file for testing purposes. ")
    print("Verilog files to be run should be saved in the folder of directory: C:\iverilog\modules ")
    print("========================================================================================")

def ListFilesFound():
    # Declaring variables
    filesFound = []
    i = 1
    
    print()
    print("List of Verilog Files found to execute:")
    for root, dirs, files in os.walk('C://iverilog/modules/'):
        for file in files:
            if file.endswith('.v') and not file.endswith('tb.v') :
                filesFound = file
                print(str(i) + "." , filesFound)
                i += 1
    print()

# opening of the contents of a verilog file to provide a testbench
raw_input = input("Please enter the name of the verilog file: ")
verilogFilename = raw_input + ".v"
verilogFile = open(verilogFilename, "r")

# providing name for the tb_file to be created
new_filename = raw_input + "_tb.v"

# saving the output file to the specified directoryn
os.chdir("C:\iVerilog\Output")
print("Output File Directory: " + os.getcwd()) 
new_file = open (new_filename, 'w') ## a will append, w will over-write

# providing the content for the file
new_file.write("module " + raw_input + "_tb;\n")

# replacement library
replacements = {'input':'reg', 'output':'wire'}

# Reading the contents of the file
for line in verilogFile: 
    for src, target in replacements.items():
        line = line.replace(src, target)
    new_file.write(line)

new_file.write("\ninitial")
new_file.write("\nbegin")

new_file.write("\nend")
new_file.write("\nendmodule")
# ending the reading task once completed   
verilogFile.close()
# ending the writing task once completed
new_file.close()
print("End of Script...")
