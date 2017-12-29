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

# for python2
from __future__ import print_function

import gi
import os
import sys
import getopt
import locale

gi.require_version('IBus', '1.0')
from gi.repository import IBus
from gi.repository import GLib
from gi.repository import GObject

from engine import EngineDeepSpeech

class IMApp:
    def __init__(self, exec_by_ibus):
        engine_name = "deepspeech" if exec_by_ibus else "deepspeech (debug)"
        self.__component = \
                IBus.Component.new("org.freedesktop.IBus.DeepSpeech",
                                   "DeepSpeech Speech Recognition Component",
                                   "0.1.0",
                                   "GPL",
                                   "Mike Sheldon <elleo@gnu.org>",
                                   "https://github.com/Elleo/ibus-deepspeech",
                                   "/usr/bin/exec",
                                   "ibus-deepspeech")
        engine = IBus.EngineDesc.new("deepspeech",
                                     engine_name,
                                     "English Speech Recognition (DeepSpeech)",
                                     "en",
                                     "GPL",
                                     "Mike Sheldon <elleo@gnu.org>",
                                     "",
                                     "us")
        self.__component.add_engine(engine)
        self.__mainloop = GLib.MainLoop()
        self.__bus = IBus.Bus()
        self.__bus.connect("disconnected", self.__bus_disconnected_cb)
        self.__factory = IBus.Factory.new(self.__bus.get_connection())
        self.__factory.add_engine("deepspeech",
                GObject.type_from_name("EngineDeepSpeech"))
        if exec_by_ibus:
            self.__bus.request_name("org.freedesktop.IBus.DeepSpeech", 0)
        else:
            self.__bus.register_component(self.__component)
            self.__bus.set_global_engine_async(
                    "deepspeech", -1, None, None, None)

    def run(self):
        self.__mainloop.run()

    def __bus_disconnected_cb(self, bus):
        self.__mainloop.quit()


def launch_engine(exec_by_ibus):
    IBus.init()
    IMApp(exec_by_ibus).run()

def print_help(v = 0):
    print("-i, --ibus             executed by IBus.")
    print("-h, --help             show this message.")
    print("-d, --daemonize        daemonize ibus")
    sys.exit(v)

def main():
    try:
        locale.setlocale(locale.LC_ALL, "")
    except:
        pass

    exec_by_ibus = False
    daemonize = False

    shortopt = "ihd"
    longopt = ["ibus", "help", "daemonize"]

    try:
        opts, args = getopt.getopt(sys.argv[1:], shortopt, longopt)
    except getopt.GetoptError as err:
        print_help(1)

    for o, a in opts:
        if o in ("-h", "--help"):
            print_help(sys.stdout)
        elif o in ("-d", "--daemonize"):
            daemonize = True
        elif o in ("-i", "--ibus"):
            exec_by_ibus = True
        else:
            sys.stderr.write("Unknown argument: %s\n" % o)
            print_help(1)

    if daemonize:
        if os.fork():
            sys.exit()

    launch_engine(exec_by_ibus)

if __name__ == "__main__":
    main()
