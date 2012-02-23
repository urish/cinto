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
        self.tracks = [[127,0], [127,0], [127,0], [127,0]]
        
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
            
    def updateTrack(self, channel, gain, pitch):
        self.tracks[channel-1] = [int(gain * 127), int(pitch * 12)]
        
    def sendNote(self, channel, pitch, length):
        gain = self.tracks[channel][0]
        pitch += self.tracks[channel][1]
        self.sequencer.send_note(self.time, channel, pitch, gain, length)
                    
    def nextMeasure(self):
        _gain = lambda x: self.tracks[x][0]
        _pitch = lambda x: self.tracks[x][1]
        if self.time < self.sequencer.get_tick():
            self.time = self.sequencer.get_tick() + 10
        b=60 + self.chords[self.chordIndex % len(self.chords)]
        self.sendNote(0, b+0, int(self.quarter * 0.95))
        self.sendNote(1, b-24, int(self.quarter * 3.95))
        self.time += self.quarter
        self.sendNote(0, b+4, int(self.quarter * 0.95))
        self.sendNote(2, b+16, int(self.quarter * 2.95))
        self.time += self.quarter
        self.sendNote(0, b+7, int(self.quarter * 0.95))
        self.time += self.quarter
        self.sendNote(0, b+12, int(self.quarter * 0.95))
        self.time += self.quarter
        self.chordIndex += 1

def main():
    cinto = CintoEngine()
    cinto.start()
    cinto.loop()


if __name__ == '__main__':
    main()