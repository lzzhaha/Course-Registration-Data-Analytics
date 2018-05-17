import re
import os
import sys
import scrapy
import crawling_util
from datetime import datetime
from datetime import timedelta

from pymongo import MongoClient
import pymongo
#print(sys.path)

class PageSpider(scrapy.Spider):
    name="Page"
    semester_time = None
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #add the path name of crawling_util.py to PYTHONPATH
       
        with open('url.txt', 'r') as u_f:
            self.start_urls = [u_f.read()]
        #print("initiate url:{}".format(self.start_urls))
    
        
    def parse_course_page(self, response):
        
        #Get the time slot. A typical url string http://comp4332.com/trial/2017/Spring/01/26/14/00/subjects/COMP.html
        url_list = response.url.split('/')
        
        month = url_list[-6]
        day = url_list[-5]
        hour = url_list[-4]
        minute = url_list[-3]
        time_str = "2018-{}-{} {}:{}".format(month, day, hour, minute)
        semester_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
        semester_time -= timedelta(hours=8)
        
        try :
            with open('./config-MongoDB.txt', 'r') as f:
                
                client = MongoClient(f.read())
            
            
            
            db=client["university"]
            #parse pages like http://comp4332.com/realistic/2017/Spring/01/25/09/00/subjects/COMP.html
            
            index = 0
            
            list_course = response.xpath("//div[@class = \"course\"]")
            #list_code = response.xpath("//div[@class=\"courseanchor\"]/a[@name]/@name").extract()
            #list_title_credits = response.xpath("//div[@class = \"course\"]/h2/text()").extract()
            for course in list_course:
                temp_course = {}
                
                code = course.xpath("./div[@class=\"courseanchor\"]/a[@name]/@name").extract_first()
                '''
                if(code == "COMP1942" or code.startswith("COMP43") or code.startswith("COMP42") or code.startswith("RMBI")):
                    pass
                else:
                    continue
                '''
                '''
                if(code == "COMP4332"):
                    pass
                else:
                    continue
                '''
                temp_course["code"] = code
                print()
                print(code)
                print()
                
                title_credits = course.xpath("./h2/text()").extract_first()
                
                #what is in the attritbute? how to make them connected with /t?????
                #attributes=response.xpath("//div[@class="courseinfo"]/div[@class="popup attrword"]/div[@class="popupdetail"]")

                
                try:
                    
                    title_c=title_credits.split(" - ", 1)[1]
                    
                    a = title_c.rfind(' (')

                    title = title_c[:a]
                    credit = float(title_c[a+2])
                except ValueError as e:
                    print("Course: {}".format(code))
                    print(e)
                #temp_course["semester"]="2017-18 Spring"
                temp_course["semester_time"] = semester_time
                temp_course["title"]=title
                temp_course["credits"]=credit
                
                attributes= course.xpath("./div[@class=\"courseinfo\"]/div[@class=\"courseattr popup\"]/div[@class=\"popupdetail\"]//tr[th=\"ATTRIBUTES\"]/td/text()").extract()
                
                ########
                #the \t is not dealt with here!!!
                temp_course["attributes"]='\t'.join(attributes)
                exclusion=course.xpath("./div[@class=\"courseinfo\"]/div[@class=\"courseattr popup\"]/div[@class=\"popupdetail\"]//tr[th=\"EXCLUSION\"]/td/text()").extract_first()
                if(exclusion is not None):
                    temp_course["exclusion"]=exclusion.split(', ')
                else:
                    temp_course["exclusion"]=[]
                
                description=course.xpath("./div[@class=\"courseinfo\"]/div[@class=\"courseattr popup\"]/div[@class=\"popupdetail\"]//tr[th=\"DESCRIPTION\"]/td/text()").extract_first()

                temp_course["description"]=description

                
                #Selectors of offerings
                listOfRecord= course.xpath("./table[@class=\"sections\"]//tr[td]")
                #List of section type(lecture or nonLecture) of each offering
                list_sec_type = course.xpath("./table[@class=\"sections\"]//tr[td]/@class").extract()
                
                
                
                

                temp_course["lecture_section_info"]= []
                temp_course["nonlecture_section_info"]= []
                
                offering_idx = -1
                lecture_idx = -1
                nonLecture_idx = -1
                
                is_lecture = False #flag that mark the type of current offering(lecture or nonLecture)
                
                #Every record corresponds to an offering may be a new section or suboffering of a section
                for record in listOfRecord:
                    offering_idx+=1
                    temp_offering = {}
                    
                    if(re.match('^new', list_sec_type[offering_idx])):#new section starts
                        temp_section = {}
                        
                        
                        sectionstr =record.xpath("./td[1]/text()").extract_first()
                        sectionstr_list = sectionstr.split(' (')
                        section_name = sectionstr_list[0]
                        section_id = sectionstr_list[1][:-1]
                        
                        dateAndTime=record.xpath("./td[2]/text()").extract_first()
                        temp_offering['dateAndTime'] = dateAndTime

                        room=record.xpath("./td[3]/text()").extract_first()
                        temp_offering['room'] = room

                        instructors=record.xpath("./td[4]/text()").extract()
                        temp_offering['instructors'] = instructors
                        
                        
                        quota_span = record.xpath("./td[5]/span/text()").extract_first()

                        quota_normal = record.xpath("./td[5]/text()").extract_first()

                        if(quota_normal is None):

                            quota=int(quota_span)
                        else:
                            quota = int(quota_normal)
                        
                        
                        
                        

                        enrol=record.xpath("./td[6]/text()").extract_first()

                        enrol=int(enrol)

                        #avail=record.xpath("//td[7]")
                        wait_strong = record.xpath("./td[8]/strong/text()").extract_first()

                        wait_normal = record.xpath("./td[8]/text()").extract_first()

                        if(wait_normal is None):

                            wait=int(wait_strong)
                        else:
                            wait = int(wait_normal)
                            
                            
                        remarks = record.xpath("./td[9]//div[@class=\'popupdetail\']/text()").extract()
                        temp_section["section name"]=section_name
                        temp_section["section_id"] = section_id
                        temp_section["quota"]=quota
                        temp_section["enrol"]=enrol
                        temp_section["wait"]=wait
                        temp_section['remark'] =remarks
                        temp_section['offerings'] = []
                        temp_section['offerings'].append(temp_offering)
                        
                        if(re.match('^L\d',section_name)):#Lecture 
                            lecture_idx +=1
                            temp_course["lecture_section_info"].append(temp_section)
                            is_lecture = True
                        else:#NonLecture
                            nonLecture_idx +=1
                            temp_course["nonlecture_section_info"].append(temp_section)

                            is_lecture = False
                            
                    else:# another offering in the section
                        
                        
                        dateAndTime=record.xpath("./td[1]/text()").extract_first()
                        temp_offering['dateAndTime'] = dateAndTime

                        room=record.xpath("./td[2]/text()").extract_first()
                        temp_offering['room'] = room

                        instructors=record.xpath("./td[3]/text()").extract()
                        temp_offering['instructors'] = instructors
                        
                        if(is_lecture):
                            temp_course["lecture_section_info"][lecture_idx]["offerings"].append(temp_offering)
                            
                        else:
                            temp_course["nonlecture_section_info"][nonLecture_idx]["offerings"].append(temp_offering)
                        
                        


                #::print(temp_course)
                db.all_courses.insert(temp_course)
                #print("insert: {}".format(temp_course))
                
            client.close()

            #db = client["university"]


        except pymongo.errors.ConnectionFailure as error: 
            print(error)

    
    
    def parse_dept_page(self, response):#parse pages like http://comp4332.com/realistic/2017/Spring/01/25/09/00/
        list_of_depts = response.xpath("//div[@class=\"depts\"]/a[@href]/@href").extract()
        
        for dept in list_of_depts:
            yield response.follow(dept, callback=self.parse_course_page)
            

        
    def parse(self, response): #parse pages like http://comp4332.com/realistic
        print("parse outer-most page:")
        list_of_link = response.xpath("//a[@href]/@href").extract()
        list_of_time = response.xpath("//a[@href]/text()").extract()
        
        
        for link in list_of_link:

            yield response.follow(link, callback=self.parse_dept_page)
            
        #print(list_of_link)

            
    
    
   


