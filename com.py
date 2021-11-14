##Things that need to be done...##

#Real Time and Game Time Modes


#CMD/PowerShell Mode for Windows users (no ANSI)
#Change the index numbers to names, optionally
#Function to clean unfinished runs
#Allow the possibility of loading a file with spaces in its name
#Comment the code better

#Function to list all runs by time and id -- done
#Function to list runs in order from best to worst -- done
#Add total times and total +/- to the compare function -- done
#Find the longest string to dynamically add padding -- done
#Load file function -- done
#List a specific run by its id -- done
#Add functions for comparing runs -- done
#Convert strings of time to integers / floats -- done

#Make the source code look pretty

import sys
import os
import xml.etree.ElementTree as et
f_list = []
error = "\033[1;31mERROR\033[0;37m"
print("type \"help\" for help")
def main():
    #gets a segment object by its id, returns name and time
    class getSeg():
        def __init__(self, root, name, id):
            for segment in root.iter("Segments"):
                for seg_element in segment.iter("Segment"):
                    for time in seg_element.iter("SegmentHistory"):
                        for t_id in time.iter("Time"):
                            if (t_id.attrib['id'] == id) & (seg_element.find("Name").text == name):
                                try:
                                    self.Time = t_id.find("GameTime").text
                                    self.Name = seg_element.find("Name").text
                                    self.sTime = toSeconds(t_id.find("GameTime").text)
                                except:
                                    #print('ERROR')
                                    continue

    class getRuns():
        def __init__(self, attempt, root):
            self.Segments = [] #A segment object
            self.Maxlen = 0 #Maximum Length!
            #self.SegNames = []
            for time in attempt.iter("GameTime"):
                self.Id = attempt.attrib['id']
                self.Time = time.text
                for segment in root.iter("Segments"):
                    for seg_element in segment.iter("Segment"):
                        for name in seg_element.iter("Name"):
                            self.Segments.append(getSeg(root, name.text, self.Id))
                            if len(name.text) > self.Maxlen:
                                self.Maxlen = len(name.text)

    class getFileInfo():
        def __init__(self, root):
            self.GameName       =   root.find("GameName").text
            self.CategoryName   =   root.find("CategoryName").text
            self.AttemptCount   =   root.find("AttemptCount").text
            self.Runs           =   [] #A run object
            #self.Segments       =

            for attempt in root.iter("Attempt"):
                for time in attempt.iter("GameTime"):
                    self.Runs.append(getRuns(attempt, root))
                    #print("Appended: ", getRuns(attempt, root))

    class comParse():
        def __init__(self, file):
            self.tree = et.parse(file)
            self.root = self.tree.getroot()
            self.main = getFileInfo(self.root)
            self.filename = file

    def comInfo(main):
        print("Game:          ", main.GameName)
        print("Category:      ", main.CategoryName)
        print(f"Attempts:       {len(main.Runs)}/{main.AttemptCount}")
        for run in main.Runs:
            print(f"-- ID: {run.Id} --")
            print(f"-- Time: {zeroStrip(run.Time)} --")
            print("")
            for seg in run.Segments:
                try:
                    print(f"{'':5}{seg.Name:<{main.Runs[0].Maxlen}} | {zeroStrip(seg.Time):10}")
                except:
                    print(f"{'':5}{error}")
            print("")

    def comInfoID(main, id):
        print("Game:          ", main.GameName)
        print("Category:      ", main.CategoryName)
        print(f"Attempts:       {len(main.Runs)}/{main.AttemptCount}")
        for run in main.Runs:
            if run.Id == id:
                print(f"-- ID: {run.Id} --")
                print(f"-- Time: {zeroStrip(run.Time)} --")
                print("")
                for seg in run.Segments:
                    try:
                        print(f"{'':5}{seg.Name:<{main.Runs[0].Maxlen}} | {zeroStrip(seg.Time):10}")
                    except:
                        print(f"{'':5}{error}")
                print("")

    #Lists runs in order from best to worst
    def comBest(main):
        i = 0
        print("Game:          ", main.GameName)
        print("Category:      ", main.CategoryName)
        print(f"Attempts:       {len(main.Runs)}/{main.AttemptCount}")
        sort_list = []
        for run in main.Runs:
            sort_list.append([toSeconds(run.Time), run.Id, run.Time.strip("0:")])

        for run in sorted(sort_list):
            print(f"#{i}: {run[2]:<8} | id: {run[1]}")
            i += 1




    #Subtracts the sTime of run_1 and run_2
    def comCompare(file_1, id_1, file_2, id_2):
        diff = 0
        n_diff = 0
        p_diff = 0
        for run_1 in file_1.Runs:
            if run_1.Id == id_1:
                for run_2 in file_2.Runs:
                    if run_2.Id == id_2:
                        for segment in zip(run_1.Segments, run_2.Segments):
                            try:
                                diff += segment[0].sTime - segment[1].sTime
                            except:
                                print(f"{error}: {'Missing Segment!'}")
                            try:
                                if (round(segment[0].sTime - segment[1].sTime)) > 0:
                                    p_diff += segment[0].sTime - segment[1].sTime
                                    print(f"{segment[0].Name:<{run_1.Maxlen}}|{zeroStrip(segment[0].Time):<12} \033[1;31m{round(segment[0].sTime - segment[1].sTime, 2):>7}\033[0;37m {zeroStrip(segment[1].Time):>12}")
                                else:
                                    n_diff += segment[0].sTime - segment[1].sTime
                                    print(f"{segment[0].Name:<{run_1.Maxlen}}|{zeroStrip(segment[0].Time):<12} \033[1;32m{round(segment[0].sTime - segment[1].sTime, 2):>7}\033[0;37m {zeroStrip(segment[1].Time):>12}")
                            except:
                                print(f"{error}: {'Missing Segment!'}")
                        print("--" * run_1.Maxlen)
                        if diff > 0:
                            print(f"{'':{run_1.Maxlen}}|{zeroStrip(run_1.Time):<12} \033[1;31m{round(diff, 2):>7}\033[0;37m {zeroStrip(run_2.Time):>12}")
                        else:
                            print(f"{'':{run_1.Maxlen}}|{zeroStrip(run_1.Time):<12} \033[1;32m{round(diff, 2):>7}\033[0;37m {zeroStrip(run_2.Time):>12}")
                        print(f"{'':{run_1.Maxlen}}|{'':<12} \033[1;31m{round(p_diff, 2):>7}\033[0;37m")
                        print(f"{'':{run_1.Maxlen}}|{'':<12} \033[1;32m{round(n_diff, 2):>7}\033[0;37m")

    #translates human readable time to pure seconds
    #not to be used with a time string that has already been stripped!
    def toSeconds(string):
        x = string.split(':')
        return int(x[0])*3600 + int(x[1])*60 + float(x[2])

    # using .strip() doesn't work in an f-string for some reason, so this is my solution
    def zeroStrip(string):
        return string.strip("0:")

    #Command Line Interface
    command = input("\033[92mcomparator\033[0m>")
    match command.split(" "):
        case ["quit"]:
            sys.exit(0)
        case ["exit"]:
            sys.exit(0)

        #Loads a file
        case ["load", file]:
            try:
                f_list.append(comParse(file))
                print(f"Loaded {file} at index {len(f_list) - 1}")
            except:
                print(f"Failed to load {file}")

        #Unloads a file
        case ["unload", index]:
            try:
                n = f_list[int(index)].filename
                f_list.pop(int(index))
                print(f"Unloaded {n}")
            except:
                print(f"Unable to pop index {index}")

        #Prints a list of all loaded files and their index number
        case ["index"]:
            i = 0
            for f in f_list:
                print(f"{i}: {f.filename}")
                i += 1

        #List the valid run IDs in a file
        case ["ids", index]:
            try:
                print("IDs:")
                print("_________________________")
                for r in f_list[int(index)].main.Runs:
                    print(f"{r.Id}: {r.Time}")
            except:
                print("List index out of range")

        #List command
        case ["list", index, option]:

            match option:
                case "-a": #-a for all
                    try:
                        comInfo(f_list[int(index)].main)
                    except:
                        print(f"File \"{index}\" not yet loaded.")

                case "-b": #-b for best to worst
                    try:
                        comBest(f_list[int(index)].main)
                    except:
                        print(f"File \"{index}\" not yet loaded.")

                case option:#list a specific runs segments
                    try:
                        comInfoID(f_list[int(index)].main, option)
                    except:
                        print(f"File \"{index}\" not yet loaded.")

        #Command to compare one runs segment times to anothers
        case ["compare", file_1, id_1, file_2, id_2]:
            comCompare(f_list[int(file_1)].main, id_1, f_list[int(file_2)].main, id_2)

        #lists all files in a folder
        case ["dir"]:
            for file in os.listdir():
                print(file)
            print('')

        #lists all files in a folder
        case ["ls"]:
            for file in os.listdir():
                print(file)
            print('')

        case["help"]:
            print("Commands:")
            print("     quit / exit")
            print("         -exits the program.")
            print('')
            print("     dir / ls")
            print("         -lists all files in the current directory")
            print('')
            print("     load [filename]")
            print("         -loads a file and parses it.")
            print('')
            print("     unload [index]")
            print("         -unloads a file and removes it from the index.")
            print("     index")
            print("         -prints the index number of all loaded files")
            print('')
            print("     ids [index]")
            print("         -prints all valid run IDs in a file")
            print('')
            print("     list [index] *[option/id]")
            print("         -lists all the segments in a run by the ID specified.")
            print("         -a: list all runs with all segments")
            print("         -b: list the runs in order from best to worst")



        #test case for me to test things
        case["test", test]:
            print(0 != 1)





    main()


if __name__ == "__main__":
    main()
