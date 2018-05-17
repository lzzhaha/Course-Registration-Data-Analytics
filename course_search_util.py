from pymongo import MongoClient
from bson.son import SON
import pprint
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
    
    try :
        client = MongoClient("mongodb://localhost:27017")
        
        db = client["university"]
        
        keyword = list(keyword)

        punct = [" ", ",", ";", ".", "?", ":", "'", "\"", "/", "\\", "&", "+", "-", "=", "*", "!", "(", ")"]

        for p in punct:
            temp = []

            for element in keyword:
                temp += element.split(p);
            
            keyword = temp
    



        result = db.course.aggregate(
            [
                {
                    "$project":{
                        "_title":{ 
                            "$setUnion":[
                            {"$setIntersection":[keyword,{"$split":["$course_title"," "]}]},
                            {"$setIntersection":[keyword,{"$split":["$course_title",","]}]},
                            {"$setIntersection":[keyword,{"$split":["$course_title","."]}]},
                            {"$setIntersection":[keyword,{"$split":["$course_title","?"]}]},
                            {"$setIntersection":[keyword,{"$split":["$course_title",":"]}]},
                            {"$setIntersection":[keyword,{"$split":["$course_title","'"]}]},
                            {"$setIntersection":[keyword,{"$split":["$course_title","\""]}]},
                            {"$setIntersection":[keyword,{"$split":["$course_title","/"]}]},
                            {"$setIntersection":[keyword,{"$split":["$course_title","\\"]}]},
                            {"$setIntersection":[keyword,{"$split":["$course_title","&"]}]},
                            {"$setIntersection":[keyword,{"$split":["$course_title","+"]}]},
                            {"$setIntersection":[keyword,{"$split":["$course_title","-"]}]},
                            {"$setIntersection":[keyword,{"$split":["$course_title","="]}]},
                            {"$setIntersection":[keyword,{"$split":["$course_title","*"]}]},
                            {"$setIntersection":[keyword,{"$split":["$course_title","!"]}]},
                            {"$setIntersection":[keyword,{"$split":["$course_title","("]}]},
                            {"$setIntersection":[keyword,{"$split":["$course_title",")"]}]}

                            ]


                            },
                    "_des":{"$setUnion":[
                            {"$setIntersection":[keyword,{"$split":["$course_description"," "]}]},
                            {"$setIntersection":[keyword,{"$split":["$course_description",","]}]},
                            {"$setIntersection":[keyword,{"$split":["$course_description","."]}]},
                            {"$setIntersection":[keyword,{"$split":["$course_description","?"]}]},
                            {"$setIntersection":[keyword,{"$split":["$course_description",":"]}]},
                            {"$setIntersection":[keyword,{"$split":["$course_description","'"]}]},
                            {"$setIntersection":[keyword,{"$split":["$course_description","\""]}]},
                            {"$setIntersection":[keyword,{"$split":["$course_description","/"]}]},
                            {"$setIntersection":[keyword,{"$split":["$course_description","\\"]}]},
                            {"$setIntersection":[keyword,{"$split":["$course_description","&"]}]},
                            {"$setIntersection":[keyword,{"$split":["$course_description","+"]}]},
                            {"$setIntersection":[keyword,{"$split":["$course_description","-"]}]},
                            {"$setIntersection":[keyword,{"$split":["$course_description","="]}]},
                            {"$setIntersection":[keyword,{"$split":["$course_description","*"]}]},
                            {"$setIntersection":[keyword,{"$split":["$course_description","!"]}]},
                            {"$setIntersection":[keyword,{"$split":["$course_description","("]}]},
                            {"$setIntersection":[keyword,{"$split":["$course_description",")"]}]}

                            ]

                        },
                     
                    "course_code":1, "semester_time":1,"lecture_section_info":1, "nonlecture_section_info":1}
                },
                {
                    "$unwind":"$lecture_section_info"
                },
                {
                    "$unwind":"$nonlecture_section_info"
                },
                {
                    "$project":{
                        "_lremark":{
                            "$setUnion":[
                            {"$setIntersection":[keyword,{"$split":["$lecture_section_info.remarks"," "]}]},
                            {"$setIntersection":[keyword,{"$split":["$lecture_section_info.remarks",","]}]},
                            {"$setIntersection":[keyword,{"$split":["$lecture_section_info.remarks","."]}]},
                            {"$setIntersection":[keyword,{"$split":["$lecture_section_info.remarks","?"]}]},
                            {"$setIntersection":[keyword,{"$split":["$lecture_section_info.remarks",":"]}]},
                            {"$setIntersection":[keyword,{"$split":["$lecture_section_info.remarks","'"]}]},
                            {"$setIntersection":[keyword,{"$split":["$lecture_section_info.remarks","\""]}]},
                            {"$setIntersection":[keyword,{"$split":["$lecture_section_info.remarks","/"]}]},
                            {"$setIntersection":[keyword,{"$split":["$lecture_section_info.remarks","\\"]}]},
                            {"$setIntersection":[keyword,{"$split":["$lecture_section_info.remarks","&"]}]},
                            {"$setIntersection":[keyword,{"$split":["$lecture_section_info.remarks","+"]}]},
                            {"$setIntersection":[keyword,{"$split":["$lecture_section_info.remarks","-"]}]},
                            {"$setIntersection":[keyword,{"$split":["$lecture_section_info.remarks","="]}]},
                            {"$setIntersection":[keyword,{"$split":["$lecture_section_info.remarks","*"]}]},
                            {"$setIntersection":[keyword,{"$split":["$lecture_section_info.remarks","!"]}]},
                            {"$setIntersection":[keyword,{"$split":["$lecture_section_info.remarks","("]}]},
                            {"$setIntersection":[keyword,{"$split":["$lecture_section_info.remarks",")"]}]}

                            ]
                    },





                    "_nlremark":{
                        "$setUnion":[
                            {"$setIntersection":[keyword,{"$split":["$nonlecture_section_info.remarks"," "]}]},
                            {"$setIntersection":[keyword,{"$split":["$nonlecture_section_info.remarks",","]}]},
                            {"$setIntersection":[keyword,{"$split":["$nonlecture_section_info.remarks","."]}]},
                            {"$setIntersection":[keyword,{"$split":["$nonlecture_section_info.remarks","?"]}]},
                            {"$setIntersection":[keyword,{"$split":["$nonlecture_section_info.remarks",":"]}]},
                            {"$setIntersection":[keyword,{"$split":["$nonlecture_section_info.remarks","'"]}]},
                            {"$setIntersection":[keyword,{"$split":["$nonlecture_section_info.remarks","\""]}]},
                            {"$setIntersection":[keyword,{"$split":["$nonlecture_section_info.remarks","/"]}]},
                            {"$setIntersection":[keyword,{"$split":["$nonlecture_section_info.remarks","\\"]}]},
                            {"$setIntersection":[keyword,{"$split":["$nonlecture_section_info.remarks","&"]}]},
                            {"$setIntersection":[keyword,{"$split":["$nonlecture_section_info.remarks","+"]}]},
                            {"$setIntersection":[keyword,{"$split":["$nonlecture_section_info.remarks","-"]}]},
                            {"$setIntersection":[keyword,{"$split":["$nonlecture_section_info.remarks","="]}]},
                            {"$setIntersection":[keyword,{"$split":["$nonlecture_section_info.remarks","*"]}]},
                            {"$setIntersection":[keyword,{"$split":["$nonlecture_section_info.remarks","!"]}]},
                            {"$setIntersection":[keyword,{"$split":["$nonlecture_section_info.remarks","("]}]},
                            {"$setIntersection":[keyword,{"$split":["$nonlecture_section_info.remarks",")"]}]}

                            ]
                },  





                    "_title":1, "_des":1,"course_code":1, "semester_time":1
                    }

                },

                {
                    "$project":{ "n_title": {"$size": "$_title"}, "n_des":{"$size":"$_des"},
                     "n_l":{"$size":"$_lremark"},"n_nl":{"$size":"$_nlremark"},"course_code":1, "semester_time":1  }  
                    
                },
                

                {"$match":
                    {
                        "$or":
                        [
                            {"n_title": {"$gte":1}},
                            {"n_des": {"$gte":1}},
                            {"n_l": {"$gte":1}},
                            {"n_nl": {"$gte":1}}
                        ]
                    
                    }
                },
                {"$project": {"course_code":1,"semester_time":1}},

                {
                    "$group":{"_id":"$course_code", "latest_time": {"$max": "$semester_time"}}
                    
                },

                {
                
                    "$project": {"course_code": "$_id", "latest_time": 1}
                
                },

                {
                "$lookup":{
                    "localField": "course_code",
                    "from": "course",
                    "foreignField": "course_code",
                    "as": "course_list"
                
                }
            
            },

            {
                "$unwind":"$course_list"
            
            },
            
            {
                "$project":{ "_id":0, "Course_Code":"$course_code", "Course_Title":"$course_list.course_title",  "No_of_Units": "$course_list.units", 
                    "section_list":{"$setUnion":["$course_list.lecture_section_info","$course_list.nonlecture_section_info"]},  
                    "time_equal": {"$eq": ["$latest_time", "$course_list.semester_time"]}
                }
            },

            {"$match": {"time_equal": True}},
            {"$sort": SON([("Course_Code", 1)])},
            {"$project": {"_id": 0, "time_equal":0}}

            ]   

        )
    except pymongo.errors.ConnectionFailure as error:
        print(error)
    
    
    result = list(result)
    if(len(result) > 0):
        print("The list of courses are as follows: \n")
        
        count = 1
        for course in result:
            print("No {:d}".format(count))
            pprint.pprint(course)
            print("\n")
            count+=1
    else:
        print("No matched record is found")
    


