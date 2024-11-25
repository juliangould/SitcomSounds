# SitcomSounds
Personalized songs and sounds when you walk through your door. From Seinfeld bass riffs to baseball walkup music.

## About
I've always thought life looked more fun in a sitcom. Everyone is beautiful, there's always an exciting B plot, and everything works out in the end. But most importantly, there are fun sound cues when people enter rooms. Seinfeld is the gold standard with its iconic bass riffs. This repository is a guide on how to set up these sitcom sounds in your own life. Sounds can be personalized to different people. 

## Hardware
To make this work, you'll need some hardware. Here's what you'll need, as well as the specific ones I bought:
+ A [reed switch](https://www.amazon.com/dp/B089P28K5V?ref=ppx_yo2ov_dt_b_fed_asin_title). This is nothing more than a small magnetic current detector. When a magnet is near the end of the read switch, the circuit opens and no electric current can flow through. But when no magnet is nearby, the circuit is closed;
+ A [serial USB with wires](https://www.amazon.com/dp/B00LODGRV8?ref=ppx_yo2ov_dt_b_fed_asin_title). This little USB plugin basically exposes the internal connections of a USB port. That's not exactly right, but close enough. There are five pins, labeled "3V3", "TXD", "RXD", "GND", and "+5V". You don't need to know what those mean, but just know that the "TXD" pin transmits data out from the port, and the "RXD" pin receives data into the port;
+ A spare Unix laptop to run it on. Unfortunately, this code is currently Unix only;
+ (Optional) USB extender, external speakers, subwoofer, gold audio cables, etc. 

### Setting up the hardware
1) Pick a door that you want to play music. Tape or glue the reed switch to your doorframe on the handle side. Do this inside your room/house/apartment, not outside.
2) Tape or glue a magnet to your door so it nearly touches the reed switch when the door is closed.
3) Using the cables, connect one end of the reed switch to the "RXD" pin of the serial USB adapter, and the other end to the "TXD" pin.
4) Connect your serial USB adapter (and audio system) to your spare laptop. Keep this on a table very near the door --- the laptop **cannot** be far from the door or the system won't work. You may want a USB extender to keep your laptop off of the floor.

## How to use this
Now for the coding side of things.

### Setup
On your computer, first you need to do three things:
+ Make a copy of this repository;
+ Inside the folder, create a new folder called `sounds`. Fill this folder with songs and sounds you want to play as mp3s or other audio files;
+ Edit the `friends.csv` by removing the dummy friends and adding your friends, their bluetooth information, and their song title. More info on `friends.csv` will be given a little later.

Next, you need to make sure you have the following python packages installed:
+ `threading`;
+ `os`;
+ `serial`;
+ `pandas`;
+ `datetime`;
+ `random`.

Finally, make sure you have installed `blueutil` on your computer, [available here](https://github.com/toy/blueutil).

### Running the script
Open `SitcomSoundsScript.py`. At the top of the file, there are five tunable parameters:
+ `waitToActivate`: how long after starting the script before music can begin to play (in seconds). For example, if you want to start the script now, but you're going to be going in and out for the next few minutes, you might set this parameter to "3600" and have an hour before any music starts;
+ `entryTime`: how long someone has to enter after first being pinged for their song to play (in seconds). If someone is detected and does not enter the door within this time period, their song is removed from the queue;
+ `maxRunTime`: how long the script will run (in hours);
+ `interval`: how long must pass between plays of any person's song (in hours). Usually, a character theme will play for their first appearance in an episode, but not every appearance;
+ `people`: who you want to have entry music for on this run of the script. If you leave this list empty, it will default to all people in the `friends.csv`. Names in the list must be the names in the `friends.csv` file. 

After picking your parameters, simply run the script! The rest will take care of itself. 

### Giving someone theme music
To give a friend theme music, you have to do a few things. First, you need to pick a song and add it to the `sounds` folder. Second, you need to add your friend to the CSV file `friends.csv`. This file has three columns:
1) "Name": this is just the name of your friend for lookup purposes;
2) "BTid": this is your friend's phone's bluetooth ID. Bluetooth enabled devices have unique identifiers. On an iPhone, you can find this identifier in settings>general>about>Bluetooth. On an Android, it can be found at settings>system>about_device>Bluetooth. It will be formatted like "XX:XX:XX:XX:XX:XX". If your friends will not share this information with you, the system won't work.
3) "Song": this is just the name of the audio file you picked for them and put in the `sounds` folder.

## Wait... how does this work?
Great question. This is pretty hacky and took some effort to figure out. 

### Detecting your friends
We set up a basic proximity detector. Your computer needs to know who is about to enter your door in order to play their theme music. To do this, your computer cycles through the bluetooth addresses stored in the `friends.csv` file and tries to connect to them one by one. The connection will fail since your friend's phone isn't expecting the connection, and your computer will throw an error message. But thankfully, the error message it throws if the device is out of range is different from the message it throws if the device is in range and rejects the connection. Thus we can tell when your friends are nearby. Since Bluetooth is short-range, this basically means we can detect when your friends are about to enter your door.

### Detecting an open door
With the reed switch in place, there will be a closed circuit if and only if your door is open. It is surprisingly hard to get a computer to check for a closed circuit. This is where the serial USB comes in. We use two threads. One thread constantly sends out a single character through the "TXD" pin, and the other thread constantly checks for that same character arriving on the "RXD" pin. So long as your door is closed, that character won't make it through the circuit, but the moment your door opens it will. Thus we can detect an open door.

### The rest
With proximity detection and a door state checker, the rest is simple. Just cue up the corresponding song, and track the time between plays. 

## Future work
I don't have a lot of experience with Arduinos, but I think this could be done on a Raspberry Pi or something similar. That would be a lot better than needing a spare laptop. 
