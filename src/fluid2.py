from fluidsynth import *

c_void = c_int

# Sequencers
new_fluid_sequencer2 = cfunc('new_fluid_sequencer2', c_void_p,
                             ('use_system_timer', c_int, 1))
fluid_sequencer_register_fluidsynth = cfunc('fluid_sequencer_register_fluidsynth', c_short,
                                            ('seq', c_void_p, 1),
                                            ('synth', c_void_p, 1))
fluid_sequencer_send_at = cfunc('fluid_sequencer_send_at', c_int,
                                 ('seq', c_void_p, 1),
                                 ('evt', c_void_p, 1),
                                 ('time', c_uint, 1),
                                 ('absolute', c_int, 1))
delete_fluid_sequencer = cfunc('delete_fluid_sequencer', c_void,
                                ('seq', c_void_p, 1))

# Events
new_fluid_event = cfunc('new_fluid_event', c_void_p)
fluid_event_set_source = cfunc('fluid_event_set_source', c_void, 
                               ('evt', c_void_p, 1),
                               ('src', c_short, 1))
fluid_event_set_dest = cfunc('fluid_event_set_dest', c_void, 
                               ('evt', c_void_p, 1),
                               ('dest', c_short, 1))
fluid_event_note = cfunc('fluid_event_note', c_int,
                         ('evt', c_void_p, 1),
                         ('chan', c_int, 1),
                         ('key', c_short, 1),
                         ('vel', c_short, 1),
                         ('duration', c_uint, 1))
fluid_event_noteon = cfunc('fluid_event_noteon', c_int,
                           ('evt', c_void_p, 1),
                           ('chan', c_int, 1),
                           ('key', c_short, 1),
                           ('vel', c_short, 1))
fluid_event_noteoff = cfunc('fluid_event_noteoff', c_int,
                            ('evt', c_void_p, 1),
                            ('chan', c_int, 1),
                            ('key', c_short, 1))
delete_fluid_event = cfunc('delete_fluid_event', c_void,
                               ('evt', c_void_p, 1))

class Event(object):
    def __init__(self, source = None, dest = None):
        self.event = new_fluid_event()
        if source != None:
            fluid_event_set_source(self.event, source)
        if dest != None:
            fluid_event_set_dest(self.event, dest)
        
    def note(self, channel, key, velocity, duration):
        fluid_event_note(self.event, channel, key, velocity, duration)
                
    def note_on(self, channel, key, velocity):
        fluid_event_noteon(self.event, channel, key, velocity)

    def note_off(self, channel, key):
        fluid_event_noteoff(self.event, channel, key)
        
    def delete(self):
        if self.event != None:
            delete_fluid_event(self.event)
            self.event = None        

    def __enter__(self):
        return self
        
    def __exit__(self, _type, value, trackback):
        self.delete()
                
    def __del__(self):
        self.delete()

class Sequencer(object):
    (TIMER_LOCAL, 
     TIMER_SYSTEM) = range(2)
    
    def __init__(self, timer_type = TIMER_LOCAL):
        self.sequencer = new_fluid_sequencer2(timer_type)
    
    def attach(self, synth):
        self.seq_id = fluid_sequencer_register_fluidsynth(self.sequencer, synth.synth)
        return self.seq_id

    def send_note(self, time, chan, key, velocity, duration):
        with Event(-1, self.seq_id) as event:
            event.note(chan, key, velocity, duration)
            return self.send_event(time, event)
    
    def send_note_on(self, time, chan, key, velocity):
        with Event(-1, self.seq_id) as event:
            event.note_on(chan, key, velocity)
            return self.send_event(time, event)

    def send_note_off(self, time, chan, key):
        with Event(-1, self.seq_id) as event:
            event.note_off(chan, key)
            return self.send_event(time, event)
    
    def send_event(self, time, event, is_absolute = True):
        is_absolute = int(is_absolute)
        return fluid_sequencer_send_at(self.sequencer, event.event, time, is_absolute)
    
    def delete(self):
        if self.sequencer != None:
            delete_fluid_sequencer(self.sequencer)
            self.sequencer = None
    
    def __del__(self):
        self.delete()
    