
# coding: utf-8

# In[1]:


#from model_util import model1, model2, model3, model4, model5, ftp_map
import pandas as pd
from datetime import datetime, timedelta
import os
from model_util import model1, model2, model3, model4, model5, ftp_map


# In[2]:


start_ts = datetime.strptime("2018-01-25 09:00", "%Y-%m-%d %H:%M")
end_ts = datetime.strptime("2018-02-15 00:30", "%Y-%m-%d %H:%M")


# In[3]:


'''
Convert ts to No of time unit(start from 0).
Params:
    start_ts: datetime object
    delta: the space between timestamps in the unit of minute
    ts: datetime object
'''
def get_time_unit(start_ts, ts, delta=30):
    diff = ts - start_ts
    
    unit = ((diff.days)*24*60 + diff.seconds/60)/30
    
    
    return int(unit)


# In[4]:


'''
Check whether the waitinglist size is already given in the training data and
check whether the course and lecture  exists or not.

Return:
    cl_exist : True if such lecuture of course exists
    wait_size : -1 if the timestamp is not in training set, otherwise return the stored value
'''
def is_exist(cc, ln, t_unit):
    
    cl_exist =False
    wait_size = None
    df = None
    fn = "{}-L{}.csv".format(cc, ln)
    raw_dir = './Raw_Time_Series/'
    for f in os.listdir(raw_dir):
        if(f == fn):
            f = os.path.join(raw_dir, f)
            df = pd.read_csv(f)
            #print("unit: {}".format(t_unit))
            ws = df[df['NoOfTimeUnit'] == t_unit]['wait'].values[0]
            
            cl_exist = True
            wait_size = ws
            return cl_exist, wait_size
    print("There is no such lecture section and thus there is no prediction result.\n")
    
    return cl_exist, wait_size


# In[6]:


from datetime import datetime        
'''
Function for 5.4.

Output: 
    N1, N2, .. N5
    where each number is the result of the corresponding model
'''

def prediction_handler():
    
    is_Valid = False
    
    while(is_Valid == False):
        
        try:
            cc = input("Please enter course code, e.g. COMP4332: ")
            ln = int(input("Please enter lecture number, which should be '1' denoting 'L1': "))
            ts = input("Please enter the time slot string in YYYY-MM-DD HH:mm format: ")
            
            ts = datetime.strptime(ts, "%Y-%m-%d %H:%M")
            is_Valid = True
            
        except ValueError as error:
            print("Invalid input format!\n")
                                  
    
    #Check whether the target waiting size exists or not
    t_unit = get_time_unit(start_ts=start_ts, ts = ts)
    lec_exist, wait_size  = is_exist(cc, ln, t_unit)
    if(lec_exist):
        if(wait_size != -1):
            print("The target waiting list size is already in the training data and it is : {}".format(wait_size))
            return
    else:
        print("There is no such lecture section and thus there is no prediction result.\n")
        return 
    
    #initialize objects for training
    #To submit
    #model_list = [model1(), model2(), model3(), model4(), model5()]
    model_list = [model1(), model2()]
    
    pred_list = []
    
    for model in model_list:
        
        regressor = model.read_model(cc = cc, ln = ln)
        
        #Get input for regressor
        
        #Get file type
        scaler_direc = None
        for ftp in ftp_map:
            if model._model_num in ftp_map[ftp]:
                scaler_direc = './' + ftp + '/'
        X_test = model.get_test_data(cc = cc, ln = ln, t_unit = t_unit, scaler_direc = scaler_direc)
        
        
        Y_pred = int(round(regressor.predict(X_test)[0][0]))
        pred_list.append(str(Y_pred))
    
    output = ','.join(pred_list)
    print(output)

