#------------------------------------------- START OF LICENSE -----------------------------------------
#tryJson.py
#Copyright (c) Microsoft Corporation
#All rights reserved. 
#Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You #may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 
#
#THIS CODE IS PROVIDED ON AN  *AS IS* BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING #WITHOUT LIMITATION ANY IMPLIED WARRANTIES OR CONDITIONS OF TITLE, FITNESS FOR A PARTICULAR PURPOSE, MERCHANTABLITY OR NON-#INFRINGEMENT. 
#
#See the Apache Version 2.0 License for specific language governing permissions and limitations under the License.
#----------------------------------------------- END OF LICENSE ------------------------------------------
import psycopg2
import pprint
import time
import datetime
from datetime import date, timedelta, datetime
import copy
from rangeset import RangeSet
print "Lets start some anaytics"

'''
#Funnel

# Emails Sent
## Sent email to 18 people
# People clicked on emails
SELECT COUNT(user_id), activities.user_id 
FROM activities 
GROUP BY activities.user_id ORDER BY activities.user_id;


SELECT 
  COUNT(users.name), users.name
FROM 
  public.activities
INNER JOIN public.users 
ON activities.user_id = users."Id" 
GROUP BY users.name


#Count if a person was ever active 

SELECT Count(*) from 
(SELECT 
  COUNT(users.name), users.name
FROM 
  public.activities
INNER JOIN public.users 
ON activities.user_id = users."Id" 
GROUP BY users.name) AS y


# give me all days someone did any activity
select (timestamp::timestamp::date) AS t from activities 
INNER JOIN public.users 
ON activities.user_id = users."Id" 
group by t

# Set goals
# How many people clicked a button
# How many people did do their goals
# How many people sticked to break goals
# How many people acceeded their goals
# Best Team of the day
# Best Person of the day
# How often are pople at the desk
# How often do people react on notifications
'''

users = {}
days = {}
activitiesDbName = "activities"
goalsDbName = "goals"
shift = False

useMDFU = True

if shift == True:
	activitiesDbName = "activitiesshift"
	goalsDbName = "goalsshift"

def daysInUser(cursor):
	print "daysInUser"
	q = "select (timestamp::timestamp::date) AS t from "+activitiesDbName+" INNER JOIN public.users ON "+activitiesDbName+".user_id = users.\"Id\" group by t"
	cursor.execute(q)
	records = cursor.fetchall()
	pprint.pprint(records)
	p = []

	return p


def confertToArea(t, area):

	if area is "nyc":
		return str((t - timedelta(hours=4)).date()) 
	else:
		return str((t - timedelta(hours=7)).date()) 

def moveDateForUser(date, userId):
	
	if useMDFU == True:
		print "useMDFU"
		if userId == 1 or 2 or 3 or 4 :
			if date == "2014-08-23":
				date = "2014-08-18"
			elif date == "2014-08-24":
				date = "2014-08-19"
			elif date == "2014-08-25":
				date = "2014-08-20"
			elif date == "2014-08-26":
				date = "2014-08-21"
			elif date == "2014-08-27":
				date = "2014-08-22"

	return date

def daysWherePeopleWhereActive(cursor):
	print "daysWherePeopleWhereActive"
#	q = "select (timestamp::timestamp::date) AS t, users.user_id, location from activities INNER JOIN public.users ON activities.user_id = users.\"Id\" order by t ASC"
#	q = "SELECT dtime, user_id FROM (SELECT  users.user_id, (timestamp -  time '04:00')::timestamp::date as dtime, location, activity_type FROM public.activities INNER JOIN public.users ON activities.user_id = users.\"Id\" WHERE location like 'nyc' union SELECT  users.user_id, (timestamp -  time '07:00')::timestamp::date as dtime, location,activity_type FROM public.activities INNER JOIN public.users ON activities.user_id = users.\"Id\" WHERE location like 'redmond' ) as t order by dtime ASC"
	q = "select timestamp AS t, users.user_id, location from "+activitiesDbName+" INNER JOIN public.users ON "+activitiesDbName+".user_id = users.\"Id\" order by t ASC"

	cursor.execute(q)
	records = cursor.fetchall()
	

	#pprint.pprint(records)	
	for n in records:
		#print n
		#print (n[0] - timedelta(hours=4)) 
		d = confertToArea(n[0], str(n[2]))
		d = moveDateForUser(d, n[1])
		#users[n[2]]["days"][str(n[0])] 
		try:
			users[str(n[1])]["days"][d]
		except:
			users[str(n[1])]["days"][d] = {"active":True}


		try:
			days[d]
		except:
			days[d] = {}
		
		#print users[str(n[1])]["days"][str(n[0])]



	#add at least empty day to each person
	for n in users:

		for a in days:
			try:
				users[n]["days"][a]
			except:
				users[n]["days"][a] = {"active":False}
	
	#p = []
	#return p

