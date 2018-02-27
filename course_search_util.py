'''
Search a course whose course titles, course description or course remarks
match the given keyword(s) text. Detailed implementation is in phase 4, 
design is in phase 2.

Param: 
    key_word: key_word string to match course
Output: 
    for each course, display “Course Code”, “Course Title”, “No. of Units/Credits”, a list of sections of the course each with “Section”, “Date & Time”, “Quota”, “Enrol”, “Avail” and “Wait”.
    The output is sorted in ascending order of "Course Code", and sections of a single course are sorted in ascending order of "Section"
'''

def keyword_search(keyword):
    
    #Temporalily, a hard-coded course is displayed
    
    course = {"Course Code": "COMP4332", "Course Title": "Data", "No. of Units/Credits": 3,"Sections": [{"Section": "L1", 
    "Date & Time": "Wed&Fri 13:30-14:50", "Quota": 100, "Enrol": 50, "Avail": 50,"Wait": 10}, 
     {"Section": "L2", "Date & Time": "Tue&Thu 13:30-14:50", "Quota": 100, "Enrol": 40, "Avail": 60,"Wait": 10}]}

    print("The list of courses are as follows: \n")
    
    keys = list(course.keys())
    
    for key in keys[:-1]:
        print(key + ": ")
        print(course[key])
        print("")
    
    print("Sections: \n")
     
    for section in course["Sections"]:
        for key in section.keys():
            print(key + ": ")
            print(section[key])
            print("")
        print("\n\n")
    


'''
Search for a list of courses, each of which has a lecture section (e.g., “L1” and “L2”) in
a time slot, says match_ts, between the input parameters : start_ts (inclusively) and end_ts (inclusively)
???where the number of students in the waiting list of this lecture section is greater than
or equal to input real number, f, multiplied by the number of students enrolled in this lecture section in
that time slot.??? (Is this necessary due to the Satisfied attribute)

Param: 
    f: A non-negative real number 
    start_ts: A datetime object representing starting Time Slot of the interval
    end_ts: A datetime object representing ending Time Slot of the interval
    
Output: 
     for each “distinct” course, please show “Course Code”, “Course Title”, “No. of Units/Credits”, “Matched Time Slot(match_ts)”,
     a list of sections (including both lecture sections and non-lecture sections) of the course each with “Section”, “Date & Time”,
     “Quota”, “Enrol”, “Avail”, “Wait” and “Satisfied” (all shown with the content/values recorded in the time slot match_ts).
     
     The output is sorted in ascending order of "Course Code", and sections of a single course are sorted in ascending order of "Section"
     
Note: 
    If a single course satisfies the required condition in multiple time slots (no matter which lecture section of this course satisfies the required condition), we just show the latest time slot among all these time slots in which this course satisfies the required
condition. Each course should appear at most once in the output.
    Satisfied is equal to “Yes” if the number of students in the waiting list of this section is greater than or equal to f
multiplied by the number of students enrolled in this section in that time slot. It is equal to “No” otherwise. Attribute “Satisfied” is not needed to be considered in Phase 2.

'''


def size_search(f, start_ts, end_ts):
     #Temporalily, a hard-coded course is displayed
    
    course = {"Course Code": "COMP4332", "Course Title": "Data", "No. of Units/Credits": 3,"Sections": [{"Section": "L1", 
    "Date & Time": "Wed&Fri 13:30-14:50", "Quota": 100, "Enrol": 50, "Avail": 50,"Wait": 10}, 
     {"Section": "L2", "Date & Time": "Tue&Thu 13:30-14:50", "Quota": 100, "Enrol": 40, "Avail": 60,"Wait": 10}]}

    print("The list of courses are as follows: \n")
    
    keys = list(course.keys())
    
    for key in keys[:-1]:
        print(key + ": ")
        print(course[key])
        print("")
        
    print("Sections: \n")
     
    for section in course["Sections"]:
        for key in section.keys():
            print(key + ": ")
            print(section[key])
            print("")
        print("\n\n")

    
    

from datetime import datetime

#Interface

def course_search_handler():
    
    print("1. Search by keywords")
    print("2. Search by waiting list size")
    print("3. Cancel")
    search_type = input("Please input your choice: 1-3\n")
    
    while(True): 
        if(search_type == "1"):

            keyword = input("Please input search keyword: \n")
            keyword_search(keyword)
            break
        elif(search_type == "2"):

            isValid = False
            while(isValid == False):

                f = input("Please input a non-negative real number for parameter f: \n")
                start_ts = input("Please input the start time slot string in YYYY-MM-DD HH:mm format\n")
                end_ts = input("Please input the end time slot string in YYYY-MM-DD HH:mm format\n")

                try: 
                    f = float(f)
                    start_ts = datetime.strptime(start_ts, "%Y-%m-%d %H:%S")
                    end_ts = datetime.strptime(end_ts, "%Y-%m-%d %H:%S")
                except ValueError as error:
                    print("Invalid input format!\n")
                    continue
                if f < 0:
                    print("f should be non-negative!\n")
                    continue
                
                isValid = True   
                
                
            size_search(f, start_ts, end_ts)
            break
        elif(search_type == "3"):
            break
        else:
            print("Invalid Input!\n")
            
