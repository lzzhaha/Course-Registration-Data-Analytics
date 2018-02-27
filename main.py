
# coding: utf-8

# # Workflow of the whole program and display the interfaces

# In[1]:


from collection_util import collection_handler
from crawling_util import crawling_handler
from course_search_util import course_search_handler
from prediction_util import prediction_handler
from training_util import training_handler


# In[4]:


def main():
    
    choice = "0"
    while(True):
        print("")
        print("\t Functionalities Menu")
        print("=======================")
        print("1. Collection Dropping and Empty Collection Creating")
        print("2. Data Crawling")
        print("3. Course Search")
        print("4. Waiting List Size Prediction")
        print("5. Waiting List Size Training")
        print("6. Exit")
        print("")
        
        choice = input("Please input your choice (1-6):")
        print("")
        
        if (choice == "1"):
            collection_handler()
        elif (choice == "2"):
            crawling_handler()
        elif (choice == "3"):
            course_search_handler()
        elif (choice == "4"):
            prediction_handler()
        elif (choice == "5"):
            training_handler()
        elif (choice == "6"):
            print("Bye!")
            break;
        else:
            print("Invalid Input!")


# In[5]:


if __name__ == "__main__":
   main()