def numberOfPeopleActiveAtADay(cursor):
	print "numberOfPeopleActiveAtADay"
	q = "select count(t), t from (select (timestamp::timestamp::date) AS t from "+activitiesDbName+" INNER JOIN public.users ON "+activitiesDbName+".user_id = users.\"Id\" group by t, "+activitiesDbName+".user_id order by t) as k group by t"
	cursor.execute(q)
	records = cursor.fetchall()
	pprint.pprint(records)
	p = []
	return p

def numberOfBreaksPerDay(cursor):
	print "numberOfBreaksPerDay" 
	q = "select (timestamp::timestamp::date) AS t, count(timestamp::timestamp::date) from "+activitiesDbName+" INNER JOIN public.users ON "+activitiesDbName+".user_id = users.\"Id\" where activity_type = 'break' group by t";
	cursor.execute(q)
	records = cursor.fetchall()
	pprint.pprint(records)
	p = []
	return p


def averageNumberObBreaksPerDayAndSumAndPeople(cursor):
	print "averageNumberObBreaksPerDay"

	q = "select allbreaks, allpeople, t, CAST(allbreaks as decimal(10,2))/CAST(allpeople as decimal(10,2)) as averageBreaks from (select (timestamp::timestamp::date) AS t, count(timestamp::timestamp::date) as allbreaks  from "+activitiesDbName+" INNER JOIN public.users ON "+activitiesDbName+".user_id = users.\"Id\" where activity_type = 'break' group by t) as k INNER JOIN (select * from (select count(m) as allpeople, m from (select (timestamp::timestamp::date) AS m from "+activitiesDbName+" INNER JOIN public.users ON "+activitiesDbName+".user_id = users.\"Id\" group by m, "+activitiesDbName+".user_id order by m) as k group by m) as l) as m ON m=t"

	cursor.execute(q)
	records = cursor.fetchall()

	for n in records:
		days[str(n[2])]["breaks"] = n[0]
		days[str(n[2])]["breaks"] = n[0]

	pprint.pprint(records)
	p = []
	return p

def createUserTableObject(cursor):
	print "createUserTableObject"
	q = "select * from users"

	cursor.execute(q)
	records = cursor.fetchall()

	for n in records:
		users[str(n[2])] = {"user_id":n[2], "id":n[0], "team":n[4], "team_id":n[3], "name":n[1], "days":{}}
		#print n

	#pprint.pprint(records)

def addUserGoals(cursor):
	print "addUserGoals"
	q = "select users.user_id, timestamp, goal_type, goal, location FROM "+goalsDbName+" INNER JOIN public.users ON "+goalsDbName+".user_id = users.\"Id\" ORDER BY timestamp ASC;"
	cursor.execute(q)
	records = cursor.fetchall()

	for n in records:
		d = confertToArea(n[1], str(n[4]))
		d = moveDateForUser(d, n[0])

		try:
			users[str(n[0])]["days"][d]
		except:
			users[str(n[0])]["days"][d] = {}


		users[str(n[0])]["days"][d][str(n[2])] = int(n[3])




