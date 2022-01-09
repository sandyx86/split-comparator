import xml.etree.ElementTree as et
import os

import classes as cl

red         = "\033[31m"
green       = "\033[32m"
clear       = "\033[0m"

## Functions that extract data from the lss file ##
def load_file(file):
    file_object = cl.File(file)
    for attempt in findAttempts(file_object):
        file_object.attempts.append(buildRun(file_object, attempt))
    
    for comparison in findComparisons(file_object):
        file_object.comparisons.append(buildComparison(file_object, comparison))
    
    return file_object

#returns a list of all comparisons in a file
#fix duplicate comparisons
def findComparisons(file):
    comparison_list = []
    for segment in file.root.iter("Segment"):
        for comparison in segment.iter("SplitTime"):
            if comparison.attrib['name'] in comparison_list:
                break
            comparison_list.append(comparison.attrib['name'])
    return comparison_list

#returns a list of all ids in the file passed
def findAttempts(file):
    attempt_list = []
    for attempt in file.root.iter("Attempt"):
        attempt_list.append(attempt.attrib['id'])
    
    #print("Attempts found:", len(attempt_list))
    return attempt_list

#returns a list of all segments in the file passed
def findSegments(file):
    segment_list = []
    for segment in file.root.iter("Name"):
        segment_list.append(segment.text)
        #print(segment.text)
    
    #print("Segments Found:", len(segment_list))
    return segment_list

#returns a run object of the name of the comparison passed
def buildComparison(file, name):
    run_object = cl.Run()
    run_object.id = name

    for segment in findSegments(file):
        run_object.segments.append(buildComparisonSegment(file, segment, name))
        #print("Apped:", buildComparisonSegment(file, segment, name).rta)
    
    return run_object

#returns a run object of the best segments in a file
def buildSumOfBest(file):
    run_object = cl.Run()
    run_object.id = "Sum of Best"

    for segment in findSegments(file):
        run_object.segments.append(buildBestSegment(file, segment))
    
    #a run object has an rta variable so just put he sum of best in self.rta
    #need a function to convert split times to segment times + vice versa
    
    return run_object

#returns a run object of the id passed
def buildRun(file, _id):
    run_object = cl.Run()
    run_object.id = _id

    for attempt in file.root.iter("Attempt"):
        if _id == attempt.attrib['id']:
            if len(attempt) == 2:
                run_object.rta = attempt[0].text
                run_object.igt = attempt[1].text
            elif len(attempt) == 1:
                run_object.rta = attempt[0].text
                run_object.igt = "None"
            else:
                run_object.rta = "None"
                run_object.igt = "None"
    
    for segment in findSegments(file):
        run_object.segments.append(buildSegment(file, segment, _id))

    #passCheck(run_object)
    return run_object

#returns a segment object of the split name and id passed
def buildSegment(file, name, _id):
    segment_object = cl.Segment()
    segment_object.name = name

    for segment in file.root.iter("Segment"):
        if name == segment.find("Name").text:
            for time in segment.iter("Time"):
                if _id == time.attrib['id']:
                    if len(time) == 2:
                        segment_object.rta = time[0].text
                        segment_object.igt = time[1].text
                    elif len(time) == 1:
                        segment_object.rta = time[0].text
                        segment_object.igt = "None"
                    elif len(time) == 0:
                        segment_object.rta = "None"
                        segment_object.igt = "None"       
                    else:
                        print("what")

    #print(segment_object.name, segment_object.igt) 
    return segment_object

#returns a list of ids for which a segment has recorded times for
def findSegmentIDs(file, name):
    seg_list = []
    for segment in file.root.iter("Segment"):
        if name == segment.find("Name").text:
            for time in segment.iter("Time"):
                seg_list.append(time.attrib['id'])
    return seg_list

#returns a segment object of the split name and comparison name passed
def buildComparisonSegment(file, splitname, name):
    segment_object = cl.Segment()
    segment_object.name = splitname

    for segment in file.root.iter("Segment"):
        # if splitname == <Name></Name>
        if splitname == segment[0].text: 
            
            #for splittime in <SplitTimes></SplitTimes>
            for split_time in segment[2]:
                for time in split_time.iter("SplitTime"):
                    if name == split_time.attrib['name']:
                        if len(split_time) == 2:
                            segment_object.rta = time[0].text
                            segment_object.igt = time[1].text
                        elif len(split_time) == 1:
                            segment_object.rta = time[0].text
                            segment_object.igt = "None"
                        else:
                            segment_object.rta = "None"
                            segment_object.igt = "None"
    return segment_object

