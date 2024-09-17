#!/usr/bin/env python3

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib


class MyWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Hello World")
        
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)

        self.button1 = Gtk.Button(label="Set Max Frequency")
        self.button1.connect("clicked", self.on_button1_clicked)
        self.grid.attach(self.button1, 0, 0, 1, 1)

        self.SYSDIR = "/sys/devices/system/cpu/cpufreq/policy0"
        freqs = open(f"{self.SYSDIR}/scaling_available_frequencies", "r").read().split()
        
        self.frequency = int(open(f"{self.SYSDIR}/scaling_max_freq", "r").read())
        
        self.scale1 = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, int(freqs[0]), int(freqs[-1]), 100)
        self.scale1.set_value(self.frequency)
        for freq in freqs:
            self.scale1.add_mark(int(freq), Gtk.PositionType.TOP, None)
        self.scale1.connect("value-changed", self.on_scale1_slided)
        
        self.grid.attach(self.scale1, 1, 0, 2, 1)
        
        self.label1 = Gtk.Label(label="Cur Freq")
        self.grid.attach(self.label1, 1, 1, 1, 1)
        
        # Core enable|disable
        self.core23_enabled = True
        self.button2 = Gtk.Button(label="Disable core 2,3")
        self.button2.connect("clicked", self.on_button2_clicked)
        self.grid.attach(self.button2, 0, 1, 1, 1)
        
        GLib.timeout_add(250, self.on_timeout, None)
        
        self.add(self.grid)

    def on_timeout(self, widget):
        cur_freq_str = open(f"{self.SYSDIR}/scaling_cur_freq", "r").read()
        
        self.label1.set_label(f"Cur Freq: {cur_freq_str}")
        GLib.timeout_add(250, self.on_timeout, None)
        
    def on_scale1_slided(self, adjustment):
        value = adjustment.get_value()
        open(f"{self.SYSDIR}/scaling_max_freq", "w").write(str(int(value)))
        self.frequency = value

    def on_button1_clicked(self, widget):
        open(f"{self.SYSDIR}/scaling_max_freq", "w").write(str(self.frequency))

    def on_button2_clicked(self, widget):
        self.core23_enabled = not self.core23_enabled
        
        open("/sys/devices/system/cpu/cpu2/online", "w").write(str(int(self.core23_enabled)))
        open("/sys/devices/system/cpu/cpu3/online", "w").write(str(int(self.core23_enabled)))
        
        if self.core23_enabled:
            self.button2.set_label("Disable core 2,3")
        else:
            self.button2.set_label("Enable core 2,3")


win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
