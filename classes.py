import xml.etree.ElementTree as et
import os
import func as fn

class File():
    def __init__(self, file):
        self.tree = et.parse(file)
        self.root = self.tree.getroot()
        self.Filename = file #might need to be changed

        self.game_name = self.root.find("GameName").text
        self.cat_name = self.root.find("CategoryName").text
        self.attempt_count = self.root.find("AttemptCount").text

        self.attempts = [] #each attempt is a run object
        self.comparisons = []
        self.golds = fn.buildSumOfBest(self)

class Run():
    def __init__(self):
        self.id = ''
        self.segments = []
        self.rta = ''
        self.igt = ''

class Segment():
    def __init__(self):
        self.name = ''
        self.rta = ''
        self.igt = ''

class DeltaRun():
    def __init__(self):
        self.t_rta = ''
        self.t_igt = ''
        self.p_rta = 0
        self.n_rta = 0
        self.p_igt = 0
        self.n_igt = 0
        self.segments = []

class DeltaSegment():
    def __init__(self):
        self.name = ''
        self.rta = ''
        self.igt = ''