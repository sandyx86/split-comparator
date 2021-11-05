import sys
import xml.etree.ElementTree as et
def main():

    class getSegments():
        def __init__(self, root):
            self.Name = ""
            self.SegTime = ""


    class getRuns():
        def __init__(self, element, root):
            self.Segments = [] #A segment object
            for text in element.iter("RealTime"):
                self.Id = element.attrib['id']
                self.Time = text.text

    class getFileInfo():
        def __init__(self, root):
            attempts = 0
            finished = 0
            self.GameName       =   root.find("GameName").text
            self.CategoryName   =   root.find("CategoryName").text
            self.AttemptCount   =   root.find("AttemptCount").text
            self.Runs           =   [] #A run object
            try:

                for attempt in root.iter("Attempt"):
                    #print("i")
                    for time in attempt.iter("RealTime"):
                        print("u")
                        try:
                            self.Runs.append(getRuns(attempt))
                        except:
                            print("didnt fucking do shit")
                            continue
            except:
                print("fuckyou")

            for run in self.Runs:
                print(run.Id, run.Time, run.Segments)
                run.Segments.append(getSegments())

    def comList(file):
        tree = et.parse(file)
        root = tree.getroot()
        file_1 = getFileInfo(root)
        print("Game:          ", file_1.GameName)
        print("Category:      ", file_1.CategoryName)
        print("Attempts:      ", file_1.AttemptCount)
        for run in file_1.Runs:
            print(run.Time)

    command = input("comparator>")
    match command.split():
        case ["quit"]:
            sys.exit(0)
        case ["exit"]:
            sys.exit(0)
        case ["list", file]:
            try:
                comList(file)
            except:
                print(f"File \"{file}\" not found.")


    main()


if __name__ == "__main__":
    main()
