db.course.insert(
		
		{
			state: "Active"
			course code: “comp 4332”,
			course title:  “big data”,
			units:  3,
			prerequisite: “comp 4223”,
			exclusion: “comp5332” ,
			course description: “good course”,
			section_id: [ 1111, 1112]
		}
)





db.time_slot.insert(
	{
		_time_slot:  new date(“2018-02-11T14:30:00Z”),

		section_info:
			[ 
				{
					section_idection_id: 1111,
					section_name: “l1”,
					quota: 50,
					avail: 40,
					wait: 30,
					enroll: 10,
					remarks: “consent required”,
					period_info:
					[
									{
										date: “01-Feb-2018 - 20-Mar-2018”,
										time:“We09:00am - 10:20am”,
										venue: “rm 1005, lsk bldg (70)”,
										instructor: “Raymond”
									},

									{

										date: “01-Feb-2018 - 20-Mar-2018”,
										time: “Fr09:00am - 10:20am”,
										venue:“rm 1004, lsk bldg (70)”,
										instructor: “Raymond”
									},

						

									{
										
										date: “21-Mar-2018 - 09-May-2018”,
										time: “Tu09:00am - 10:20am”,
										venue: “rm 1007, lsk bldg (70)”),
										instructor: “Wong”
									}
					]
				},
				
				
				
				{
					section_idection_id: 1112,
					section_name: “T1”,
					quota: 50,
					avail: 40,
					wait: 30,
					enroll: 10,
					remarks: “”,
					period_info
					[
									{
										time: “We09:00am - 10:00am”,
										venue: “rm 3333”,
										instructor: “ABC”
									}
					]
				}
			],
			
	}
)
