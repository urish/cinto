'''
Created on Feb 22, 2012

@author: Uri
'''

import time
import fluid2
import os

class CintoEngine(object):
    def __init__(self):
        myPath = os.path.dirname(os.path.abspath(__file__))
        self.synth = fluid2.Synth(gain=1.0)
        self.sequencer = fluid2.Sequencer()
        self.sequencer.attach(self.synth)
        self.soundFont = self.synth.sfload(os.path.join(myPath, "../media/FluidR3 GM.sf2"))
        self.quarter = 250
        self.time = 100
        self.chords = (0, 4, 7, 4, 7, 12, 4, 7)
        self.chordIndex = 0
        
    def start(self):
        self.synth.start()
        self.synth.program_select(0, self.soundFont, 0, 0)
        self.synth.program_select(1, self.soundFont, 0, 33)
        self.synth.program_select(2, self.soundFont, 0, 27)
        while True:
            self.nextMeasure()
            time.sleep(0.1)
            
    def nextMeasure(self):
        b=60 + self.chords[self.chordIndex % len(self.chords)]
        self.sequencer.send_note(self.time, 0, b+0, 127, int(self.quarter * 0.95))
        self.sequencer.send_note(self.time, 1, b-24, 127,  int(self.quarter * 3.95))
        self.time += self.quarter
        self.sequencer.send_note(self.time, 0, b+4, 127, int(self.quarter * 0.95))
        self.sequencer.send_note(self.time, 2, b+16, 80, int(self.quarter * 2.95))
        self.time += self.quarter
        self.sequencer.send_note(self.time, 0, b+7, 127, int(self.quarter * 0.95))
        self.time += self.quarter
        self.sequencer.send_note(self.time, 0, b+12, 127, int(self.quarter * 0.95))
        self.time += self.quarter
        self.chordIndex += 1

def main():
    cinto = CintoEngine()
    cinto.start()

if __name__ == '__main__':
    main()