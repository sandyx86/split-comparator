import sys
import func as fn
import xml.etree.ElementTree as et
from os import path

red         = "\033[31m"
green       = "\033[32m"
clear       = "\033[0m"
blink_on    = "\033[5m"
blink_off   = "\033[25m"
error       = red + "ERROR" + clear


def main():
    #The Command-Line Loop
    def cmdloop():
        command = input(f"{green}comparator{clear}>")

        filepaths = [arg for arg in pathSplitter(command) if path.isfile(arg)]
        
        method = "igt" if "igt" in command else "rta"
        idl = [x for x in command.split() if x.isdigit()]

        if "quit" in command:
            sys.exit()
        
        elif "best" in command:
            root = et.parse(filepaths[0]).getroot() if len(filepaths) else None
            if not root == None:
                
                for a in fn.listBest(root, method):
                    print(a[0], ' id:', a[1])
            else:
                print("No valid file")

        elif "compare" in command:
            root_1 = et.parse(filepaths[0]).getroot() if len(filepaths) else None
            root_2 = et.parse(filepaths[1]).getroot() if len(filepaths) > 1 else None

            if not len(idl):
                cmdloop()

            if root_1 == None:
                cmdloop()

            if root_2 == None:
                fn.fastCompare(root_1, idl[0], idl[-1], method)
                cmdloop()
                
            fn.fastCompareTwo(root_1, idl[0], root_2, idl[-1], method)

        elif "hybrid" in command:
            root_1 = et.parse(filepaths[0]).getroot() if len(filepaths) else None
            root_2 = et.parse(filepaths[1]).getroot() if len(filepaths) > 1 else None

            if not len(idl):
                cmdloop()

            if root_1 == None:
                cmdloop()

            fn.fastHybrid(root_1, idl[0], idl[-1], method)

        elif "resets" in command:
            root = et.parse(filepaths[0]).getroot() if len(filepaths) else None
            
            if not root == None:
                fn.fastResetCounter(root)

        elif "variance" in command:
            root = et.parse(filepaths[0]).getroot() if len(filepaths) else None
            
            if not len(idl):
                cmdloop()

            if root == None:
                cmdloop()
            
            fn.fastVariance(root, idl[0], idl[-1], method)

        elif "help" in command:
            with open("help.txt", 'r') as help_file:
                for line in help_file:
                    print(line, end='')
        
        cmdloop()
    
    cmdloop()


def pathSplitter(string):
    if "\"" in string:
        #paths = [odd for index, odd in enumerate(string.split("\"")) if index % 2]
        return pathSplitter(string.split("\"")[0].strip()) + [string.split("\"")[1]] + pathSplitter(''.join(string.split("\"")[2:5]).strip())
    else: 
        return string.split()
    

if __name__ == "__main__":
    main()
