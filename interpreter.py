import os
import sys

def getAddressLength():
    global addressLength
    # Open the numeric code
    tempFile = open(os.path.join(sys.path[0], 'output.txt'), 'r')
    # Initialize the address length
    addressLength = int((len(tempFile.readline().strip()) - 2) / 3)
    tempFile.close()

addressLength = None
getAddressLength()

dataMemory = [0 for x in range(10 ** addressLength)]
programMemory = [0 for x in range(10 ** addressLength)]

inputFile = open(os.path.join(sys.path[0], 'output.txt'), 'r')
IP = 0

def ADD(op1, op2, op3):
    """This functions adds the value in address op1 to the value in
        address op2 and stores the sum in address op3 in data memory"""
    dataMemory[op3] = dataMemory[op1] + dataMemory[op2]


def SUB(op1, op2, op3):
    """This functions subtracts the value in address op1 to the value in
    address op2 and stores the subtraction in address op3 in data memory"""
    dataMemory[op3] = dataMemory[op1] - dataMemory[op2]


def MUL(op1, op2, op3):
    """This functions multiplies the value in address op1 to the value in
        address op2 and stores the multiplication in address op3 in data memory"""
    dataMemory[op3] = dataMemory[op1] * dataMemory[op2]


def DIV(op1, op2, op3):
    """This functions divides the value in address op1 to the value in
        address op2 and stores the division in address op3 in data memory"""
    dataMemory[op3] = dataMemory[op1] / dataMemory[op2]


def ASG(op1, op2, op3):
    """This functions assigns to the address op3 the value in the address op1"""
    dataMemory[op3] = dataMemory[op1]


def OUT(op1, op2, op3):
    """This functions outputs the value in the address op1"""
    print(">> ", dataMemory[op1])


def SQR(op1, op2, op3):
    """This function calculates the square of the value in address op1 and stores
        the square in address op3 in data memory"""
    dataMemory[op3] = dataMemory[op1] * dataMemory[op1]


def GTE(op1, op2, op3):
    """This function checks if the value in address op1 is bigger than or equal to the value in address op2.
        If it's true then it changes the IP to point to the instruction of address op3"""
    global IP
    if dataMemory[op1] >= dataMemory[op2]:
        IP = op3


def INP(op1, op2, op3):
    """This functions inputs a value and stores it in the address op3"""
    line = inputFile.readline()
    if not line.startswith('+9') :
        dataMemory[op3] = int(line)


def SQT(op1, op2, op3):
    """This function calculates the square root of the value in address op1 and stores
            the square root in address op3 in data memory"""
    dataMemory[op3] = dataMemory[op1] ** 0.5


def EQL(op1, op2, op3):
    """This function checks if the value in address op1 and the value in address op2 are equal.
        If it's true then it changes the IP to point to the instruction of address op3"""
    global IP
    if dataMemory[op1] == dataMemory[op2]:
        IP = op3


def WTA(op1, op2, op3):
    """This functions writes a value from the address op3 and stores in the array"""
    dataMemory[op2 + dataMemory[op3]] = dataMemory[op1]


def RDA(op1, op2, op3):
    """This functions reads a value from the array and stores it in the address op3"""
    dataMemory[op3] = dataMemory[op1 + dataMemory[op2]]


def STP(op1, op2, op3):
    """This function stops the program"""
    pass


def ITJ(op1, op2, op3):
    """This function increments the index (loop), compares it to the number of element,
        if smaller then changes the IP to point to the instruction of address op3"""
    global IP
    dataMemory[op1] += 1
    if dataMemory[op1] < dataMemory[op2]:
        IP = op3


def NEQ(op1, op2, op3):
    """This function checks if the value in address op1 and the value in address op2 are not equal.
            If it's true then it changes the IP to point to the instruction of address op3"""
    global IP
    if dataMemory[op1] != dataMemory[op2]:
        IP = op3


def LSS(op1, op2, op3):
    """This function checks if the value in address op1 is strictly smaller than the value in address op2.
                    If it's true then it changes the IP to point to the instruction of address op3"""
    global IP
    if dataMemory[op1] < dataMemory[op2]:
        IP = op3


def fillData():
    """This functions read all the data memory from the file"""
    line = inputFile.readline()
    idx = 0
    while not line.startswith('+9') :
        dataMemory[idx] = int(line)
        line = inputFile.readline()
        idx += 1


def fillProgram():
    """This functions read all the program memory from the file"""
    line = inputFile.readline()
    idx = 0
    while  not line.startswith('+9'):
        programMemory[idx] = int(line)
        line = inputFile.readline()
        idx += 1
    programMemory[idx] = int(line)
    inputFile.readline()


def executeProgram():
    """This function performs the read-decode-execute cycle"""
    global IP
    opcode = int(programMemory[IP] / (10 ** (3 * addressLength)))
    while opcode != 9:
        # Compute the three operands using division and modulo
        op1 = abs(int(abs(programMemory[IP]) / (10 ** (2 * addressLength))) - abs(opcode) * (10 ** addressLength))
        op3 = abs(abs(programMemory[IP]) % (10 ** (addressLength)))
        op2 = abs(int((abs(programMemory[IP]) % (10 ** (2 * addressLength)) - op3) / (10 ** addressLength)))

        # Increment the IP
        IP += 1
        
        # Execute the instruction
        switcher[opcode](op1, op2, op3)

        # Compute the next line's opcode
        opcode = int(programMemory[IP] / (10 ** (3 * addressLength)))


def Display(startindex, endindex, which):
    """This function displays data or code from a starting address until an ending address in the memory"""
    if which == 'data':
        print(dataMemory[int(startindex):int(endindex)+1])
    elif which == 'program':
        print(programMemory[int(startindex):int(endindex)+1])
    else:
        raise Exception('Invalid!')


switcher = {
    +0: ASG, +1: ADD, +2: MUL, +3: SQR, +4: EQL,
    +5: GTE, +6: RDA, +7: ITJ, +8: INP, +9: STP,
    -1: SUB, -2: DIV, -3: SQT, -4: NEQ,
    -5: LSS, -6: WTA, -8: OUT
}

fillData()
fillProgram()
executeProgram()
#Display('000','007','data')