def addActivities(cursor):
	print "addActivities"
	q = "select users.user_id, timestamp, activity_type, activity_state, name, location from "+activitiesDbName+" INNER JOIN public.users ON "+activitiesDbName+".user_id = users.\"Id\" ORDER BY timestamp ASC"
	cursor.execute(q)
	records = cursor.fetchall()

	for n in records:
		#print users[str(n[0])]["days"][str(n[1])]

		d = confertToArea(n[1], str(n[5]))
		d = moveDateForUser(d, n[0])

		if str(n[2]) == "break":
			#print "break"
			try:
				users[str(n[0])]["days"][d]["breaksum"]
			except:
				users[str(n[0])]["days"][d]["breaksum"] = 0

			users[str(n[0])]["days"][d]["breaksum"] = users[str(n[0])]["days"][d]["breaksum"] + 1

		if str(n[2]) == "robot" and int(n[3]) == 1:
			#print "break"
			try:
				users[str(n[0])]["days"][d]["robotyes"]
			except:
				users[str(n[0])]["days"][d]["robotyes"] = 0

			users[str(n[0])]["days"][d]["robotyes"] = users[str(n[0])]["days"][d]["robotyes"] + 1

		if str(n[2]) == "robot" and int(n[3]) == 0:
			#print "break"
			try:
				users[str(n[0])]["days"][d]["robotno"]
			except:
				users[str(n[0])]["days"][d]["robotno"] = 0

			users[str(n[0])]["days"][d]["robotno"] = users[str(n[0])]["days"][d]["robotno"] + 1

		if str(n[2]) == "robot" and int(n[3]) == -1:
			#print "break"
			try:
				users[str(n[0])]["days"][d]["robotna"]
			except:
				users[str(n[0])]["days"][d]["robotna"] = 0

			users[str(n[0])]["days"][d]["robotna"] = users[str(n[0])]["days"][d]["robotna"] + 1

		if str(n[2]) == "notification":
			#print "break"
			try:
				users[str(n[0])]["days"][d]["notification"]
			except:
				users[str(n[0])]["days"][d]["notification"] = 0

			users[str(n[0])]["days"][d]["notification"] = users[str(n[0])]["days"][d]["notification"] + 1


def turnUserAndDate():
	for n in days:

		for a in users:
			d = users[a]["days"]			
			try:
				days[n][a] = d[n]
			except:
				None	


def pivCSV(values):
	csv = "day, user, name, team, "

	for t in values:
		csv += t+", "

	csv += "\n"

	for n in users:
		#print n

		ddays = users[n]["days"]
		for d in ddays:
			#print d

			#Move days
			#print d
			#copy 19-27 to 10-18
			

			csv += d+", "+n+", "+users[n]["name"]+", "+str(users[n]["team_id"])+", "
			

			for t in values:

				try:
					#print "--- !!!!!"
					#print d[a]
					if t is "active":
						if str(ddays[d][t]) == "True":
							csv += "1"
					else:
						csv += ""+str(ddays[d][t])					
				except:
					#print "--- onoen"
					None

				csv += ", "

			csv += "\n"


	return csv

def drawCSV(values):
	csv = "day, "

	su = []
	for n in users:
		su.append(int(n))
	su.sort()

	for n in su:
		n = str(n)
		for t in values:
			csv += ""+n+"_"+users[n]["name"]+"_"+t+", "

	csv += "\n"

	sd = []
	for n in days:
		sd.append(n)
	sd.sort()

	for n in sd:

		csv += ""+n+", "
		d = days[n]
		#print d
		
		ssd = []
		for a in d:
			ssd.append(int(a))
		ssd.sort()
		#print ssd

		for a in ssd:
			a = str(a)
			#print a
			for t in values:

				try:
					#print "--- !!!!!"
					#print d[a]
					csv += ""+str(d[a][t])
				except:
					#print "--- onoen"
					None

				csv += ", "

		
		csv += "\n"
	
	return csv

