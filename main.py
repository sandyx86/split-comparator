import sys, os
import func as fn
import xml.etree.ElementTree as et

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

            case["best", file, method]:
                root = et.parse(file).getroot()
                for a in fn.listBest(root, method):
                    print(a[0], ' id:', a[1])

            #compare two runs
            #this one should definitely be able to compare from
            #two different files
            case["compare", file, id_1, id_2, method]:
                root = et.parse(file).getroot()
                fn.fastCompare(root, id_1, id_2, method)
            
            #may be modified later to take from two files
            case ["hybrid", file, id_1, id_2, method]:
                root = et.parse(file).getroot()

                fn.fastHybrid(root, id_1, id_2, method)

            #show how many times each segment has been reset on
            case ["resets", file]:
                root = et.parse(file).getroot()

                print(fn.fastResetCounter(root))

            case _:
                print("Unrecognized Command")
        
        cmdloop()
    
    cmdloop()


if __name__ == "__main__":
    main()