import SoftLayer
import sys
import pprint
from prettytable import PrettyTable
pp = pprint.PrettyPrinter(indent=4)

argv=sys.argv
if ( len(argv) != 2 ):
    print 'Usage: python %s <Your IP>' % argv[0]
    exit(10)

targetip = argv[1]
LIMITSIZE=500


client = SoftLayer.Client()
myip = client['Network_Subnet_IpAddress'].getByIpAddress(targetip)
if (myip is None) or (myip == "") :
    print "You don't have  %s in your account." % (targetip)
    exit(20)

_offset=0
alllists=[]
while True:
    lists = client['Network_Subnet_IpAddress'].getSyslogEventsSevenDays(id=myip['id'], limit=LIMITSIZE, offset=_offset)
    alllists = alllists + lists
    _offset = _offset + LIMITSIZE
    if len(lists) < LIMITSIZE :
        break

if (alllists ==[]):
    print "No records for this IP"
    exit(0)

alllists = sorted(alllists, key= lambda x: x['createDate'], reverse=False)
table = PrettyTable(['createDate',
                     'sourceIpAddress',
                     'sourcePort',
                     'destinationIpAddress',
                     'destinationPort',
                     'protocol',
                     'eventType'])

for list in alllists:
    table.add_row([
                     list['createDate'],
                     list['sourceIpAddress'],
                     list['sourcePort'],
                     list['destinationIpAddress'],
                     list['destinationPort'],
                     list['protocol'],
                     list['eventType']
    ])
    
print table
