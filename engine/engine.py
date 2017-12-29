# vim:set et sts=4 sw=4:
#
# ibus-deepspeech - Speech recognition engine for IBus
#
# Copyright (c) 2017 Mike Sheldon <elleo@gnu.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function

import gi

gi.require_version('IBus', '1.0')
from gi.repository import IBus
gi.require_version('Pango', '1.0')
from gi.repository import Pango
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst

GObject.threads_init()
Gst.init(None)

class EngineDeepSpeech(IBus.Engine):
    __gtype_name__ = 'EngineDeepSpeech'

    def __init__(self):
        super(EngineDeepSpeech, self).__init__()
        self.recording = False
        self.__is_invalidate = False
        self.__preedit_string = ""
        self.__prop_list = IBus.PropList()
        self.__prop_list.append(IBus.Property(key="toggle-recording", icon="audio-input-microphone", type=IBus.PropType.TOGGLE, state=0, tooltip="Toggle speech recognition"))

        self.pipeline = Gst.parse_launch("pulsesrc ! audioconvert ! audiorate ! audioresample ! deepspeech silence-threshold=0.3 silence-length=20 ! fakesink")
        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect ("message", self.bus_message)

    def do_focus_in(self):
        self.register_properties(self.__prop_list)

    def do_property_activate(self, prop_name, state):
        if prop_name == 'toggle-recording':
            self.recording = bool(state)
            if self.recording:
                self.pipeline.set_state(Gst.State.PLAYING)
            else:
                self.pipeline.set_state(Gst.State.PAUSED)

    def bus_message(self, bus, message):
        structure = message.get_structure()
        if structure and structure.get_name() == "deepspeech":
            text = structure.get_value("text")
            self.commit_text(IBus.Text.new_from_string(text))
        return True

