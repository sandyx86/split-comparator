# Python Split Comparator #

# Compare any run of any two split files
# Compare any two runs of any split file
# function to list all final times
# function to list all split times within a run
# function to do both of those things
# add a mode option for realtime/gametime

# comparator.py file1.lss -c file2.lss

import sys, getopt
import xml.etree.ElementTree as et
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "l:", [])
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
                print(f_info.Runs)
                for run in f_info.Runs:
                    print(run)
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
        self.Runs = []
        
        class getRunInfo():
            def __init__(self, root):
                self.FinalTime = root.find("GameTime").text
                self.Id = root.find("Attempt").attrib("id")

                #self.Id = root.attrib.get("id") #get the id of the run
        
        #gets every id for every run in <AttemptHistory>
        for a in root.iter("AttemptHistory"):
            for b in root.iter("Attempt"):
                print(b.attrib['id'])
    
            


    

        


if __name__ == "__main__":
    main()