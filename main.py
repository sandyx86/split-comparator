#Command Line Interface of split-comparator
#This file should never directly access data
#Only what is returned from func.py
import sys
import os
import func as fn

f_list = []

red = "\033[31m"
green = "\033[32m"
ansi_end = "\033[0m"

def main():
    command = input(f"{green}comparator{ansi_end}>")
    match command.split(" "):
        case ["quit"]:
            sys.exit(0)
        case ["exit"]:
            sys.exit(0)

        #Loads a file
        case ["load", file]:
            print(f"\033[5mLoading {file}\033[25m")
            f_list.append(fn.Load(file))
            print(f"Loaded {file} at index {len(f_list) - 1}")



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
            for i, f in enumerate(f_list):
                print(f"{i}: {f.filename}")

        #List the valid run IDs in a file
        case ["ids", index]:
            print("IDs:")
            print("_________________________")
            for r in f_list[int(index)].main.Runs:
                try:
                    print(f"{r.Id}: {r.igt}")
                except:
                    print("List index out of range")

                    #List command
        case ["list", index, option]:
            match option:
                case "-a": #-a for all
                    try:
                        fn.Info(f_list[int(index)].main)
                    except:
                        print(f"File \"{index}\" not yet loaded.")

                case "-b": #-b for best to worst
                    try:
                        fn.Best(f_list[int(index)].main)
                    except:
                        print(f"File \"{index}\" not yet loaded.")

                case option:#list a specific runs segments
                    try:
                        fn.InfoID(f_list[int(index)].main, option)
                    except:
                        print(f"File \"{index}\" not yet loaded.")

    #Command to compare one runs segment times to anothers
        case ["compare", file_1, id_1, file_2, id_2]:
            fn.Compare(f_list[int(file_1)].main, id_1, f_list[int(file_2)].main, id_2)

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

        #subtracts two times and prints the result
        case ["sub", theSubtrahend, theMinuend]:
            try:
                theDifference = fn.toSeconds(theSubtrahend) - fn.toSeconds(theMinuend)
                print(fn.toMinutes(theDifference))
            except:
                print("invalid format")

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
            print("     sub [Subtrahend] [Minuend]")
            print("         -subtrzcts two times and returns the result")
            print("         -format must be: 00:00:00.00")
            print("         -milliseconds not required, a single digit in each field is acceptable")

    main()
if __name__ == '__main__':
    main()