def calcUserStats(values):
	print "calcUserStats"
	#print users

	for a in users:
		sortArr = []
		d = users[a]["days"]
		for sd in d:			
			sortArr.append(sd)
		sortArr.sort()
		#print sortArr

		emptyBreakT = None
		emptyStandingTime = None
		emptySittingTime = None
		emptyDeskTime = None
		for s in sortArr:

			if emptyBreakT == None:
				#print "############--- !!!!!"
				#print users[a]["days"]
				emptyBreakT = users[a]["days"][s]["breaks_day"]

			try: 
				emptyBreakT = users[a]["days"][s]["breaks_day"]
			except:
				users[a]["days"][s]["breaks_day"] = emptyBreakT
				#print "none"
				None


			if emptyStandingTime == None:
				#print "############--- !!!!!"
				#print users[a]["days"]
				emptyStandingTime = users[a]["days"][s]["standing_time"]

			try: 
				emptyStandingTime = users[a]["days"][s]["standing_time"]
			except:
				users[a]["days"][s]["standing_time"] = emptyStandingTime
				#print "none"
				None

			if emptySittingTime == None:
				#print "############--- !!!!!"
				#print users[a]["days"]
				emptySittingTime = users[a]["days"][s]["sitting_time"]

			try: 
				emptySittingTime = users[a]["days"][s]["sitting_time"]
			except:
				users[a]["days"][s]["sitting_time"] = emptySittingTime
				#print "none"
				None

			if emptyDeskTime == None:
				#print "############--- !!!!!"
				#print users[a]["days"]
				emptyDeskTime = users[a]["days"][s]["desk_time"]

			try: 
				emptyDeskTime = users[a]["days"][s]["desk_time"]
			except:
				users[a]["days"][s]["desk_time"] = emptyDeskTime
				#print "none"
				None

			#print emptyBreakT


			try:
				users[a]["days"][s]["breaks_achieved_day"] = float(users[a]["days"][s]["breaksum"]*100)/float(emptyBreakT)
			except:
				users[a]["days"][s]["breaks_achieved_day"] = 0

			try:
				users[a]["days"][s]["breaks_short"] = emptyBreakT - users[a]["days"][s]["breaksum"]
			except:
				users[a]["days"][s]["breaks_short"] = emptyBreakT

			
			#print users[a]["name"], users[a]["user_id"], s, users[a]["team"]

			presence_rs = make_rangeset(cursor, users[a]["user_id"], users[a]["team"], 'presence', s)
			standing_rs = make_rangeset(cursor, users[a]["user_id"], users[a]["team"], 'standing', s)
			notification_rs = make_rangeset(cursor, users[a]["user_id"], users[a]["team"], 'notification', s)
			mutual_overlaps = RangeSet.mutual_overlaps(presence_rs, standing_rs, notification_rs, minimum=3)

			actual_standing_time = mutual_overlaps.measure()
			if actual_standing_time != 0:
				actual_standing_time = actual_standing_time.total_seconds() / 3600

			actual_deks_time = RangeSet.mutual_overlaps(presence_rs, notification_rs).measure()
			if actual_deks_time != 0:
				actual_deks_time = actual_deks_time.total_seconds() / 3600

			#print presence_rs.measure().total_seconds()/ 3600 ## desk time
			#print mutual_overlaps.measure().total_seconds()/ 3600 ## standing time

			users[a]["days"][s]["standing_achieved_time"] = actual_standing_time
			users[a]["days"][s]["desk_achieved_time"] = actual_deks_time
			#print actual_standing_time
			#print actual_deks_time
			##cals desk time and sitting time

			#print s
			#print users[a]["days"][s]

			# goal calculations

			try:
				users[a]["days"][s]["breaks_goal_achievement"] = float(users[a]["days"][s]["breaksum"])/float(emptyBreakT)
			except:
				users[a]["days"][s]["breaks_goal_achievement"] = 0

			try:
				users[a]["days"][s]["standing_goal_achievement"] = float(actual_standing_time)/float(users[a]["days"][s]["standing_time"])
			except:
				users[a]["days"][s]["standing_goal_achievement"] = 0

			users[a]["days"][s]["overall_goal_achievement"] = (users[a]["days"][s]["breaks_goal_achievement"]+users[a]["days"][s]["standing_goal_achievement"])/2


