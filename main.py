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
                    case ["id", file]:
                        for run in fn.load_file(file).attempts:
                            print(run.id)

                    case ["times", file]:
                        for run in fn.load_file(file).attempts:
                            print(run.rta, run.id)

                    case ["comparison", file]:
                        for run in fn.load_file(file).comparisons:
                            print(run.id)

                    case ["best", file]:
                        for segment in fn.load_file(file).golds.segments:
                            print(segment.name, segment.rta)
                            
                    case _:
                        print("Unmatched")

            case ["compare", file1, id1, file2, id2]:
                for run in fn.load_file(file1).attempts:
                    if id1 == run.id:
                        x = run
                
                for run in fn.load_file(file2).attempts:
                    if id2 == run.id:
                        y = run

                fn.runCompare(x, y)
            case _:
                print("No Match")
        
        cmdloop()
    
    cmdloop()


if __name__ == "__main__":
    main()