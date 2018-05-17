import scrapy
import subprocess
import os
URL = None #Global variable of URL for the crawling webpage



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
    print(url)
    try:
        if (url=="default"):
            #crawl all data from the default URL given in the project webpage 
            #inserted the data into the database
            #print("Default Data Crawling is successful and all data are inserted into the database")
            URL = "http://comp4332.com/realistic"
        else:
            #crawl all data from the URL inputted 
            #inserted the data into the database
            #print("Data Crawling is successful and all data are inserted into the database")
            URL = url

        #Store URL in file
        
        os.chdir('./testCrawl/')
        print(os.getcwd())
        with open('url.txt', 'w') as u_f:
            u_f.write(URL)
            u_f.close()
        command = "scrapy crawl Page"
        subprocess.run(command,shell=True, check=True, stdout=subprocess.PIPE)
    except Exception as e:
        print(e)
        
    
    return
#Interface

def crawling_handler():
    
    #url = input("Please enter a URL or a special keyword: ")
    url = 'default'
    data_crawling(url)
    
    return

'''
def main():
    crawling_handler()
if __name__ == "__main__":
    main()
'''
