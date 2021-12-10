#functions that can be called from cli.py
#these functions act upon the data collected from class.py
import classes as cl
error = "error"

def Load(file):
    return cl.comParse(file)

def Info(main):
    print("Game:          ", main.GameName)
    print("Category:      ", main.CategoryName)
    print(f"Attempts:       {main.FinishedCount}/{main.AttemptCount}")
    for run in main.Runs:
        print(f"-- ID: {run.Id} --")
        print(f"-- Time: {zeroStrip(run.igt)} --")
        print("")
        print("Completed Segments:", len(run.Segments))
        for seg in run.Segments:
            try:
                print(f"{seg.Name:<{main.Runs[0].Maxlen}} | {zeroStrip(seg.igt):10}")
            except:
                print(f"{error}")
        print("")

def InfoID(main, id):
    print("Game:          ", main.GameName)
    print("Category:      ", main.CategoryName)
    print(f"Attempts:       {main.FinishedCount}/{main.AttemptCount}")
    for run in main.Runs:
        if run.Id == id:
            print(f"-- ID: {run.Id} --")
            print(f"-- Time: {zeroStrip(run.igt)} --")
            print("")
            for seg in run.Segments:
                try:
                    print(f"{seg.Name:<{main.Runs[0].Maxlen}} | {zeroStrip(seg.igt):10}")
                except:
                    print(f"{error}")
            print("")

#Lists runs in order from best to worst
def Best(main):
    print("Game:          ", main.GameName)
    print("Category:      ", main.CategoryName)
    print(f"Attempts:       {main.FinishedCount}/{main.AttemptCount}")
    sort_list = []
    for run in main.Runs:
        if not run.igt == "Unfinished":
            sort_list.append([toSeconds(run.igt), run.Id, run.igt.strip("0:")])

    for i, run in enumerate(sorted(sort_list), start = 1):
        print(f"#{i}: {run[2]:<8} | id: {run[1]}")

#Prints the time difference of each segment of two specified runs
def Compare(file_1, id_1, file_2, id_2):
    diff = 0
    n_diff = 0
    p_diff = 0
    for run_1 in file_1.Runs:
        if run_1.Id == id_1:
            for run_2 in file_2.Runs:
                if run_2.Id == id_2:
                    for segment in zip(run_1.Segments, run_2.Segments):
                        try:
                            diff += toSeconds(segment[0].igt) - toSeconds(segment[1].igt)
                        except:
                            print(f"{error}: {'Missing Segment!'}")
                        try:
                            #If its greater than 0, make the text red, else make it green
                            if (round(toSeconds(segment[0].igt) - toSeconds(segment[1].igt))) > 0:
                                p_diff += toSeconds(segment[0].igt) - toSeconds(segment[1].igt)
                                print(f"{segment[0].Name:<{run_1.Maxlen}}|{zeroStrip(segment[0].igt):<12} \033[1;31m{round(toSeconds(segment[0].igt) - toSeconds(segment[1].igt), 2):>7}\033[0;37m {zeroStrip(segment[1].igt):>12}")
                            else:
                                n_diff += toSeconds(segment[0].igt) - toSeconds(segment[1].igt)
                                print(f"{segment[0].Name:<{run_1.Maxlen}}|{zeroStrip(segment[0].igt):<12} \033[1;32m{round(toSeconds(segment[0].igt) - toSeconds(segment[1].igt), 2):>7}\033[0;37m {zeroStrip(segment[1].igt):>12}")
                        except:
                            print(f"{error}: {'Missing Segment!'}")
                    print("--" * run_1.Maxlen)
                    if diff > 0:
                        print(f"{'':{run_1.Maxlen}}|{zeroStrip(run_1.igt):<12} \033[1;31m{round(diff, 2):>7}\033[0;37m {zeroStrip(run_2.igt):>12}")
                    else:
                        print(f"{'':{run_1.Maxlen}}|{zeroStrip(run_1.igt):<12} \033[1;32m{round(diff, 2):>7}\033[0;37m {zeroStrip(run_2.igt):>12}")
                    print(f"{'':{run_1.Maxlen}}|{'':<12} \033[1;31m{round(p_diff, 2):>7}\033[0;37m")
                    print(f"{'':{run_1.Maxlen}}|{'':<12} \033[1;32m{round(n_diff, 2):>7}\033[0;37m")

#helper functions

def toSeconds(string):
    x = string.split(':')
    return int(x[0])*3600 + int(x[1])*60 + float(x[2])

def toMinutes(num):
    theMinutes = int(num / 60)
    theSeconds = num % 60
    return f"{theMinutes:02}:{round(theSeconds, 2):05}"
        

# using .strip() doesn't work in an f-string for some reason, so this is my solution
def zeroStrip(string):
    return string.strip("0:")
