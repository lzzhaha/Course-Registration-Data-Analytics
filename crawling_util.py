
'''
Otains the information of each webpage and
inserts this information into the database of the database server set up
in Phase .
Detailed implementation is in phase 3.

Param: 
    url: a string containing a URL (e.g., “http://course.cse.ust.hk/comp4332/index.html”) or a specifial keyword, 'default
Output:
    successful messages or failure messages for exceptions
'''

def data_crawling(url):

    
    if (url=="default"):
        #crawl all data from the default URL given in the project webpage 
        #inserted the data into the database
        print("Default Data Crawling is successful and all data are inserted into the database")
    else:
        #crawl all data from the URL inputted 
        #inserted the data into the database
        print("Data Crawling is successful and all data are inserted into the database")
    return




#Interface

def crawling_handler():
    
    url = input("Please enter a URL or a special keyword: ")
    
    data_crawling(url)
    
    return 