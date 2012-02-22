import os
from ctypes import (c_void_p, c_int, c_short, c_uint, c_char_p, CFUNCTYPE, CDLL)

_lib_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../lib/fluidsynth")
_lib = CDLL(_lib_path)

c_void = c_int

def cfunc(name, result, *args):
    atypes = []
    aflags = []
    for arg in args:
        atypes.append(arg[1])
        if len(arg) == 2:
            arg = (arg[0], arg[1], 1)
        aflags.append((arg[2], arg[0]) + arg[3:])
    return CFUNCTYPE(result, *atypes)((name, _lib), tuple(aflags))

# Settings
new_fluid_settings = cfunc('new_fluid_settings', c_void_p)
delete_fluid_settings = cfunc('delete_fluid_settings', c_void_p)

# Synth
new_fluid_synth = cfunc('new_fluid_synth', c_void_p,
                        ('settings', c_void_p))
fluid_synth_sfload = cfunc('fluid_synth_sfload', c_int,
                           ('synth', c_void_p),
                           ('filename', c_char_p),
                           ('update_midi_presets', c_int))
fluid_synth_start = cfunc('fluid_synth_start', c_int,
                           ('synth', c_void_p))
fluid_synth_program_select = cfunc('fluid_synth_program_select', c_int,
                                   ('synth', c_void_p),
                                   ('chan', c_int),
                                   ('sfont_id', c_uint),
                                   ('bank_num', c_uint),
                                   ('preset_num', c_uint))
delete_fluid_synth = cfunc('delete_fluid_synth', c_void,
                           ('synth', c_void_p))

# Audio Driver
new_fluid_audio_driver = cfunc('new_fluid_audio_driver', c_void_p,
                               ('settings', c_void_p, 1),
                               ('synth', c_void_p, 1))
delete_fluid_audio_driver = cfunc('delete_fluid_audio_driver', None,
                                  ('driver', c_void_p, 1))

# Sequencers
new_fluid_sequencer2 = cfunc('new_fluid_sequencer2', c_void_p,
                             ('use_system_timer', c_int))
fluid_sequencer_register_fluidsynth = cfunc('fluid_sequencer_register_fluidsynth', c_short,
                                            ('seq', c_void_p),
                                            ('synth', c_void_p))
fluid_sequencer_send_at = cfunc('fluid_sequencer_send_at', c_int,
                                 ('seq', c_void_p),
                                 ('evt', c_void_p),
                                 ('time', c_uint),
                                 ('absolute', c_int))
delete_fluid_sequencer = cfunc('delete_fluid_sequencer', c_void,
                                ('seq', c_void_p))

# Events
new_fluid_event = cfunc('new_fluid_event', c_void_p)
fluid_event_set_source = cfunc('fluid_event_set_source', c_void, 
                               ('evt', c_void_p),
                               ('src', c_short))
fluid_event_set_dest = cfunc('fluid_event_set_dest', c_void, 
                               ('evt', c_void_p),
                               ('dest', c_short))
fluid_event_note = cfunc('fluid_event_note', c_int,
                         ('evt', c_void_p),
                         ('chan', c_int),
                         ('key', c_short),
                         ('vel', c_short),
                         ('duration', c_uint))
fluid_event_noteon = cfunc('fluid_event_noteon', c_int,
                           ('evt', c_void_p),
                           ('chan', c_int),
                           ('key', c_short),
                           ('vel', c_short))
fluid_event_noteoff = cfunc('fluid_event_noteoff', c_int,
                            ('evt', c_void_p),
                            ('chan', c_int),
                            ('key', c_short))
delete_fluid_event = cfunc('delete_fluid_event', c_void,
                               ('evt', c_void_p))

class Synth(object):
    def __init__(self):
        self.settings = new_fluid_settings()
        self.synth = new_fluid_synth(self.settings)
        self.audiodrv = None
        
    def load_sf2(self, filename, update_midi_preset=0):
        return fluid_synth_sfload(self.synth, filename, update_midi_preset)
    
    def program_select(self, channel, soundfont, bank, preset):
        return fluid_synth_program_select(self.synth, channel, soundfont, bank, preset)
    
    def start(self):
        if self.audiodrv == None:
            self.audiodrv = new_fluid_audio_driver(self.settings, self.synth)
        
    def stop(self):
        if self.audiodrv != None:
            delete_fluid_audio_driver(self.audiodrv)
            self.audiodrv = None
    
    def delete(self):
        self.stop()
        if self.synth != None:
            delete_fluid_synth(self.synth)
            self.synth = None
        if self.settings != None:
            delete_fluid_settings(self.settings)
            self.settings = None
            
    def __del__(self):
        self.delete()

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
    