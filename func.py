from types import NoneType
import xml.etree.ElementTree as et
import os

red         = "\033[31m"
green       = "\033[32m"
clear       = "\033[0m"

## Functions that extract data from the lss file ##

## Finders ##
#returns a list of all comparison names the file passed
def findComparisons(file):
    return {comparison.attrib['name'] for comparison in et.parse(file).getroot().iter("SplitTime")}

#returns a list of all attempt ids in the file passed
def findAttemptIDs(root):
    return [attempt.attrib['id'] for attempt in root.iter("Attempt")]

#returns a list of all segment names in the file passed
def findSegments(root):
    return [segment.text for segment in root.iter("Name")]

#returns a list of all completed runs' ids, and their times
def findCompleted(file, method=None):
    if method == "rta":
        return [
            (attempt.attrib['id'], time.text)
        for attempt in et.parse(file).getroot().iter("Attempt") 
        for time in attempt.iter("RealTime")
    ]

    elif method == "igt":
        return [
            (attempt.attrib['id'], time.text)
        for attempt in et.parse(file).getroot().iter("Attempt")
        for time in attempt.iter("GameTime")
    ]

#returns a list of all segment times recorded for the specified segment
def findRecordedSegmentTimes(root, name, method=None):
    if method == 'rta':
        return [
            tag.text
            for segment in root.iter("Segment")
            for time in segment.iter("Time")
            for tag in time.iter("RealTime")
            if segment.find("Name").text == name
        ]
    else:
        return [
            tag.text
            for segment in root.iter("Segment")
            for time in segment.iter("Time")
            for tag in time.iter("GameTime")
            if segment.find("Name").text == name
        ]

#returns a list of all segment times recorded for the specified attempt id
def findRunSegments(root, _id, method=None):
    if method == 'rta':
        return [
            (segment.find("Name").text, tag.text)
            for segment in root.iter("Segment")
            for time in segment.iter("Time")
            for tag in time.iter("RealTime")
            if time.get('id') == _id
        ]
    else:
        return [
            (segment.find("Name").text, tag.text)
            for segment in root.iter("Segment")
            for time in segment.iter("Time")
            for tag in time.iter("GameTime")
            if time.get('id') == _id
        ]

#pass a list of split times, return a list of segment times
#this one needs changed
def splitToSegment(splits):
    segments = []
    zero = 0
    for split in splits:
        segments.append(toSeconds(split) - zero)
        zero += toSeconds(split)
    return segments

#pass a list of segment times, return a list of split times
#segments must already be converted to seconds
def segmentToSplit(segments):
    return allMinutes(
        [round(sum(segments[0:index+1]), 2) for index, _ in enumerate(segments)]
    )

#returns a list of all completed runs in order from least to greatest time
def listBest(root, string):
    return [
        (zeroStrip(toMinutes(sort[0])), sort[1])
        for sort in sorted(
            [(toSeconds(attempt[1]), attempt[0]) for attempt in findCompleted(root, method=string)]
        )
    ]

#returns a list of the lower of two numbers in two zipped lists
def lowerSegment(l1, l2):
    return [x if x < y else y for x, y in zip(l1, l2)]

#prints a list of the better of each segment in two runs
def fastHybrid(root, id_1, id_2, method):
    run_1 = findRunSegments(root, id_1, method)
    run_2 = findRunSegments(root, id_2, method)
    segments = findSegments(root)
    length = len(max(segments, key=len))
    hybrid = lowerSegment(allSeconds(run_1), allSeconds(run_2))

    for index, segment in enumerate(segmentToSplit(hybrid)):
        print(segments[index].ljust(length, ' '), zeroStrip(segment))

#prints a comparison of two runs
#may be modified to optionally show split times instead of segment times
def fastCompare(root, id_1, id_2, method=None):
    run_1 = findRunSegments(root, id_1, method)
    run_2 = findRunSegments(root, id_2, method)
    segments = findSegments(root) #just to get the length of the longest segment

    for x, y in zip(run_1, run_2):
        diff = toSeconds(x[1]) - toSeconds(y[1])
        print(
            x[0].ljust(len(max(segments, key=len)), ' '), "|",
            zeroStrip(x[1]).ljust(10, ' '),
            green if diff <= 0 else red,
            str(round(diff, 2)).rjust(10, ' '),
            clear,
            zeroStrip(y[1]).rjust(15, ' ')
        )

#return the segment in which a run was reset on
def findResetPoint(root, _id):
    one = findSegments(root)[0]

    y = [
        segment for segment in reversed(
            [segment for segment in root.iter("Segment")]
        )
    ]

    x = [
        y[index-1].find("Name").text
        for index, segment in enumerate(y) 
        for time in segment.iter("Time") 
        if time.get("id") == _id
    ]

    #the list that x and y create isn't 100% perfect,
    #[index - 1] works for every segment besides the first one in the list
    #because (index = -1) returns the last item in a list
    #which would be the first segment on a finished run, since the list is reversed
    #so these two if statements fix that

    #if x[0] returns None, return the first segment
    if not len(x):
        return one

    #if x[0] returns the name of the first segment, don't return it
    if x[0] != one:
            return x[0]
    return

#print how many times each segment has been reset on
def fastResetCounter(root):
    segments = findSegments(root)
    resets = [findResetPoint(root, _id) for _id in findAttemptIDs(root)]
    counted = [resets.count(segment) for segment in segments]
    for index, count in enumerate(sorted(counted, reverse=1)):
        print(
            segments[index].ljust(len(max(segments, key=len)), ' '), 
            count
        )
    print(
        "Total:".ljust(len(max(segments, key=len)), ' '),
        sum(counted)
    )

#turns a string of time into a float
def toSeconds(string):
    #print("passed:", string)
    if string:
        x = string.split(':')
        return int(x[0])*3600 + int(x[1])*60 + float(x[2])
    return 0

#returns a string of time in the same format as in the lss file
def toMinutes(num):
    minutes, seconds = divmod(num, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{int(hours):02}:{int(minutes):02}:{round(seconds, 2):010.7f}"

def allMinutes(the_list):
    return [toMinutes(time) for time in the_list]

def allSeconds(the_list):
    return [toSeconds(time[1]) for time in the_list]

#cuts the leading and trailing zeroes off of a string of time
def zeroStrip(string):
    if string:
        return string.strip("0:")