#returns a segment object of the best segment of the split name passed
def buildBestSegment(file, splitname):
    segment_object = cl.Segment()
    segment_object.name = splitname

    for segment in file.root.iter("Segment"):
        if splitname == segment[0].text:
            for time in segment.iter("BestSegmentTime"):
                if len(time) == 2:
                    segment_object.rta = time[0].text
                    segment_object.igt = time[1].text
                elif len(time) == 1:
                    segment_object.rta = time[0].text
                    segment_object.igt = "None"
                else:
                    segment_object.rta = "None"
                    segment_object.igt = "None"
    return segment_object

## Functions that operate on the data extracted ##

#Comparison function
#compare the whole object, find rta and igt and store it
#pass two segment objects to this func
def buildDeltaSegment(name, s1, s2):
    dsegment = cl.DeltaSegment()
    dsegment.name = name
    dsegment.rta = toSeconds(s1.rta) - toSeconds(s2.rta)
    dsegment.igt = toSeconds(s1.igt) - toSeconds(s2.igt)
    return dsegment

def buildDeltaRun(run_1, run_2):
    drun = cl.DeltaRun()
    
    #all return empty strings
    #passCheck(run_1)
    #passCheck(run_2)

    for seg_1, seg_2 in zip(run_1.segments, run_2.segments):
        drun.segments.append(buildDeltaSegment(seg_1.name, seg_1, seg_2))

    for segment in drun.segments:
        if segment.rta > 0:
            drun.p_rta = float(drun.p_rta) + float(segment.rta)
        else:
            drun.n_rta = float(drun.n_rta) + float(segment.rta)
        
        if segment.igt > 0:
            drun.p_igt = float(drun.p_rta) + float(segment.igt)
        else:
            drun.n_igt = float(drun.n_rta) + float(segment.igt)

    drun.t_rta = totalAdder(drun.segments, 'rta')
    drun.t_igt = totalAdder(drun.segments, 'igt')
    #make a totalAdder function
    
    return drun

#for use with buildDeltaRun(), the segment times should already be floats / doubles
def totalAdder(seg_list, method):
    if method == 'rta':
        adder = []
        for segment in seg_list:
            adder.append(segment.rta)
        added = sum(adder)
        return added
    
    if method == 'igt':
        adder = []
        for segment in seg_list:
            adder.append(segment.igt)
        added = sum(adder)
        return added
    
    return

#pass a list of split times, return a list of segment times
def splitToSegment(splits):
    segments = []
    zero = 0
    for split in splits:
        segments.append(toSeconds(split) - zero)
        zero = toSeconds(split)
    return segments


#pass a list of segment times, return a list of split times
def segmentToSplit(segments):
    splits = []
    zero = 0
    for segment in segments:
        splits.append(toSeconds(segment) + zero)
        zero = toSeconds(segment)
    return splits
    
#find a clean way to write this spaghetti code
def runCompare(run_1, run_2):
    delta_run = buildDeltaRun(run_1, run_2)

    #for determining the length of the longest segment name
    segment_list = []
    for segment in run_1.segments:
        segment_list.append(segment.name)
    
    #print the comparison of each segment
    for index, segment in enumerate(run_1.segments):
        print(
            segment.name.ljust(len(max(segment_list, key=len)), ' '),
            zeroStrip(
                segment.igt
            ).ljust(10, ' '),

            green if delta_run.segments[index].igt <= 0 else red,

            str(
                round(delta_run.segments[index].igt, 2)
            ).rjust(10, ' '),

            clear,
            
            zeroStrip(
                run_2.segments[index].igt
            ).rjust(15, ' ')
        )
    
    print("-" * (40 + len(max(segment_list, key=len))))

    #print the sum of all positive splits
    print(
        "Total".ljust(len(max(segment_list, key=len)), ' '),
        zeroStrip(
            run_1.igt
        ).ljust(10, ' '),
        
        red,

        str(
            round(delta_run.p_igt, 2)
        ).rjust(10, ' '),
        
        clear,

        zeroStrip(
            run_2.igt
        ).rjust(15, ' ')
    )

    #print the sum of all negative splits
    print(
        green,
        str(
            round(delta_run.n_igt, 2)
        ).rjust(len(max(segment_list, key=len)) + 22, ' '),
        clear
    )

    #print the sum of all positive and negative splits
    print(
        str(
            round(delta_run.t_igt, 2)
        ).rjust(len(max(segment_list, key=len)) + 23, ' ')
    )
        
def toSeconds(string):
    if string:
        x = string.split(':')
        return int(x[0])*3600 + int(x[1])*60 + float(x[2])
    return 0

#this can be improved with if else
def toMinutes(num):
    theMinutes = int(num / 60)
    theSeconds = num % 60
    return f"{theMinutes:02}:{round(theSeconds, 2):05}"

def zeroStrip(string):
    return string.strip("0:")

def passCheck(run):
    for segment in run.segments:
        print(segment.rta)
        pass


                
        
    


