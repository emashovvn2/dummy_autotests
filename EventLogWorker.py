import win32evtlog
import argparse
import sys
import json
with open("Event_dictionary.json") as read_file:
    data = json.load(read_file)
    
def createParser ():
    
    parser = argparse.ArgumentParser()
    parser.add_argument ('--func', '-u', required=True)
    #parser.add_argument ('--id', '-i', default=1000)
    parser.add_argument ('--log', '-l', default="InfinityAudit")
    #parser.add_argument ('--server', '-s', default='localhost')
    parser.add_argument ('--find_string', '-f', default='')
    return parser

def clear_log(logtype = "Application", server = 'localhost'):
    hand = win32evtlog.OpenEventLog(server,logtype)
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ
    total = win32evtlog.GetNumberOfEventLogRecords(hand)
    win32evtlog.ClearEventLog(hand, None)

def find_event_by_ID(ID, logtype = "Application", server = 'localhost', findStr = '', prn=True):
    hand = win32evtlog.OpenEventLog(server,logtype)
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ
    total = win32evtlog.GetNumberOfEventLogRecords(hand)
    events = win32evtlog.ReadEventLog(hand, flags,0, 100000)
    if events:
        for event in events:
            if int(event.EventID) == int(ID):
                data = event.StringInserts
                if data:
                    for msg in data:
                        if findStr in msg :
                            if (prn):
                                print("Find")
                            return True
    if (prn):
        print("Not Found")
    return False

def find_pack_event(FS):
    not_found_events = []
    for evnt in FS:
        ID = data[evnt]['i']
        LT = data[evnt]['l']
        FS = data[evnt]['f']
        SERV = data[evnt]['s']
        if not find_event_by_ID(ID, logtype=LT, server=SERV, findStr=FS, prn=False):
            not_found_events.append(ID)
    if len(not_found_events) == 0:
        print("Find")
        return True
    else:
        print("Not found events  -  " + str(not_found_events))
        return False

parser = createParser()
namespace = parser.parse_args(sys.argv[1:])

if namespace.func == 'clear_log':
    clear_log(logtype=namespace.log)

if namespace.func == 'find_event_by_ID':
    ID = data[namespace.find_string]['i']
    LT = data[namespace.find_string]['l']
    FS = data[namespace.find_string]['f']
    SERV = data[namespace.find_string]['s']
    find_event_by_ID(ID, logtype=LT, server=SERV, findStr=FS)

if namespace.func == 'find_pack_event':
    FS = data[namespace.find_string]['f']
    find_pack_event(FS.split(' '))
