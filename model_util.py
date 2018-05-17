
# coding: utf-8

# In[1]:


import os 
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
from keras.layers import Dropout
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.externals import joblib


# In[2]:


#A mapping between the prefix of file types folders and the model
#the element at index i corresponds to the file type number of (i+1)-th model
#e.g. model 2 corresponds to file type 1
ftp_map = {'ftp1': [1], 'ftp2': [2]}


# In[3]:


'''
Save the input model in json and h5 
file format.
'''
def save_model(model, modelFilenamePrefix):
    structureFilename = modelFilenamePrefix + ".json"
    model_json = model.to_json()
    with open(structureFilename, "w") as f:
        f.write(model_json)
    weightFilename = modelFilenamePrefix + ".h5"
    model.save_weights(weightFilename)

    print("Successfully save model in {} and {}\n".format(structureFilename, weightFilename))


# ## A base class of 5 models

# In[4]:


class base:
    def __init__(self):
        self._model_num = 100
    
    def train(self, directory, fn):#function to be overrided
         print("Training Model No.{} for {}\n".format(self._model_num, fn))
    
    '''
    Load the model for given course code and lecture number
    
    Para:
        cc: course code
        ln: lecture number
    '''
    
    def read_model(self, cc, ln):
        
        #Obtain file names
        read_dir = './model{}/'.format(self._model_num)
        fn = '{}-L{}'.format(cc, ln)
        structure_file = os.path.join(read_dir, fn + '.json')
        weight_file = os.path.join(read_dir, fn + '.h5')
        
        
        #load model
        try:
            with open(structure_file, 'r') as sf:
                model = model_from_json(sf.read())
            model.load_weights(weight_file)
        except FileNotFoundError as e:
            print("There is no such lecture section and thus there is no prediction result.\n")
            return None
            
            
        return model
    
    '''
    Get the test data for this model based on course code, 
    lecture number and timestamp. The implementation depends
    on the design of input of each model.
    
    Params:
        cc: course code
        ln: lecture number
        t_unit: No of Unit of time (30 mins)
        scalre_direc: directory of the scaler of the dataset (if any)
    
    Return:
        X: a numpy array of shape 1 x num_feature
    '''
    def get_test_data(self, cc, ln , t_unit, scaler_direc=None):
        print("Get test data from {}-L{} for Model {} \n".format(cc, ln, self._model_num))
        


# In[5]:



class model1(base):
    
    
    def __init__(self):
        self._model_num =1
    '''
    Train the model 1 for prediction function in section 5.4.
    Save the trained model in json and h5 files in correpsonding
    directory.

    Param: 
        directory: the directory of the file
        fn : file name of the traininig data (e.g. COMP4332-L1.csv)
        
    Output: 
        Successful message after the training process on the waiting list size finishes.

    
    '''

    def train(self, directory, fn):
        super().train(directory, fn)
        np.random.seed(11)
        
        #Generate the absolute path name
        load_fn = os.path.join(directory, fn)
        
        #Load data
        dataset = np.loadtxt(load_fn, delimiter=',')

        X = dataset[:, 0:8]
        

        Y = dataset[:, 8]


        #Build model

        

        model = Sequential()
        model.add(Dense(8, input_dim=8, activation='relu'))
        model.add(Dense(1, activation='relu'))
        model.compile(loss="mse", optimizer="adam", metrics=["mse"])
        model.fit(X, Y, epochs=150, batch_size=32, validation_split=0.2)
        
        
        
        print("Waiting list size training for model 1 is successful\n")
        
        
        save_dir = './model{}/'.format(self._model_num)
        
        save_fn = os.path.join(save_dir, fn.split('.')[0])
        save_model(model, save_fn)
    
    '''
    Get the test data for this model based on course code, 
    lecture number and timestamp. The implementation depends
    on the design of input of each model.
    
    Params:
        cc: course code
        ln: lecture number
        t_unit: No of Unit of time (30 mins)
        scalre_direc: directory of the scaler of the dataset (if any)
    return:
        X: a numpy array of shape 1 x num_feature
    '''
    def get_test_data(self, cc, ln , t_unit, scaler_direc=None):
        super().get_test_data(cc = cc, ln = ln, t_unit = t_unit)

        df = None
        fn = "{}-L{}.csv".format(cc, ln)
        raw_dir = './Raw_Time_Series/'

        for f in os.listdir(raw_dir):
            #print(f)
            if(f == fn):
                
                f = os.path.join(raw_dir, f)
                df = pd.read_csv(f)


        df.drop(['Timestampe', "NoOfTimeUnit"], axis=1, inplace=True)

        dataset = df.values

        noOfPrev = noOfFuture = 1

        #Add previous data
        count = 0 #number of previous data already added
        step = 1 #number of steps going backward
        previous_data = []

        while(count <noOfPrev and t_unit - step>=0):
            if(dataset[t_unit - step, 0] == -1):
                step+=1
                continue
            else:
                count+=1
                previous_data = [dataset[t_unit-step, :]] + previous_data


        #Add future data
        count = 0 #number of future data already added
        step = 0 #number of steps going forward
        future_data = []
        while(count <noOfFuture and t_unit + step < dataset.shape[0]):

            if(dataset[t_unit + step, 0] == -1):
                step+=1
                continue
            else:
                count+=1
                future_data.append(dataset[t_unit + step,:])




        previous_data = np.array(previous_data).flatten()
        previous_data = previous_data.reshape(previous_data.shape[0],1)
        future_data = np.array(future_data).flatten()
        future_data = future_data.reshape(future_data.shape[0],1)
       
        dataX = np.append(previous_data, future_data, axis=0)
        #dataX = np.array(dataX).astype(float)

        #Normalize data
        scaler_filename = os.path.join(scaler_direc, "scaler.save")
        scaler = joblib.load(scaler_filename)
        
        X_test = scaler.fit_transform(dataX)
        X_test = X_test.reshape(1,X_test.shape[0])
        return X_test 

    
    

    


