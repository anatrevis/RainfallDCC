import datetime
from collections import defaultdict

# Open file        
fileHandler = open ("dcc.out", "r")
lastsenddict = {}
transmissiontime = []

while True:
	# Get next line from file
	line = fileHandler.readline()
	# If line is empty then end of file reached
	if not line :
		break;
	strline = line.strip()

	if ('\"\"timestamp_status\"\":\"\"' in strline or '\"\"timestamp\"\":\"\"' in strline) and '\"\"deveui\"\":\"\"' in strline:
		strtimestamp = ''
		if '\"\"timestamp_status\"\":\"\"' in strline:
			strtimestamp = strline.split('\"\"timestamp_status\"\":\"\"')[1].split('Z\"\"')[0]
		else:
			strtimestamp = strline.split('\"\"timestamp\"\":\"\"')[1].split('Z\"\"')[0]

		transmissiontime.append(datetime.datetime.strptime(strtimestamp, '%Y-%m-%dT%H:%M:%S.%f')) #list of all transmissions times

		strdeviceui = strline.split('\"\"deveui\"\":\"\"')[1].split('\"\"')[0]
		#print("Deviceui_status: %s - Timestamp_status: %s" %(strdeviceui_status,strtimestamp_status))

		if strdeviceui in lastsenddict:								
			date_time_1 = datetime.datetime.strptime(strtimestamp, '%Y-%m-%dT%H:%M:%S.%f')
			date_time_2 = datetime.datetime.strptime(lastsenddict[strdeviceui], '%Y-%m-%dT%H:%M:%S.%f')
			diff = date_time_1 - date_time_2
			days, seconds = diff.days, diff.seconds
			hours = days * 24 + seconds // 3600
			minutes = (seconds % 3600) // 60
			seconds = seconds % 60

			#TO CONFIGURE
			if days > 2: #in this case, shows gaps bigger than 2 days for each device
				print("GAP in deviceui %s between %s and %s" %(strdeviceui,strtimestamp,lastsenddict[strdeviceui]))

		else:
			print("------ NEW DEVICE -----")

		lastsenddict[strdeviceui] = strtimestamp

# Close file   
fileHandler.close()  

print("------ LOOKING FOR COMON GAPS -----") #if no other device transmitted any data during a device gap, this is a PN Outage
transmissiontime.sort() #put all transmissions in order
# print(transmissiontime)
for i in range(0, len(transmissiontime)-1):
	diftime = transmissiontime[i] - transmissiontime[i+1] #compares
	days, seconds = diftime.days, diftime.seconds
	hours = days * 24 + seconds // 3600
	minutes = (seconds % 3600) // 60
	seconds = seconds % 60
	if hours>1: #if the difference is bigger than 1 hour between 2 transmissions it means that no device transmitted anything during 1 hour, so its a PN outage
		print("There is a PN outage between %s and %s" %(transmissiontime[i],transmissiontime[i+1]))


	

