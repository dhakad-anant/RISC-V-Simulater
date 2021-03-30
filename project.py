# CS204 Project
# Read the .mc file as input
mcFile = open("input.mc","r+")
# File reading completed

#defining global variables________________________________________________________________________________
reg = [0]*32
RS1,RS2,RD,RM,RZ,RY,RA,RB,PC,IR,MuxB_select,MuxC_select,MuxINC_select,MuxY_select,MuxPC_select,RegFileAddrA,RegFileAddrB,RegFileAddrC,RegFileInp,RegFileAOut,RegFileBOut,MAR,MDR,opcode,immed=[0]*25
dataMemory = {}
instructionMemory = {}

def Fetch():
    #Pc, ir
    global IR
    print("Fetching the instruction")
    IR = instructionMemory[hex(PC)]
    print(IR)

def Decode():
    print("Decoding the instruction")
    #getting the opcode
    global opcode
    opcode = int(str(IR),16) & int("0x7f",16)
    fun3 = (int(str(IR),16) & int("0x7000",16)) >> 12
    instruction = [0]*32
    print(opcode)
    # R format - (add,srl,sll,sub,slt,xor,sra,and,or,) ( mul, div, rem)
    # R format - (0110011)(?)
    
    # I format - (lb,lh,lw,)(addi, andi, ori,)(jalr)
    # I format - (0000011)(0010011)(1100111)
    
    # S format - (sb, sw, sh)
    # S format - (0100011) f3 - sb - 000, sh - 001, sw - 010
    
    # SB format - beq, bne, bge, blt
    # SB format - (1100011) f3 - beq - 000, bne - 001, blt - 100, bge - 101
    
    # U format - auipc-0010111, lui-0110111
    
    # UJ format - jal-1101111


    if opcode==int("0110011",2): # r format
        pass
    elif opcode==int("0000011",2) or opcode==int("0010011",2) or opcode==int("1100111",2): # i format

        RD = (int(IR,16) & '0xF80') >> 7
        RS1 = (int(IR,16) & '0xF8000') >> 15
        immed = (int(IR,16) & '0xFFF00000') >> 20

    elif opcode==int("0100011",2): # S format
        RS1 = (int(str(IR),16) & int("0xF8000",16)) >> 15
        RS2 = (int(str(IR),16) & int("0x1F00000",16)) >> 20
        immed40 = (int(str(IR),16) & int("0xF80",16)) >> 7
        print("immed40 : ",immed40)
        immed11to5 = (int(str(IR),16) & int("0xFE000000",16)) >> 20
        print("immed11to5 : ",immed11to5)
        immed = immed40 | immed11to5
        print("rs1 : ",RS1)
        print("rs2 : ",RS2)
        print("immed : ",immed)
        if fun3 != int("000",2) and fun3 != int("001",2) and fun3 != int("010",2):
            print("invalid opcode")
            exit(1)
            return

    elif opcode==int("1100011",2): # SB format
        pass
    elif opcode==int("0010111",2) or opcode==int("0110111",2): # U type
        pass
    elif opcode==int("1101111",2): # UJ format
        pass
    else:
        print("invalid opcode")
        
def Execute():

    pass

def MemoryAccess():
    pass

def RegisterUpdate():
    pass

def validateDataSegment(y):
    if len(y)!=2:
        return False
    addr,data = y[0],y[1]
    if addr[:2]!='0x' or data[:2]!='0x':
        return False
    try:
        if int(addr,16)<int("0x10000000",16):
            return False
        int(data,16)
    except:
        return False 
    return True

def main():
    # load the data segment
    flag = 0
    for x in mcFile:
        #creating a hashmap, data segment stored
        y = x.split('\n')[0].split()
        if flag==1:
            if validateDataSegment(y)==False:
                print("ERROR")
                exit(1)
            dataMemory[y[0]] = y[1]
        if '$' in y:
            flag = 1
        if flag==0:
            #TODO : Add Validation______________
            y = x.split('\n')[0].split()
            instructionMemory[y[0]] = y[1]            
    # run simulator 
    run_RISC_simulator()
    # exit from the code

def run_RISC_simulator():
    Fetch()
    Decode()
    Execute()
    MemoryAccess()
    RegisterUpdate()

main()
