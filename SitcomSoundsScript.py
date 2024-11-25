#### Parameters ####
waitToActivate = 60 #how long to wait to activate (in seconds)
entryTime = 120 #how long you have to enter after first being pinged for your song to play. (in seconds)
maxRunTime = 24 #how long should the program run (in hours)
interval = 2   #how long must pass between plays of any person's song (in hours)
people = ["Joe"] #people to include. If empty, everyone is included.


#### Imports ####
import os
import SitcomSoundsFunctions
import pandas
import datetime
import threading
import serial


#wait to activate
os.system('sleep ' + str(waitToActivate))

#### Read in CSV / gather basic info / instantiate variables ####

#read in CSV
df = pandas.read_csv("friends.csv", delimiter = ","
                        #, index_col = 0
                        )

#add column for last play (way in the past so it's no problem)
df['LastPlay'] = "2000-01-01 00:00:00"

#add column for last ping (also way in the past)
df['LastPing'] = "2000-01-01 00:00:00"

#filter on people, if non-empty
if (len(people) > 0):
    df = df.loc[df["Name"].isin(people)]

#get initial time for start of loop
startTime = datetime.datetime.now()                     #this is typed as a datetime
startTimeStr = startTime.strftime("%Y-%m-%d %H:%M:%S")  #this is typed as a string


#get maxRunTime, entryTime and interval as timedeltas
maxRunTimeAsDelta = datetime.timedelta(hours = maxRunTime)
intervalAsDelta = datetime.timedelta(hours = interval)
entryTimeAsDelta = datetime.timedelta(seconds = entryTime)


#### Main Loop ####
#this while loop runs for maxRunTime (specified at top)
while ((datetime.datetime.now() - startTime) < maxRunTimeAsDelta):
    
    #attempt to ping each BlueTooth ID
    for rowNum in df.index:


        #get BTid
        BTid = df.at[rowNum, "BTid"]
        print(BTid)

        #ping BTid
        pingStatus = pingerBTFun(BTid)


        #check if ping was successful
        if (pingStatus == 1):
            print('successful ping')

            #get last play time
            lastPing = df.at[rowNum, "LastPing"]

            #convert lastPlay to a dateTime
            lastPing = datetime.datetime.fromisoformat(lastPing)

            #check if device has already pinged within interval
            if ((datetime.datetime.now() - lastPing) > intervalAsDelta):
                print('ping outside of interval')
                song = df.at[rowNum, "Song"]

                #update LastPing in dataframe
                currentTime = datetime.datetime.now()                    #this is typed as a datetime
                currentTimeStr = currentTime.strftime("%Y-%m-%d %H:%M:%S")  #this is typed as a string
                df.at[rowNum, "LastPing"] = currentTimeStr

                #loop for checking if door is open
                while ((datetime.datetime.now() - currentTime) < entryTimeAsDelta):
                    print('inside while loop')
                    
                    #wait one second
                    os.system('sleep 1')

                    #check if door is open
                    if(doorOpenFun() == 1):

                        #play the song
                        playSoundFun(song)

                        #break from while loop
                        print('about to break')
                        break
                
                print('outside of while loop')
