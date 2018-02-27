'''
Predict the size of waiting list of a lecture of a specific course during a given time slot. The predictions are made by 5 models.
Detailed implementation is in phase 5 and 6.

Param:
    cc: Course code string (e.g. 'COMP4332')
    ln: Lecture Number (e.g., the input should be “1” denoting “L1”)
    ts: Time Slot
    
Output:
    “N1, N2, N3, N4, N5”
    where Ni denotes the number of students in the waiting list of the lecture
    number (ln) (if any) of the course cc in the given time slot (ts) predicted by
    Model i for each i in [1, 5] (Note that these 5 numbers are integers.)
    
Note: See projec_spec p10 - p11
'''

def predict_size(cc, ln, ts):
     
   #Temporalily, only print 5 numbers
    print("\n\n")
    print(1, 2, 3, 4, 5)
        
        
        
from datetime import datetime        
# Interface

def prediction_handler():
    
    is_Valid = False
    
    while(is_Valid == False):
        
        try:
            cc = input("Please enter course code, e.g. COMP4332: ")
            ln = int(input("Please enter lecture number, which should be '1' denoting 'L1': "))
            ts = input("Please enter the time slot string in YYYY-MM-DD HH:mm format: ")
            
            ts = datetime.strptime(ts, "%Y-%m-%d %H:%S")
            is_Valid = True
            
        except ValueError as error:
            print("Invalid input format!\n")
                                  
    
    predict_size(cc, ln, ts)
                
                