def make_rangeset(cursor, theuser, area, activity_type, beginningofwindow):
	starts = []
	ends = []
	dayStart = datetime.strptime(beginningofwindow, '%Y-%m-%d')
	dayEnd = None

	if area is "nyc":		
		dayStart = dayStart + timedelta(hours=4)
	else:
		dayStart = dayStart + timedelta(hours=7)
	
	dayEnd = dayStart + timedelta(hours=23, minutes=59, seconds=59)

	#print dayStart
	#print dayEnd
	q = "select (timestamp::timestamp::date) AS t, activity_state, timestamp, * from "+activitiesDbName+" INNER JOIN public.users ON "+activitiesDbName+".user_id = users.\"Id\" WHERE activity_type = '"+activity_type+"' and timestamp > '"+str(dayStart)+"' and timestamp < '"+str(dayEnd)+"' and users.user_id = '"+str(theuser)+"' order by timestamp DESC"
	#print q
	cursor.execute(q)
	records = cursor.fetchall()

	#print len(records)
	#print records
	if activity_type == 'notification':
		winsize = timedelta(minutes=45)
		for a in records:
			starts.append(a[2] - winsize)
			ends.append(a[2] + winsize)
	else:
		i = -1
		for a in records:
			i = i + 1
			#print a
			if i == 0 and a[1] == 1: ends.append(dayEnd)
			if a[1] == 1: starts.append(a[2])
			elif a[1] == 0: ends.append(a[2])
			if i == len(records) - 1 and a[1] == 0: starts.append(dayStart)
	
	pairs = zip(tuple(starts),tuple(ends))


	# print len(pairs)
	# print pairs
	if len(pairs) > 0:
		therangeset = RangeSet.mutual_union(pairs[0])
		for i in range(1,len(pairs)):
			therangeset = therangeset.union(RangeSet.mutual_union(pairs[i]))
	elif activity_type == 'notification':
		therangeset = RangeSet(dayEnd,dayEnd)
	elif activity_type != 'notification':

		q = "select (timestamp::timestamp::date) AS t, activity_state, timestamp, * from "+activitiesDbName+" INNER JOIN public.users ON "+activitiesDbName+".user_id = users.\"Id\" WHERE activity_type = '"+activity_type+"' and timestamp <= '"+str(dayStart)+"' and users.user_id = '"+str(theuser)+"' order by timestamp DESC LIMIT 1"
		cursor.execute(q)
		records = cursor.fetchall()
		currentstate = None

		if len(records) > 0:
			currentstate = records[0]

		if currentstate == None: currentstate = 0
		else: currentstate = currentstate[1]

		now = dayEnd
		if currentstate == 1:
			therangeset = RangeSet(dayStart,now)
		else:
			therangeset = RangeSet(now,now)
		# print therangeset
	return therangeset
    

def main():
	#Define our connection string
	conn_string = "host='localhost' dbname='fidget' user='fidgetbackup' password='Quitch641backup'"
 
	# print the connection string we will use to connect
	print "Connecting to database\n	->%s" % (conn_string)
 
	# get a connection, if a connect cannot be made an exception will be raised here
	conn = psycopg2.connect(conn_string)
 
	# conn.cursor will return a cursor object, you can use this cursor to perform queries

	global cursor
	cursor = conn.cursor()
	print "Connected!\n"

	t = True
	if t:
		createUserTableObject(cursor)
		daysWherePeopleWhereActive(cursor)
		addUserGoals(cursor)
		addActivities(cursor)

		calcUserStats(cursor)
		
		

		turnUserAndDate()
		#pprint.pprint(users)
		#pprint.pprint(days)

		d = pivCSV(["active","notification", "robotyes", "robotno", "robotna", "standing_time", "sitting_time", "desk_time", "standing_achieved_time", "sitting_achieved_time", "desk_achieved_time", "breaks_day",  "breaksum", "breaks_short", "breaks_achieved_day", "breaks_goal_achievement", "standing_goal_achievement", "overall_goal_achievement"])

		#print d
		f = open('workfile.csv', 'w')
		f.write(d)
		

	#print make_rangeset(cursor, 3, "nyc", "standing", "2014-08-06")
	#print make_rangeset(cursor, 3, "nyc", "presence", "2014-08-06")
	
	presence_rs = make_rangeset(cursor, 3, "nyc", 'presence', "2014-08-06")
	standing_rs = make_rangeset(cursor, 3, "nyc", 'standing', "2014-08-06")
	mutual_overlaps = RangeSet.mutual_overlaps(presence_rs, standing_rs)
	actual_standing_time = mutual_overlaps.measure()
	if actual_standing_time != 0:
		actual_standing_time = actual_standing_time.total_seconds() / 3600
	
	print presence_rs.measure().total_seconds()/ 3600 ## desk time
	print mutual_overlaps.measure().total_seconds()/ 3600 ## standing time
	

if __name__ == "__main__":
	main()
