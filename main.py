import sys
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

            #oddly specific command, unfinished for now
            #compare an attempt against another file's PB
            case["compare", file_1, id_1, file_2, "pb", method]:
                root_1 = et.parse(file_1).getroot()
                root_2 = et.parse(file_2).getroot()

                fn.fastComparePB(root_1, id_1, root_2, method)    
            
            case["compare", file_1, id_1, file_2, id_2, method]:
                root_1 = et.parse(file_1).getroot()
                root_2 = et.parse(file_2).getroot()

                fn.fastCompareTwo(root_1, id_1, root_2, id_2, method)
            
            #may be modified later to take from two files
            case ["hybrid", file, id_1, id_2, method]:
                root = et.parse(file).getroot()

                fn.fastHybrid(root, id_1, id_2, method)

            #show how many times each segment has been reset on
            case ["resets", file]:
                root = et.parse(file).getroot()

                print(fn.fastResetCounter(root))
            
            case ["variance", file, x, y, method]:
                root = et.parse(file).getroot()
                fn.fastVariance(root, int(x), int(y), method)
            
            case["help"]:
                print(
                    " quit - exits the program\n",
                    "   quit\n\n",
                    "best - prints a list of all recorded times from fastest to slowest\n",
                    "   best <file> [rta, igt]\n\n",
                    "compare - prints a comparison of two runs\n",
                    "   compare <file> <id1> <id2> [rta, igt]\n\n",
                    "   compare <file1> <id1> <file2> <id2> [rta, igt]"
                    "hybrid - prints a list of split times\n"
                    "   created from the better of two segments in each run\n",
                    "   hybrid <file> <id1> <id2> [rta, igt]\n\n",
                    "resets - print how many times each segment has been reset on\n",
                    "   resets <file>\n",
                    "variance - prints the maximum difference for each segment in a range of runs\n",
                    "   variance <file> <x> <y> [rta, igt]"
                )
            
            case _:
                print("Unrecognized Command")
        
        cmdloop()
    
    cmdloop()


if __name__ == "__main__":
    main()