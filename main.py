import sys, os
import func as fn

red         = "\033[31m"
green       = "\033[32m"
clear       = "\033[0m"
blink_on    = "\033[5m"
blink_off   = "\033[25m"
error       = red + "ERROR" + clear

def main():
    #This list stores the file objects
    file_list = []

    #The Command-Line Loop
    def cmdloop():
        command = input(f"{green}comparator{clear}>")
        match command.split():
            case ["quit"]:
                sys.exit()

            case ["list", option, file]:
                match [option, file]:
                    case ["times", file]:
                        for run in fn.load_file(file).attempts:
                            print(run.igt, run.id)

                    case ["comparison", file]:
                        for run in fn.load_file(file).comparisons:
                            print(run.id)

                    case ["best", file]:
                        for run in fn.rankedRuns(fn.load_file(file).attempts):
                            print(
                                fn.zeroStrip(run[1]).ljust(10, ' '),
                                "id:",
                                run[2]
                            )
                    case _:
                        print("Unrecognized Command")

            case ["compare", file1, id1, file2, id2]:
                for run in fn.load_file(file1).attempts:
                    if id1 == run.id:
                        x = run
                
                for run in fn.load_file(file2).attempts:
                    if id2 == run.id:
                        y = run

                fn.runCompare(x, y)
            
            #may be modified later to take from two files
            case ["hybrid", file, id1, id2]:
                for run in fn.load_file(file).attempts:
                    if id1 == run.id:
                        x = run
                    
                    if id2 == run.id:
                        y = run
                    
                for segment in fn.createHybrid(x, y):
                    print(segment)

            case _:
                print("Unrecognized Command")
        
        cmdloop()
    
    cmdloop()


if __name__ == "__main__":
    main()