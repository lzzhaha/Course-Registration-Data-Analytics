
# coding: utf-8

# In[1]:


import os 
import numpy as np
from model_util import model1, model2, model3, model4, model5, ftp_map


# In[4]:


''' 
For each lecture section of each course, train 5 models. Assume all data are 
preprocessed, legally named and stored in the corresponding directory already.
For example, data of COMP4332 L1 of file type 1 is stored in ./ftp1/COMP4332-L1.csv
'''
def training_handler():   
    #initialize objects for training
    #To submit    
    #model_list = [model1(), model2(), model3(), model4(), model5()]
    model_list = [model1(), model2()]
    cwd = os.getcwd()
    for f in os.listdir(cwd):
        if(not os.path.isdir(f) or not f.startswith('ftp')):
            continue
    
        dir_name = os.path.join(cwd, f)
        
        #list of model number responsible for this file type
        model_num_list = ftp_map[f]
        
        for csv_f in os.listdir(dir_name):
            if(csv_f[-4:] != ".csv"):
                continue
            for num in model_num_list:
                model_list[num-1].train(directory = dir_name, fn=csv_f)

