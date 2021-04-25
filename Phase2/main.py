from state_class import CPU,State,BTB
from hdu_class import HDU
states=[None for i in range(5)] # don't change it
predictionEnabled=1
hduob = HDU()
prediction_enabled = 1
knob2_stallingEnabled= True # don't change it
controlChange = False
cntBranchHazards = 0
cntBranchHazardStalls = 0
controlChange_pc = 0
controlHazard = False
controlHazard_pc = 0
btb = BTB()
cntDataHazards = 0
cntDataHazardsStalls = 0
ProcessingUnit = CPU(prediction_enabled)
ProcessingUnit.readFile()
master_PC=0
master_cycle=0
masterClock = 0
# states[0] - fetch
# states[1] - Decode
# states[2] - execute
# states[3] - MemoryAccess
# states[4] - writeback
while True:

    if knob2_stallingEnabled:
        checkDataHazard = hduob.checkDataHazardStalling(states)
        copyOfStates = states[:] 
        # states[0] = State(master_PC)

        # [state1,state2,state3,state4,state5]  
        # stalling will occcue when data hazard
        # control hazard means stalling
        alreadyUpdatedPC = 0
        for i in reversed(range(5)):
            print("states : ",states)
            if(i==0):
                states[i] = State(master_PC)
                states[i] = ProcessingUnit.Fetch(states[i],btb)
                if(states[i].predictionPC!=-1):
                    master_PC = states[i].predictionPC
                    alreadyUpdatedPC = 1
                # controlChange = states[i+1].predictionOutcome
                # controlChange_pc= states[i+1].predictionPC
                # states[i]=None  
                states[i+1]=states[i]
                states[i]=None
            if(i==1):
                if(states[i]==None):
                    continue
                controlHazard,control_hazard_pc,st = ProcessingUnit.Decode(states[i],btb)
                if(controlHazard==1):
                    master_PC = states[i].PC + 4
                states[i+1] = states[i]
                states[i]=None         
            if(i==2):
                if(states[i]==None):
                    continue
                ProcessingUnit.Execute(states[i])
                states[i+1]=states[i]
                states[i]=None                
            if(i==3):
                if(states[i]==None):
                    continue
                ProcessingUnit.MemoryAccess(states[i])
                states[i+1]=states[i]
                states[i]=None
            if(i==4):
                if(states[i]==None):
                    continue
                ProcessingUnit.RegisterUpdate(states[i])
                states[i]=None        
        if(alreadyUpdatedPC == 0):
            master_PC += 4
    else:
        pass

    masterClock +=1
    if states[0]==None and states[1]==None and states[2]==None and states[3]==None and states[4]==None:
        break
    states = [State(master_PC)]+states
print(ProcessingUnit.reg)
print("Program Executed!!!")