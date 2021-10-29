# Python Split Comparator #

# Compare any run of any two split files
# Compare any two runs of any split file
# function to list all final times
# function to list all split times within a run
# function to do both of those things

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
                f_info = getRunInfo(root)
                print("Game:          ", f_info.GameName)
                print("Category:      ", f_info.CategoryName)
                print("Attempts:      ", f_info.AttemptCount)
            except:
                print("file not found")
        
#class for the name and category of a split file
#should also have: RunCount, FinishedRunCount, Platform, AttemptCount
class getRunInfo():
    def __init__(self, root):
        self.GameName       = root.find("GameName").text
        self.CategoryName   = root.find("CategoryName").text
        self.AttemptCount   = root.find("AttemptCount").text

#def getRunInfo(root):
#    print("Game:        ", root.find("GameName").text)
#    print("Category:    ", root.find("CategoryName").text)
    

        


if __name__ == "__main__":
    main()