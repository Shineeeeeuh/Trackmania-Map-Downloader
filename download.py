import requests
import json
import wget
import os.path
import os

def loadConfig():
	cf = open("config.json", "r")
	cjson = json.loads(cf.read())
	author = cjson["TrackInformation"]["Author"]
	name = cjson["TrackInformation"]["Name"]
	directorypath = cjson["DirectoryPath"]
	if directorypath == "":
		print("Error: You don't set the directory path on the file named config.json !")
		os._exit(0)
	verifyDirectory(directorypath, name, author)
	
def verifyDirectory(directorypath, name, author):
	if os.path.exists(directorypath):
		startDownload(directorypath, name, author)
	else:
		print("Error: The directory path is not exist !")
		
def startDownload(directorypath, name, author):
	print("Search for all maps with your settings on config.json");
	link = "https://tm.mania-exchange.com/tracksearch2/search?api=on&limit=100"
	if name == "":
		if author == "":
			print("Error: You don't set any Name or Author for map search !")
			os._exit(0)
		else:
			link = link+"&author="+author
	else:
		link = link+"&name="+name
		if author != "":
			link = link+"&author="+author
	jsonres = json.loads(requests.get(link).text);
	print("Find: "+str(len(jsonres["results"]))+" maps on ManiaExchange !");
	print("Let's download !");
	for i in range(len(jsonres["results"])):
		trackid = jsonres["results"][i]["TrackID"];
		wget.download("https://tm.mania-exchange.com/tracks/download/"+str(trackid), directorypath+str(jsonres["results"][i]["Name"])+".Map.Gbx");
		print("Downloading "+str((i+1))+"/"+str(len(jsonres["results"])))
		
		
def start():
	if os.path.isfile('config.json'):
		print("Load config...")
		loadConfig()
	else:
		print("Oh, I see, the configuration file isn't created !")
		print("I will created this");
		configcontains = {"TrackInformation" : {"Author" : "","Name" : ""},"DirectoryPath" : ""}
		f = open("config.json","w+")
		f.write(json.dumps(configcontains));
		os._exit(0)
		
start()