# In[6]:


class model2(base):
    def __init__(self):
        self._model_num =2
    '''
    Train the model 2 for prediction function in section 5.4.
    Save the trained model in json and h5 files in correpsonding
    directory.

    Param: 
        directory: the directory of the file
        fn : file name of the traininig data (e.g. COMP4332-L1.csv)
        
    Output: 
        Successful message after the training process on the waiting list size finishes.

    
    
    '''
    def train(self, directory, fn):
        super().train(directory, fn)
        np.random.seed(11)
        
        #Generate the absolute path name
        load_fn = os.path.join(directory, fn)
        
        #Load data
        dataset = np.loadtxt(load_fn, delimiter=',')

        X = dataset[:, 0:8]
        

        Y = dataset[:, 8]


        #Build model

        

        model = Sequential()
        model.add(Dense(8, input_dim=8, activation='relu'))
        model.add(Dense(8, activation='relu'))
        model.add(Dense(1, activation='relu'))
        model.compile(loss="mse", optimizer="adam", metrics=["mse"])
        model.fit(X, Y, epochs=150, batch_size=32, validation_split=0.2)
        
        
        
        print("Waiting list size training for model2 is successful\n")
        
        
        save_dir = './model{}/'.format(self._model_num)
        
        save_fn = os.path.join(save_dir, fn.split('.')[0])
        save_model(model, save_fn)
    
    def get_test_data(self, cc, ln , t_unit, scaler_direc=None):
        super().get_test_data(cc = cc, ln = ln, t_unit = t_unit)

        df = None
        fn = "{}-L{}.csv".format(cc, ln)
        raw_dir = './Raw_Time_Series/'

        for f in os.listdir(raw_dir):
            #print(f)
            if(f == fn):
                
                f = os.path.join(raw_dir, f)
                df = pd.read_csv(f)


        df.drop(['Timestampe', "NoOfTimeUnit"], axis=1, inplace=True)

        dataset = df.values

        noOfPrev = noOfFuture = 1

        #Add previous data
        count = 0 #number of previous data already added
        step = 1 #number of steps going backward
        previous_data = []

        while(count <noOfPrev and t_unit - step>=0):
            if(dataset[t_unit - step, 0] == -1):
                step+=1
                continue
            else:
                count+=1
                previous_data = [dataset[t_unit-step, :]] + previous_data


        #Add future data
        count = 0 #number of future data already added
        step = 0 #number of steps going forward
        future_data = []
        while(count <noOfFuture and t_unit + step < dataset.shape[0]):

            if(dataset[t_unit + step, 0] == -1):
                step+=1
                continue
            else:
                count+=1
                future_data.append(dataset[t_unit + step,:])




        previous_data = np.array(previous_data).flatten()
        previous_data = previous_data.reshape(previous_data.shape[0],1)
        future_data = np.array(future_data).flatten()
        future_data = future_data.reshape(future_data.shape[0],1)
       
        dataX = np.append(previous_data, future_data, axis=0)
        #dataX = np.array(dataX).astype(float)

        #Normalize data
        #scaler_filename = os.path.join(scaler_direc, "scaler.save")
        #scaler = joblib.load(scaler_filename)
        
        #X_test = scaler.fit_transform(dataX)
        #X_test = X_test.reshape(1,X_test.shape[0])
        return dataX.reshape(1, dataX.shape[0])     


# In[7]:


