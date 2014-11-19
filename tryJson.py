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
import cjson
import random
import smtplib
import argparse
import copy
from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule
from pprint import pprint
import time
import cherrypy
import requests
from threading import Thread

# Global variable to store the ReactToTouch module instance
memory = None
currentTread = None
userQueue = []
iAmGlobal = None
smtpserver = None
emailto = 't-nolieb@microsoft.com'
emailfrom = 'j_brandstetter@weristin.at'

def sendEmailAndLogg(trackServerNr, user_id):

	header = 'To:' + emailto + '\n' + 'From: ' + emailfrom + '\n' + 'Subject:robot talking! \n'
	msg = header + '\n searious activities here!!! \n\n'
	smtpserver.sendmail(emailfrom, emailto, msg)  

	payload= {'robot' : trackServerNr}
	print payload
	
	try:
		requests.post('http://fidgetvm.cloudapp.net//'+user_id+'/set_activity_state/',data=payload)
	except requests.exceptions.RequestException as e:    # This is the correct syntax
		print e

	


class TalkingBot():

	def goToPerson(self,name):

		self.motion.wakeUp()
		self.posture.goToPosture("StandInit",0.5)

		#set camera to center
		self.motion.setAngles("HeadYaw", 0, 0.5)
		self.motion.setAngles("HeadPitch", 0, 0.5)

		self.video.setActiveCamera(0)
		if True:
			calCount = 2
			while True and calCount > 0:
				
				data = self.memProxy.getData("LandmarkDetected")
				#print data
				l = len(data)
				if l > 0:
					d = data[1]
					mid = d[0][1][0]
					alpha = d[0][0][1]
					beta = d[0][0][2]
					#print beta
					#print d[0][0][3]
					if mid == 85:
						self.motion.moveTo(0,0,alpha)
						calCount = calCount - 1
					print str(mid) + " ---- " + str(beta) + " ---- " + str(d[0][0][3]) 
				time.sleep(0.2)


		self.video.setActiveCamera(1)

		self.motion.moveTo(0,0,0.5)
		self.motion.waitUntilMoveIsFinished();

		self.motion.moveTo(0.8,0,0)
		self.motion.waitUntilMoveIsFinished();

		if True:
			calCount = 2
			while True and calCount > 0:
				
				data = self.memProxy.getData("LandmarkDetected")
				#print data
				l = len(data)
				if l > 0:
					d = data[1]
					mid = d[0][1][0]
					alpha = d[0][0][1]
					beta = d[0][0][2]
					#print beta
					#print d[0][0][3]
					
					self.motion.moveTo(0,0,alpha)
					calCount = calCount - 1
					print str(mid) + " ---- " + str(beta) + " ---- " + str(d[0][0][3]) 
				time.sleep(0.2)


		self.motion.moveTo(0.30,0,0)
		self.motion.waitUntilMoveIsFinished();

		self.motion.moveTo(0.,0,-0.8)
		self.motion.waitUntilMoveIsFinished();

		#motion.moveTo(0.0,0,0,1)
		#motion.waitUntilMoveIsFinished();
		#video.setActiveCamera(1)

		##walk a bit back
		#motion.moveTo(2,0,0)
		#motion.waitUntilMoveIsFinished();
		#autonomousMoves.setExpressiveListeningEnabled(True)



	def goBackFromPerson(self,name):
		self.motion.setAngles("HeadYaw", 0, 0.5)
		self.motion.setAngles("HeadPitch", 0, 0.5)
		self.motion.moveTo(0.,0,-2)
		self.motion.waitUntilMoveIsFinished();

		time.sleep(1)
		self.motion.moveTo(0.,0,-1)
		self.motion.waitUntilMoveIsFinished();
		#motion.moveTo(0.,0,-2)
		#motion.waitUntilMoveIsFinished();

		self.motion.moveTo(0.3,0,0)
		self.motion.waitUntilMoveIsFinished();

		self.video.setActiveCamera(0)


		if True:
			calCount = 2
			while True and calCount > 0:
				
				data = self.memProxy.getData("LandmarkDetected")
				#print data
				l = len(data)
				if l > 0:
					d = data[1]
					mid = d[0][1][0]
					alpha = d[0][0][1]
					beta = d[0][0][2]
					#print beta
					#print d[0][0][3]
					if mid == 80:
						self.motion.moveTo(0,0,alpha)
						calCount = calCount - 1
					print str(mid) + " ---- " + str(beta) + " ---- " + str(d[0][0][3]) 

				time.sleep(0.2)

		self.motion.moveTo(0.6,0,0)
		self.motion.waitUntilMoveIsFinished();


		self.motion.rest()

	##############################
	# Function definition is here
	def getRandomText(self, section, subsection):

		return self.data[section][subsection][random.randint(0,len(self.data[section][subsection])-1)].encode("utf-8")
	

	def touchMe(self, value):
		#print "touch Me pleeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeees"
		self.decision = value

			
			


	def wakeRobotUp(self):
		# Wake up robot
		self.motion.wakeUp()


	def runActivities(self, maxTime):
		newRand = True #I mage a new randomizantion algorithm. That should work better. and is way simpler

		if newRand:
			print "newRand"
			random.shuffle(self.maxActivies)
			print self.maxActivies

			#
			startTime = time.time()
			curTime = 0.0
			stayInLoop = True #set this false if next activity would take much too long
			listPost = 0
			print "curTimes: " + str(curTime) + "maxTime: " + str(maxTime)
			while curTime < maxTime and stayInLoop:

				l = self.maxActivies[listPost]

				if l["animation"] is True:
					saying = "^start(" + l["file"] +") " + l["text"] + "^wait(" + l["file"] +") "
					print "use ALSpeach"
					print l["file"]
					print l["text"]
					print saying
					
					self.tts.say(saying.encode("utf-8"))
					
					#tts.say("Hello! ^start(animations/Stand/Gestures/Hey_1) Nice to meet you ^wait(animations/Stand/Gestures/Hey_1)")
				else:
					print "start behavior"
					saying = ""+l["text"]
					beh = ""+l["file"]
					#self.tts.say(saying.encode("utf-8"))
					self.behave.runBehavior(beh.encode("utf-8"))

				listPost = listPost + 1
				curTime = time.time() - startTime
				print "currentTime" + str(curTime)
				#check here if it's a good idea to stay in loop especially if next step takes too long




		else: 	
			# create a list of things to do
			tryToOften = False
			randTest = 4
			currentActivities = []
			while tryToOften is False and randTest > 0:
				c = random.choice (self.maxActivies)

				if maxTime - c["time"] >= 0:
					currentActivities.append(c)
					maxTime = maxTime - c["time"]
				else:
					randTest = randTest - 1

			print currentActivities

			
			##############################
			# Dynamic generation

			# turn of auto mode/nao life?
			for l in currentActivities:
				checkTime = time.time()
				if l["animation"] is True:
					saying = "^start(" + l["file"] +") " + l["text"] + "^wait(" + l["file"] +") "
					print "use ALSpeach"
					print l["file"]
					print l["text"]
					print saying
					
					tts.say(saying.encode("utf-8"))
					
					#tts.say("Hello! ^start(animations/Stand/Gestures/Hey_1) Nice to meet you ^wait(animations/Stand/Gestures/Hey_1)")
				else:
					print "start behavior"

				checkTime = time.time()-checkTime
				sleepTime = l["time"] - checkTime
				print "checkTime: " + str(checkTime)

				if sleepTime > 0.0:
					print "sleep: " + str(sleepTime)
					time.sleep(sleepTime)



	
	#motion.rest()
	#return

	def orientTo(self,num):
		self.motion.wakeUp()
		startAng = 2.07
		
		count = 0
		found = False
		saveFound = None
		self.motion.setAngles("HeadPitch", 0, 0.5)
		self.motion.setAngles("HeadYaw", startAng, 0.5)
		size = None
		data = None
		while startAng > -1.85  and not found:
			time.sleep(2)
			self.motion.setAngles("HeadYaw", startAng, 0.5)
			self.motion.waitUntilMoveIsFinished();
			time.sleep(0.5)
			data = self.memProxy.getData("LandmarkDetected")
			l = None
			if data is not None:
				l = len(data)
			if data is not None and l > 1:
				mid = data[1][0][1][0]
				size = data[1][0][0][3]
				print mid
				print size
				if mid == num:
					found = True
					saveFound = data[1][0]

			if not found:
				startAng = startAng - 0.2

		if not found:
			return None

		startAng = self.motion.getAngles("HeadYaw", True)[0]
		curMark = data[1][0][0][1]
		print startAng
		print curMark
		correct = (startAng + curMark)
		correct = startAng
		print correct
		self.motion.moveTo(0,0,correct) #about 90 deg
		self.motion.waitUntilMoveIsFinished();
		calCount = 2
		self.motion.setAngles("HeadPitch", 0, 0.5)
		self.motion.setAngles("HeadYaw", 0, 0.5)
		size = None
		exi = 0
		while True and calCount > 0 and exi < 10:
			
			data = self.memProxy.getData("LandmarkDetected")
			#print data
			l = len(data)
			if l > 0:
				d = data[1]
				mid = d[0][1][0]
				alpha = d[0][0][1]
				beta = d[0][0][2]
				size = d[0][0][3]
				#print beta
				#print d[0][0][3]
				if mid == num:
					self.motion.moveTo(0,0,alpha)
				calCount = calCount - 1
				print str(mid) + " ---- " + str(beta) + " ---- " + str(d[0][0][3]) 

			else:
				exi = exi +1
			time.sleep(0.2)

		return size

	def getDist(self, size):
		print "site:" + str(size)
		if size > 0.091 and size < 0.117:
			return 0.88-0.2
		elif  size > 0.117 and size < 0.113:
			return 0.635-0.2
		elif  size > 0.113 and size < 0.3:
			return 0.381-0.2


		return x



	def walkTo(self, user, toUser):


		self.motion.setAngles("HeadPitch", 0, 0.5)
		self.motion.setAngles("HeadYaw", 0, 0.5)
		print "'''''''''''''''''''''''' start '''''''''''''''''''"
		print "user: " + str(user) + "toUser: " + str(toUser)

		if toUser:

			if user == 1:	
				self.motion.moveTo(0.3,0,0) #about 90 deg
				self.motion.waitUntilMoveIsFinished();

				self.motion.moveTo(0,0,0.5) #about 90 deg
				self.motion.waitUntilMoveIsFinished();


			elif user == 2:
				self.motion.moveTo(0.3,0,0) #about 90 deg
				self.motion.waitUntilMoveIsFinished();

				self.motion.moveTo(0,0,-0.5) #about 90 deg
				self.motion.waitUntilMoveIsFinished();


			elif user == 3:
				self.motion.moveTo(0.3,0,0) #about 90 deg
				self.motion.waitUntilMoveIsFinished();

				self.motion.moveTo(0,0,2) #about 90 deg
				self.motion.waitUntilMoveIsFinished();
				time.sleep(2)


			elif user == 4:
				
				self.motion.moveTo(0.3,0,0) #about 90 deg
				self.motion.waitUntilMoveIsFinished();

				self.motion.moveTo(0,0,-2) #about 90 deg
				self.motion.waitUntilMoveIsFinished();
				time.sleep(2)

		else:
			if user == 1:		
				self.motion.moveTo(0,0,1.5) #about 90 deg
				self.motion.waitUntilMoveIsFinished();
				time.sleep(1.5)
				self.motion.moveTo(0,0,1) #about 90 deg
				self.motion.waitUntilMoveIsFinished();
				time.sleep(1.5)

			elif user == 2:
				self.motion.moveTo(0,0,-1.5) #about 90 deg
				self.motion.waitUntilMoveIsFinished();
				time.sleep(1.5)
				self.motion.moveTo(0,0,-1.5) #about 90 deg
				self.motion.waitUntilMoveIsFinished();
				time.sleep(1.5)

			o = self.orientTo(80)
			dist = 0
			if o is not None:
				dist = self.getDist(o)

			print "walk Back dist: " + str(dist)

			self.motion.moveTo(dist,0,0) #about 90 deg
			self.motion.waitUntilMoveIsFinished();

			self.motion.moveTo(0,0,1.5) #about 90 deg
			self.motion.waitUntilMoveIsFinished();
			time.sleep(2)
			self.motion.moveTo(0,0,1.5) #about 90 deg
			self.motion.waitUntilMoveIsFinished();
			time.sleep(2)


	def __init__(self, robotIP, PORT, participantName, user_id, volume):

		global iAmGlobal
		iAmGlobal = self
		print iAmGlobal
		print participantName
		##############################
		# connec to NAO

		#add self to touch events
		#global reactToTouch
		#reactToTouch.setThread(self)
		
		self.decision = None
		self.robotIP = robotIP
		self.PORT = PORT
		self.participantName = participantName
		self.volume = volume

		self.tts  = ALProxy("ALAnimatedSpeech", robotIP, PORT)
		self.motion = ALProxy("ALMotion", robotIP, PORT)
		self.posture = ALProxy("ALRobotPosture", robotIP, PORT)
		self.vol = ALProxy("ALAudioDevice", robotIP, PORT)
		self.video = ALProxy("ALVideoDevice", robotIP, PORT)
		self.autonomousMoves = ALProxy("ALAutonomousMoves", robotIP, PORT)
		self.compass = ALProxy("ALVisualCompass", robotIP, PORT)
		self.markProxy = ALProxy("ALLandMarkDetection", robotIP, PORT)
		self.memProxy = ALProxy("ALMemory", robotIP, PORT)
		self.behave = ALProxy("ALBehaviorManager", robotIP, PORT)
		
		self.markProxy.subscribe("Test_LandMark", 500, 0.0 )
		#json_data=open('randomSeceneDataSet.json')
		#data = json.load(json_data)
		self.data = cjson.parse_json('randomSeceneDataSet.json')
		self.motion.setExternalCollisionProtectionEnabled("All", False)
		self.motion.setOrthogonalSecurityDistance(0.0)
		self.motion.setTangentialSecurityDistance(0.0)
		self.autonomousMoves.setExpressiveListeningEnabled(False)
		#print(data)


		#ReactToTouch.setThread(self)

		self.wakeRobotUp()
		self.vol.setOutputVolume(volume)
		#self.goToPerson(str(participantName))
		self.walkTo(int(user_id), True)
		


		##############################
		# Activity should be later. This is just for now
		
		self.data["activity"]
		self.maxActivies = []


		for a in self.data["activity"]:
			
			t = {
				"name":a["name"],
				"animation":a["animation"],
				"file":a["file"],
				"time":a["time"],
				"text":None
			}

			if a["animation"] is True:
				

				oneSay= True

				if oneSay is True:
					b = random.choice (a["namings"])
					if t["time"] < b["time"]:
						t["time"] = b["time"]

					t["text"] = b["text"]
					self.maxActivies.append(copy.copy(t))

				else:
					for b in a["namings"]:
						#print b["text"]
						if t["time"] < b["time"]:
							t["time"] = b["time"]

						t["text"] = b["text"]
						#print t["text"]
						self.maxActivies.append(copy.copy(t))


			else:
				#print a["file"]
				t["time"] = a["time"]
				t["text"] = a["namings"][0]["text"]
				self.maxActivies.append(t)

		

	


		##############################
		# Intro
		hiPlusName = self.getRandomText("intro","hiPlusName")
		hiPlusName = hiPlusName.replace("{NAME}" ,participantName)


		self.tts.say(hiPlusName);
		print hiPlusName

		whatRobotDoes = self.getRandomText("intro","whatRobotDoes")
		self.tts.say(whatRobotDoes);
		print whatRobotDoes

		askForJoining = self.getRandomText("intro","askForJoining")
		self.tts.say(askForJoining);
		print askForJoining


		##############################
		# Wait for answer
		#accept = True
		self.posture.goToPosture("StandZero",0.5)
		time.sleep(2)
		self.decision = None
		#a = 1

		#wee could read here directyl from ALMemory not
		#while self.decision is None:
			#print "wait for decision"
			#print self.decision
			#time.sleep(1)
			#a =1
			#pass

		yesNoThresh = 1
		touch = ALProxy("ALTouch", robotIP, PORT)
		start = time.time() + 30
		threshYes  = 0
		threshNo = 0
		print "and start"
		while start > time.time() and threshYes < yesNoThresh and threshNo < yesNoThresh:
			t = touch.getStatus()
			#print t
			if  t[15][1] or t[16][1]:
				print t[14]
				print t[15]
				print t[16]
				print random.random() 
				print "-----------"
				threshYes = threshYes + 1
			else:
				if  t[18][1] or t[19][1]:
					print t[17]
					print t[18]
					print t[19]
					print random.random() 
					print "-----------"
					threshNo = threshNo + 1
				else:
					threshYes = 0
					threshNo = 0

		print str(threshYes) + "---" + str(threshNo)

		trackServerNr = 0
		if threshYes == yesNoThresh:
			print "yes"
			self.decision = True
			trackServerNr = 1
		else:
			if threshNo == yesNoThresh:
				print "no"
				self.decision = None
				trackServerNr = 0
			else:
				print "timeout"
				self.decision = None
				trackServerNr = -1


		#Thread(target = sendEmailAndLogg, args = (trackServerNr, user_id)).start()


		if self.decision:
			beeingHappy = self.getRandomText("acceptIntro","beeingHappy")
			self.tts.say(beeingHappy);
			print beeingHappy
			whatHumanShouldDo = self.getRandomText("acceptIntro","whatHumanShouldDo")
			self.tts.say(whatHumanShouldDo);
			print whatHumanShouldDo
		else:
			declineSent = self.getRandomText("declineIntro","declineSent")
			self.tts.say(declineSent);
			self.vol.setOutputVolume(0)
			print declineSent
			# start activity but silent


		##############################
		# Create Activity here
		
		self.runActivities(30.001)

		##############################
		# We are done
		doneSentence = self.getRandomText("done","doneSentence")
		self.tts.say(doneSentence);
		self.tts.say("Don't forget to indicate your break on your system!");
		print doneSentence


		##############################
		# Ask if extras are wanted?
		#extraSentence = getRandomText("extra","extraSentence")
		#tts.say(extraSentence);
		#print extraSentence


		##############################
		# accept extra
		# GOTO Wait for answer and set accept = True

		##############################
		# decline extra
		# we can use decline sentence abint
		#declineExtraSent = getRandomText("declineIntro","declineSent")
		#tts.say(declineExtraSent);
		#print declineExtraSent


		# Go to rest position
		#self.motion.rest()
		self.vol.setOutputVolume(15)

		#self.goBackFromPerson(str(participantName))
		self.walkTo(int(user_id), False)	
		self.motion.rest()


		try:
			sC = cjson.parse_json('config.json')
			gmail_user = sC["user"]
			gmail_pwd = sC["password"]
			smtpserver = smtplib.SMTP(sC["serverName"],587)
			smtpserver.ehlo()
			smtpserver.starttls()
			smtpserver.ehlo
			smtpserver.login(gmail_user, gmail_pwd)

			header = 'To:' + emailto + '\n' + 'From: ' + emailfrom + '\n' + 'Subject:robot talking! \n'
			msg = header + '\n searious activities here!!! \n\n'
			smtpserver.sendmail(emailfrom, emailto, msg)  
		except :    # This is the correct syntax
			print "Problem with sending an email"


		payload= {'robot' : trackServerNr}
		print payload
		
		try:
			requests.post('http://fidgetvm.cloudapp.net/'+user_id+'/set_activity_state/',data=payload)
		except :    # This is the correct syntax
			print "Saving to DB did not realy work"

		
		time.sleep(300) #wait 5minutes

		userQueue.pop(0)
		iAmGlobal = None
		if len(userQueue) > 0:
			global currentTread
			currentTread = Thread(target = newThread, args = (robotIP, PORT, str(userQueue[0]["name"]), str(userQueue[0]["user_id"]), volume))
			currentTread.start()




