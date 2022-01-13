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
                for a in fn.listBest(file, method):
                    print(a[0], ' id:', a[1])

            #compare two runs
            case["compare", file, id_1, id_2, method]:
                tree = et.parse(file)
                root = tree.getroot()
                fn.fastCompare(root, id_1, id_2, method)
            
            #may be modified later to take from two files
            case ["hybrid", file, id_1, id_2, method]:
                tree = et.parse(file)
                root = tree.getroot()

                fn.fastHybrid(root, id_1, id_2, method)
            #show how many times a segment has been reset on (miscounting bug?)
            case ["resets", file]:
                slist = fn.findSegments(file)
                for segment in fn.fastReset(file):
                    print(
                        segment[1].ljust(len(max(slist, key=len)), ' '),
                        "-",
                        segment[0]
                    )

            case ["test", file]:
                tree = et.parse(file)
                root = tree.getroot()

                fn.fastCompare(root, '110', '140', 'igt')

            case _:
                print("Unrecognized Command")
        
        cmdloop()
    
    cmdloop()


if __name__ == "__main__":
    main()