'''
Search for a list of courses, each of which has a lecture section (e.g., “L1” and “L2”) in
a time slot, says match_ts, between the input parameters : start_ts (inclusively) and end_ts (inclusively)
where the number of students in the waiting list of this lecture section is greater than
or equal to input real number, f, multiplied by the number of students enrolled in this lecture section in
that time slot.

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

##Without Satisfied Attribute

def size_search(f, start_ts, end_ts):
    
    try :
        client = MongoClient("mongodb://localhost:27017")
        
        db = client["university"]


        db.course.aggregate(
        [   
            {"$unwind":"$lecture_section_info"},

            {
                "$match":{
                    "$and": [{"semester_time":{"$lte": end_ts}},   
                        {"semester_time":{"$gte": start_ts}}]
                }
            },
            
            {   "$project": {
                    "_id":0, "course_code":1, "course_title":1, "units":1 ,"Timeslots":"$semester_time" ,
                    "lecture_section_info":1, "nonlecture_section_info":1,
                    "size_match": {"$gte":["$lecture_section_info.wait",{"$multiply": ["$lecture_section_info.enrol",f]
                    }] } 
                }
            },

            {"$match": {"size_match": True}},

            {
                    "$group":{"_id":"$course_code", "Matched_Timeslot": {"$max": "$Timeslots"}}
                    
            },

            {"$project": {"_id":0, "course_code":"$_id", "Matched_Timeslot":1}
            },
            
            {"$out": "temp2"}
            ]
            
        )

        result = db.course.aggregate(
        [
           {
            "$lookup":{
                "localField": "course_code",
                "from": "temp2",
                "foreignField": "course_code",
                "as": "course_list"
            
            }
        
        },

        {
            "$unwind":"$course_list"
        
        },
        
        
        {
            "$project":{ "_id":0, "course_code":1,"course_title":1, "units":1, 
                "section_list":{"$setUnion":["$lecture_section_info","$nonlecture_section_info"]},  
                
                "course_list.Matched_Timeslot": 1
            }
        },


        {"$project": {"_id": 0, "course_code":1,"course_title":1, "units":1, "Matched_Timeslot":"$course_list.Matched_Timeslot",
         "section_list.section_id":1,"section_list.section_name":1,"section_list.section_specific_info":1, "section_list.quota":1, 
         "section_list.enrol":1, "section_list.avail":1, "section_list.wait":1, "section_list.Satisfied": ""
            }
            
        },


        {"$unwind": "$section_list"},
        {
            "$project": {"_id": 0, "course_code":1,"course_title":1, "units":1,  "Matched_Timeslot":1, "section_list.section_id":1,
            "section_list.section_name":1,"section_list.section_specific_info":1, "section_list.quota":1, "section_list.enrol":1, 
            "section_list.avail":1, "section_list.wait":1, "section_list.Satisfied":
            {"$cond":{"if":{"$gte":["$section_list.wait",{"$multiply": ["$section_list.enrol",f] }] 
            },"then": "Yes", "else": "No" } }
            }

        },

        { "$group": {
        "_id": "$course_code",
       "Course_Code":{"$first": "$course_code"},
        "Course_Title": {"$first": "$course_title"} ,
        "Units":  {"$first": "$units" },   
        "Section_List": { "$push": "$section_list" }
        }},

        {"$sort": SON([("Course_Code", 1)])},

        {"$project": {"_id": 0}}
            
    ]
    )
    except pymongo.errors.ConnectionFailure as error:
        print(error)
    
    
    result = list(result)
    if(len(result)):
        print("The list of courses are as follows: \n")
        
        count = 1
        for course in result:
            print("No {:d}".format(count))
            pprint.pprint(course)
            print("\n")
            count+=1
    else:
        print("No matched record is found")

    
    
   

from datetime import datetime

#Interface

def course_search_handler():
    
    print("1. Search by keywords")
    print("2. Search by waiting list size")
    print("3. Cancel")
    
    while(True): 
        search_type = input("Please input your choice: 1-3\n")
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
