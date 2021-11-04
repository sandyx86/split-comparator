# Python Split Comparator #

# Compare any run of any two split files
# Compare any two runs of any split file
# function to list all final times - done -
# function to list all split times within a run
# function to do both of those things
# add a mode option for realtime/gametime

# comparator.py file1.lss -c file2.lss

import sys, getopt
import xml.etree.ElementTree as et
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "l:c:", [])
    except getopt.GetoptError:
        print("usage: comparator.py file_1 [run id] -c file_2 [run id]") #allows for the same input file twice even though that seems weird
        sys.exit(2)

    #single file
    for opt, arg in opts:
        if opt == "-l":
            try:
                tree = et.parse(arg)
                root = tree.getroot()
                f_info = getFileInfo(root)
                print("Game:          ", f_info.GameName)
                print("Category:      ", f_info.CategoryName)
                print("Attempts:      ", f_info.AttemptCount)
                for run in f_info.Runs:
                    print(" ", run.Id, run.Time)
            except:
                print("file not found")
        elif opt == "-c":
            try:
                tree = et.parse(arg)
                root = tree.getroot()
                f_info = getFileInfo(root)
                print("Game:          ", f_info.GameName)
                print("Category:      ", f_info.CategoryName)
                print("Attempts:      ", f_info.AttemptCount)
                for run in f_info.Runs:
                    print(run.Id, run.Time)
            except:
                print("file not found")

        
#class for the name and category of a split file
#should also have: RunCount, FinishedRunCount, Platform, AttemptCount
#make nested classes
class getFileInfo():
    def __init__(self, root):
        self.GameName       = root.find("GameName").text
        self.CategoryName   = root.find("CategoryName").text
        self.AttemptCount   = root.find("AttemptCount").text
        self.Runs = [] #this should be a run object, a time paired with an id
        
        class getSegments(): #should probably pass the run id
                def __init__(self, runId):
                    self.SegNames = []

                    for a in root.iter("Time"):
                        if a.attrib['id'] == runId:
                            print(a.attrib['id'])
                            for name in root.iter("Name"):
                                print(name.text)
                                print(a.find("GameTime").text)



        class getRunInfo():
            def __init__(self, element):
                self.Segments = []
                for b in element.iter("GameTime"):
                    self.Id = element.attrib['id']
                    self.Time = b.text
                    self.Segments.append(getSegments(self.Id))


                        


        #gets every id for every finished run in <AttemptHistory>
        for a in root.iter("AttemptHistory"):
            for b in a.iter("Attempt"):
                for c in b.iter("GameTime"):
                    self.Runs.append(getRunInfo(b))

            


    

        


if __name__ == "__main__":
    main()