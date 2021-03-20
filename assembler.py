import os
import sys

addressLength = None
ERROR_COUNT = 0

def isAddress(val):
    for letter in val:
        if not letter.isdigit():
            return 0
    return 1

def initData():
    global addressLength
    global ERROR_COUNT
    """Function that initializes declared data"""
    lineNumber = 0 # Initialize line number for data memory addressing
    line = inputFile.readline()
    addressLength = len(line.split()[3])
    
    # Loop until line is a terminating instruction
    while not line.startswith('+9'):
        # Tokenize data part line
        tokens = line.split()

        # Verify if opcode is Valid
        if tokens[0] != "DEC" : 
            errors.append(f'ERROR: {tokens[0]} INVALID OPCODE AT LINE >> {tokens[0]} {tokens[1]} {tokens[2]} {tokens[3]}')
            ERROR_COUNT+=1
            
        # Replace symbols with their according address
        symbols[tokens[1]] = str(lineNumber).zfill(addressLength)

        # Get the number of words to print to output file
        words = int(tokens[2])

        # Scan the next line which contains an integer value and write it out
        line = inputFile.readline()
        
        # Write the value to the output file or as many words as there are
        for _ in range(0,words):
            intermFile.write(line.replace(' ', ''))

        # Scan next line
        line = inputFile.readline()

        # Increment line number
        lineNumber += 1
    
    # Write the terminating instruction
    intermFile.write(line.replace(' ', ''))


def initProgram():
    global ERROR_COUNT
    """Function that reads the program"""
    lineNumber = 0 # For program memory addressing
    line = inputFile.readline() # Read first data line

    # Loop until line is a terminating instruction
    while not line.startswith('+9'):
        # Tokenize the line
        tokens = line.split()

        # Check for invalid opcode
        temp = switcher.get(tokens[0],None)
        
        if temp != None: 
            # If opcode is valid meaning the opcode was found in the switcher
            tokens[0] = temp
        else: 
            # Opcode is invalid, print error prompt
            errors.append(f'ERROR: {tokens[0]} INVALID OPCODE AT LINE >> {tokens[0]} {tokens[1]} {tokens[2]} {tokens[3]}')
            ERROR_COUNT+=1
        
        if tokens[0] == '-7':
            labels[tokens[1]] = str(lineNumber).zfill(addressLength)
            tokens[1] = str(lineNumber).zfill(addressLength)
        else:
            # Check if operands 1 and 2 are symbols, if yes then swap with their addresses
            for i in range(1,3):
                temp = symbols.get(tokens[i],None)
                if temp is not None:
                    tokens[i] = temp
                elif isAddress(tokens[i]):
                    # Do nothing cause it's a valid address
                    pass
                else:
                    errors.append(f'SYMBOL ERROR: {tokens[i]} DOES NOT EXIST AT LINE >> {tokens[0]} {tokens[1]} {tokens[2]} {tokens[3]}')
                    ERROR_COUNT+=1
                

            # Check if operand 3 should be a label or a symbol
            if not tokens[0].isalnum():
                n = int(tokens[0])
                if not n in {4,-4,5,-5,7}:
                    # Then the third operand should be a symbol
                    temp = symbols.get(tokens[3],None)
                    # A wrong symbol error will be handled in the label adjustment phase
                    if temp!= None:
                        tokens[3] = temp
                    elif isAddress(tokens[3]):
                        # Do nothing cause it's a valid address
                        pass
                    else:
                        errors.append(f'SYMBOL ERROR: {tokens[3]} DOES NOT EXIST AT LINE >> {tokens[0]} {tokens[1]} {tokens[2]} {tokens[3]}')
                        ERROR_COUNT+=1
                    # The third operand should be a label that will be handled later

            # Print the modified instruction to the intermediate file
            intermFile.write(tokens[0]+" "+tokens[1]+" " +tokens[2]+" "+tokens[3]+"\n")
            lineNumber += 1
        
        line = inputFile.readline()
    
    intermFile.write(line.replace(" ",""))


def initInput():
    """Function that reads the input"""
    # Scan first input line
    line = inputFile.readline()

    # Write it without spaces to intermediate file
    while not line.startswith('+9'):
        intermFile.write(line.replace(" ",""))
        line = inputFile.readline()
    intermFile.write(line.replace(" ",""))

    # Close both files
    inputFile.close()
    intermFile.close()


def adjustLabels():
    """Function to remove the labels"""
    global ERROR_COUNT
    readInterm = open(os.path.join(sys.path[0], 'intermFile.txt'), 'r')
    # Scan then write all data initializers
    for line in readInterm:
        outputFile.write(line)
        if line.startswith('+9'):
            break

    # Scan for labels
    for line in readInterm:
        tokens = line.split()
        if tokens[0] in {"+4","-4","+5","-5","+7"}: 
            temp = labels.get(tokens[3],None)
            if temp is not None:
                tokens[3] = temp
            elif isAddress(tokens[3]):
                # Do nothing cause it's a valid address
                pass
            else : 
                errors.append(f"LABEL ERROR: {tokens[3]} DOES NOT EXIST AT LINE >> {tokens[0]} {tokens[1]} {tokens[2]} {tokens[3]}\n")
                ERROR_COUNT+=1
        outputFile.write(tokens[0]+tokens[1]+tokens[2]+tokens[3]+"\n")
        if line.startswith('+9'):
            break
    
    # Scan then write out the terminating instruction
    line = readInterm.readline()
    outputFile.write(line)

    # Scan through the rest of the file for inputs
    for line in readInterm:
        outputFile.write(line)
    
    intermFile.close()
    outputFile.close()
    os.remove(os.path.join(sys.path[0], 'intermFile.txt'))


inputFile = open(os.path.join(sys.path[0], 'assemblycode.txt'), 'r')
intermFile = open(os.path.join(sys.path[0], 'intermFile.txt'), 'w')
outputFile = open(os.path.join(sys.path[0], 'output.txt'), 'w')
switcher = {
    'ASG': '+0', 'ADD': '+1', 'MUL': '+2', 'SQR': '+3', 'EQL': '+4',
    'GTE': '+5', 'RDA': '+6', 'ITJ': '+7', 'INP': '+8', 'STP': '+9',
    'SUB': '-1', 'DIV': '-2', 'SQT': '-3', 'NEQ': '-4',
    'LSS': '-5', 'WTA': '-6', 'LBL': '-7', 'OUT': '-8'
}
symbols = {}
labels = {}

errors = []

initData()
initProgram()
initInput()
adjustLabels()

if ERROR_COUNT:
    for error in errors:
        print(error)
    print('Unsuccessful assembly due to',ERROR_COUNT,'errors!')
    os.remove(os.path.join(sys.path[0], 'output.txt'))
    exit()
else:
    print('Successful assembly!')

"""code for BEAUTIFIED code"""

outputBeautyFile = open(os.path.join(sys.path[0], 'beautifuloutput.txt'), 'w')
inputFile = open(os.path.join(sys.path[0], 'output.txt'), 'r')

for line in inputFile:
    outputBeautyFile.write(line[0:2]+' '+' '.join(line[i:i+addressLength] for i in range(2, len(line), addressLength)))
 