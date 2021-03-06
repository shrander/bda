from scapy.all import *
import sys
import os.path
import httplib, urllib2
import json

url = "http://codexcom01.cloudapp.net:3000/insertall"
header = {'Content-type': 'application/json', 'Accept': 'text/plain'}

if (os.path.isfile(sys.argv[1])):
   print "Parsing..." 
else:
    print "File not found, exiting..."
    sys.exit()

#pcap = rdpcap("capfiles/airportSniffHwGVg3.cap")
pcap = rdpcap(sys.argv[1])
f = open('json', 'w')

f.write("{\n\"items\":[\n")

for i in pcap:
    try:
        proto = i.getlayer(6).name
        if "802.11 Information Element" in proto:
            continue
    except:
        continue

    f.write("{\n")
    try:
        f.write("\"smac\":\""+i[Dot11].addr1+"\",")
        f.write("\n\"dmac\":\""+i[Dot11].addr2+"\",")
    except:
        pass
    try:
        f.write("\n\"sip\":\""+i[IP].src+"\",")
        f.write("\n\"dip\":\""+i[IP].dst+"\",")
    except:
        pass
    try:
        f.write("\n\"sport\":\""+str(i.sport)+"\",")
        f.write("\n\"dport\":\""+str(i.dport)+"\",")
    except AttributeError:
        pass
    f.write("\n\"protocol\":\""+str(proto)+"\",")
    try:
        mpa = dict.fromkeys(range(32))
        f.write("\n\"qclass\":"+json.dumps(i[UDP][DNSQR].qname)+",")
    except:
        pass
#    try:
#        f.write("\nuser:TBD")
#    except:
#        pass
    try:
        f.write("\nbytes:\""+i[IP].len+"\",")
    except:
        pass
    try:
        f.write("\n\"time\":\""+str(int(i.time))+"\"")
    except:
        pass
    f.write("\n},\n")

f.write("{\"\":\"\"}")
f.write("]\n}")



f.close()

if os.stat('json').st_size < 1:
    print "Empty JSON file, skipping upload..."
    sys.exit()
print "Uploading to "+url

data = open('json').read()
req = urllib2.Request(url)
req.add_header('Content-Type', 'application/json')
try:
    response = urllib2.urlopen(req, data)
except URLError:
    print "*** Error, re-trying..."
    response = urllib2.urlopen(req, data)
except HTTPError:
    print "*** File too large, skipping..."
print response.geturl()
print response.read()