cherrypy.server.socket_host = '0.0.0.0'



def newThread (robotIP, PORT, participantName, user_id, volume):

	TalkingBot(robotIP, PORT, participantName, user_id, volume)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559,
                        help="Robot port number")
    parser.add_argument("--name", type=str, default="Brandi",
                        help="Name of the participant")
    parser.add_argument("--vol", type=int, default=35,
                        help="Speech volume")


    args = parser.parse_args()

    


    class HelloWorld(object):
	    @cherrypy.expose
	    def index(self, a='', user_id='1', name="1", lord="user"):
	    	print "args: " + name
	    	#main(args.ip, args.port, args.name, args.vol)
	    	
	    	if user_id == "bot":
	    		user_id = "1"

	    	if lord == "server":
		    	if len(userQueue) == 0:
		    		userQueue.append({"name" : name, "user_id":user_id})
		    		global currentTread
		    		currentTread = Thread(target = newThread, args = (args.ip, args.port, str(userQueue[0]["name"]), str(userQueue[0]["user_id"]),  args.vol))
		    		currentTread.start()
		    	else:
		    		userQueue.append({"name" : name, "user_id":user_id})
		    	
		    	print userQueue
		    	print userQueue[0]
		    	print "queueSize: "+ str(len(userQueue))

	    	return "Hello World!4 "+ str(random.random())
	    
	    index.exposed = True


    cherrypy.quickstart(HelloWorld())
   # main(args.ip, args.port, args.name, args.vol)