class model3(base):
    def __init__(self):
        self._model_num =3
    '''
    Train the model 3 for prediction function in section 5.4.
    Save the trained model in json and h5 files in correpsonding
    directory.

    Param: 
        directory: the directory of the file
        fn : file name of the traininig data (e.g. COMP4332-L1.csv)
        
    Output: 
        Successful message after the training process on the waiting list size finishes.

    
    '''
   
    
    def train(self, directory, fn):
        super().train(directory, fn)
        np.random.seed(11)
        
        #Generate the absolute path name
        load_fn = os.path.join(directory, fn)
        
        #Load data
        dataset = np.loadtxt(load_fn, delimiter=',')

  
        #Build model

        print("Waiting list size training for model 3 is successful")
        
        save_dir = './model{}/'.format(self._model_num)
        save_fn = os.path.join(save_dir, fn.split('.')[0])
        save_model(model, save_fn)

     
    

    '''
    Get the test data for this model based on course code, 
    lecture number and timestamp. The implementation depends
    on the design of input of each model.
    
    Params:
        cc: course code
        ln: lecture number
        t_unit: No of Unit of time (30 mins)
        scalre_direc: directory of the scaler of the dataset (if any)
    
    Return:
        X: a numpy array of shape 1 x num_feature
    '''
    
    def get_test_data(self, cc, ln , t_unit, scaler_direc=None):
        super().get_test_data( cc = cc, ln = ln, t_unit = t_unit)
        
        
        #Code for extracting data here...
        X_test = np.array([[1],[2],[3]])
        
        return X_test
    
    

# In[8]:


class model4(base):
    def __init__(self):
        self._model_num =4
    '''
    Train the model 4 for prediction function in section 5.4.
    Save the trained model in json and h5 files in correpsonding
    directory.

    Param: 
        directory: the directory of the file
        fn : file name of the traininig data (e.g. COMP4332-L1.csv)
        
    Output: 
        Successful message after the training process on the waiting list size finishes.

    
    '''

    
    def train(self, directory, fn):
        super().train(directory,fn)
        np.random.seed(11)
        
        #Generate the absolute path name
        load_fn = os.path.join(directory, fn)
        
        #Load data
        dataset = np.loadtxt(load_fn, delimiter=',')



        #Build model

    
        
        print("Waiting list size training for model 4 is successful\n")
        
        save_dir = './model{}/'.format(self._model_num)
        save_fn = os.path.join(save_dir, fn.split('.')[0])
        save_model(model, save_fn)
    
    '''
    Get the test data for this model based on course code, 
    lecture number and timestamp. The implementation depends
    on the design of input of each model.
    
    Params:
        cc: course code
        ln: lecture number
        t_unit: No of Unit of time (30 mins)
        scalre_direc: directory of the scaler of the dataset (if any)
    
    Return:
        X: a numpy array of shape 1 x num_feature
    '''
    
    def get_test_data(self, cc, ln , t_unit, scaler_direc=None):
        super().get_test_data( cc = cc, ln = ln, t_unit = t_unit)
        
        
        #Code for extracting data here...
        X_test = np.array([[1],[2],[3]])
        
        return X_test
    
    


# In[9]:


class model5(base):
    def __init__(self):
        self._model_num =5
    '''
    Train the model 5 for prediction function in section 5.4.
    Save the trained model in json and h5 files in correpsonding
    directory.

    Param: 
        directory: the directory of the file
        fn : file name of the traininig data (e.g. COMP4332-L1.csv)
        
    Output: 
        Successful message after the training process on the waiting list size finishes.

    
    '''
    
    
    def train(self, directory, fn):
        super().train(directory,fn)
        np.random.seed(11)
        
        #Generate the absolute path name
        load_fn  = os.path.join(directory, fn)
        
        #Load data
        dataset = np.loadtxt(load_fn, delimiter=',')




        #Build model

         
        
        print("Waiting list size training is successful")
        
        save_dir = './model{}/'.format(self._model_num)
        save_fn = os.path.join(save_dir, fn.split('.')[0])
        save_model(model, save_fn)
        
    
    '''
    Get the test data for this model based on course code, 
    lecture number and timestamp. The implementation depends
    on the design of input of each model.
    
    Params:
        cc: course code
        ln: lecture number
        t_unit: No of Unit of time (30 mins)
        scalre_direc: directory of the scaler of the dataset (if any)
    
    Return:
        X: a numpy array of shape 1 x num_feature
    '''
    
    def get_test_data(self, cc, ln , t_unit, scaler_direc=None):
        super().get_test_data( cc = cc, ln = ln, t_unit = t_unit)
        
        
        #Code for extracting data here...
        X_test = np.array([[1],[2],[3]])
        
        return X_test
    
    

