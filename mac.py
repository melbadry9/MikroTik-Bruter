import subprocess
import sqlite3 

data = sqlite3.connect('rotana.sqlite')
command = subprocess.Popen("nmap -sn 10.0.0.0/24 -T5 -n",shell=True,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
result  = command.communicate()
macs = {}
result = result[0].decode("utf-8").split("\n")
for ping in result:
	if "MAC" in ping:
		#mac
		start = ping.find("")
		end = ping.find("(", start+3)
		stri = ping[start:end - 1]
		mac = stri.replace("MAC Address: ","")		
		#name
		start = ping.find("(")
		end = ping.find(")",start)
		name = ping[start:end].replace("(","")
		macs[mac] = name
for i in macs.keys() :
	m = data.cursor()
	m.execute("select mac from rotana where mac = ? ",(i,))
	if len(m.fetchall()) == 0:
		print(i)
		m.execute("insert into rotana (mac,name) values (?,?)",(i,macs[i]))
	else:
		pass
data.commit()
data.close()	