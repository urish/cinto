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
        self.tracks = [[1,1], [1,0], [.8,.6], [.8,.4]]
        self.programs = [
            [(0, 0, 3.95)],
            [(0, 0, 1.95), (2, 0, 1.95)],
            [(0, 0, 0.95), (2, 4, 0.95)],
            [(0, 0, 0.95), (1, 4, 0.95), (2, 7, 0.95), (3, 4, 0.95)],
        ]
        
    def start(self):
        self.synth.start()
        self.synth.program_select(0, self.soundFont, 0, 0)
        self.synth.program_select(1, self.soundFont, 0, 33)
        self.synth.program_select(2, self.soundFont, 0, 27)
        self.synth.program_select(3, self.soundFont, 0, 55)
        self.running = True
    
    def stop(self):
        self.synth.stop()
        self.running = False
        
    def loop(self):
        while True:
            self.nextMeasure()
            time.sleep(1)

    def getTrack(self, channel):
        return self.tracks[channel-1]
                    
    def updateTrack(self, channel, gain, program):
        self.tracks[channel-1] = [gain, program]
                      
    def nextMeasure(self):
        if self.time < self.sequencer.get_tick():
            self.time = self.sequencer.get_tick() + 10
        b=60 + self.chords[self.chordIndex % len(self.chords)]
        for channel in range(4):
            gain, program = self.tracks[channel]
            program = self.programs[int(program * (len(self.programs) - 0.0001))]
            for index, pitch, duration in program:
                if channel == 1:
                    pitch -= 24
                startTime = int(self.time + index * self.quarter) 
                duration = int(duration * self.quarter)
                self.sequencer.send_note(startTime, channel, b + pitch, int(gain * 127), duration)
        self.time += 4 * self.quarter
        self.chordIndex += 1

def main():
    cinto = CintoEngine()
    cinto.start()
    cinto.loop()


if __name__ == '__main__':
    main()