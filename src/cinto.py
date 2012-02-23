'''
Created on Feb 22, 2012

@author: Uri
'''

import time
import fluid
import os

class CintoEngine(object):
    def __init__(self):
        myPath = os.path.dirname(os.path.abspath(__file__))
        self.synth = fluid.Synth()
        self.sequencer = fluid.Sequencer()
        self.sequencer.attach(self.synth)
        self.soundFont = self.synth.load_sf2(os.path.join(myPath, "../media/FluidR3 GM.sf2"))
        self.quarter = 250
        self.time = 0
        self.chords = (0, 4, 7, 4, 7, 12, 4, 7)
        self.chordIndex = 0
        self.running = False
        
    def start(self):
        self.synth.start()
        self.synth.program_select(0, self.soundFont, 0, 0)
        self.synth.program_select(1, self.soundFont, 0, 33)
        self.synth.program_select(2, self.soundFont, 0, 27)
        self.running = True
    
    def stop(self):
        self.synth.stop()
        self.running = False
        
    def loop(self):
        while True:
            self.nextMeasure()
            time.sleep(1)
            
    def nextMeasure(self):
        if self.time < self.sequencer.get_tick():
            self.time = self.sequencer.get_tick() + 10
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
    cinto.loop()


if __name__ == '__main__':
    main()