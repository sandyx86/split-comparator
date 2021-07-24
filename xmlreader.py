from tkinter.constants import TRUE
import xml.etree.ElementTree as et


__Mode__ = 'RealTime'
_id = []
_time = []
_split = []
_name = []
g = globals()

#single file version for now


#lssParse is gonna need some work to account for the id numbers not matching
def lssParse(xmlfile): #makes a list for the id, final time, split, and split name
    tree = et.parse(xmlfile)
    root = tree.getroot()
    i = 0

    for Attempt in root.iter('Attempt'):
        
        for Time in Attempt.iter(__Mode__):
            _id.append(Attempt.attrib['id'])
            _time.append(Time.text)
            g['run_{0}'.format(_id[i])] = [] #this magic g makes a list for every completed run there is
            i += 1                           #example name run_5 where 5 is the id number

def lssGetName(xmlfile):
    tree = et.parse(xmlfile)
    root = tree.getroot()
    

    for Segment in root.iter('Segment'):
        
        for Name in Segment.iter('Name'):
            _name.append(Name.text)
            
            

def lssGetSplits(xmlfile):
    tree = et.parse(xmlfile)
    root = tree.getroot()
    

    for SegmentHistory in root.iter('SegmentHistory'):
                
        for SegmentTime in SegmentHistory.iter('Time'):
            i = 0
            
            for t in SegmentTime.iter(__Mode__):
               
                for id in SegmentTime.attrib['id']:  #this id check makes sure it only appends split times that were part of a finished run
                    if id in _id:
                        g['run_{0}'.format(id)].append(t.text)
                i += 1

i = 0
def bitch():
    for i in range(len(_id)):
        print(_id[i] + ':' ,g['run_{0}'.format(_id[i])])
                            
    
def splSeconds(string):
    x = string.split(':')
    h = int(x[0])
    m = int(x[1])
    s = float(x[2])
    x = h*3600 + m*60 + s
    return x

i = 0 #when i changes, the splits splCompare compares changes

def splCompare(r1, r2): 
    list = []
    for i in range(len(_name)):
        c1 = splSeconds(g['run_{0}'.format(r1)][i])
        c2 = splSeconds(g['run_{0}'.format(r2)][i])
        list.append(round(c2 - c1,2))
    return list
        
lssParse('Luigis Mansion - Any%.lss') #make this a file select thing later
lssGetName('Luigis Mansion - Any%.lss')
lssGetSplits('Luigis Mansion - Any%.lss')
bitch()


print(splCompare(5, 5))
