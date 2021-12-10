import xml.etree.ElementTree as et

class getSeg():
    def __init__(self, root, name, id):
        for segment in root.iter("Segments"):
            for seg_element in segment.iter("Segment"):
                for time in seg_element.iter("SegmentHistory"):
                    for t_id in time.iter("Time"):
                        if (t_id.attrib['id'] == id) & (seg_element.find("Name").text == name):
                            try:
                                self.rta = t_id.find("RealTime").text
                                try:
                                    self.igt = t_id.find("GameTime").text
                                except:
                                    self.igt = "No GameTime"
                                self.Name = seg_element.find("Name").text
                            except:
                                continue
class getRuns():
    def __init__(self, attempt, root):
        self.Segments = [] #A segment object
        self.Maxlen = 0 #Maximum Length!
        self.Id = attempt.attrib['id']

        #If <Attempt> does not have <RealTime>/<GameTime>:
        if not len(attempt):
            self.rta = 'Unfinished'
            self.igt = 'Unfinished'
            #print(self.timeRTA)

        #For every <Attempt> that does have <RealTime>/<GameTime>:
        for time in attempt:
            if time.tag == 'RealTime':
                self.rta = time.text

            elif time.tag == 'GameTime':
                self.igt = time.text


        #Only want to append a segment object if <SegmentHistory> contains a <Time> with its id
        for segment in root.iter("Segments"):
            for seg_element in segment.iter("Segment"):
                for time in seg_element.iter("SegmentHistory"):
                    for t_id in time.iter("Time"):
                        if (t_id.attrib['id'] == self.Id):
                            self.Segments.append( getSeg(root, seg_element.find("Name").text, self.Id))

                        #Increases Maxlen when it finds a longer string
                    if len(seg_element.find("Name").text) > self.Maxlen:
                        self.Maxlen = len(seg_element.find("Name").text)

class getFileInfo():
    def __init__(self, root):
        self.GameName       =   root.find("GameName").text
        self.CategoryName   =   root.find("CategoryName").text
        self.AttemptCount   =   root.find("AttemptCount").text
        self.FinishedCount = 0
        self.Runs           =   [] #A run object
        #self.Segments       =

        for attempt in root.iter("Attempt"):
            self.Runs.append( getRuns(attempt, root) )
            for time in attempt:
                #if statement to test for RealTime because there will always be a RealTime
                if time.tag == 'RealTime':
                    self.FinishedCount += 1

class comParse():
    def __init__(self, file):
        self.tree = et.parse(file)
        self.root = self.tree.getroot()
        self.main = getFileInfo(self.root)
        self.filename = file
