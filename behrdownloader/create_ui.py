#!/usr/bin/env python
# https://wiki.python.org/moin/PortingToPy3k/BilingualQuickRef
from __future__ import absolute_import, division, print_function, unicode_literals

from collections import OrderedDict

from . import download_behr as getbehr

__metaclass__ = type  # Automatically makes Python 2 classes inherit from object to be new-style classes


try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

class GetBEHRGuiMain():
    def __init__(self, root_window):
        self.root_window = root_window
        self.root_window.title('BEHRDownloader')

        self.download_panel = GetBEHRGuiDownload(self)

        self.close_button = tk.Button(self.root_window, text="Exit", command=self.root_window.quit)
        self.close_button.pack()

class GetBEHRGuiDownload():
    # The first region listed will always be the default.
    # The keys should be the name you want listed in the options menu, the value should be the abbreviation used in the
    # BEHR file names and the file hierarchy
    regions_dict = OrderedDict([('United States', 'US'), ('Hong Kong', 'HK')])
    prof_modes_list = ['Monthly', 'Daily']

    def __init__(self, main_instance):
        self.main = main_instance
        self.root_window = main_instance.root_window
        self._create_selectors()

    def _create_selectors(self):
        self.region_label = tk.Label(self.root_window, text="Region")
        self.region_label.pack()

        self.region = tk.StringVar(self.root_window)
        self.region.set(self.regions_dict.keys()[0])
        self.region_dropdown = tk.OptionMenu(self.root_window, self.region, *self.regions_dict.keys())
        self.region_dropdown.pack()

        self.profmode_label = tk.Label(self.root_window, text="Profile time resolution")
        self.profmode_label.pack()

        self.profmode = tk.StringVar(self.root_window)
        self.profmode.set(self.prof_modes_list[0])
        self.profmode_dropdown = tk.OptionMenu(self.root_window, self.profmode, *self.prof_modes_list)
        self.profmode_dropdown.pack()

        self.startdate_label = tk.Label(self.root_window, text="Start date")
        self.startdate_label.pack()

        self.startdate = tk.StringVar(self.root_window)
        self.startdate_input = tk.Entry(self.root_window, textvariable=self.startdate)
        self.startdate.set('2005-01-01')
        self.startdate_input.pack()

        self.startdate_label = tk.Label(self.root_window, text="End date")
        self.startdate_label.pack()

        self.enddate = tk.StringVar(self.root_window)
        self.enddate_input = tk.Entry(self.root_window, textvariable=self.enddate)
        self.enddate.set('2016-12-31')
        self.enddate_input.pack()

        self.list_button = tk.Button(self.root_window, text='List files', command=self.db_print_files)
        self.list_button.pack()

    def db_print_files(self):
        region = self.region.get()
        region_abbr = self.regions_dict[region]
        getbehr.print_file_list_debug(region_abbr, self.profmode.get(), self.startdate.get(), self.enddate.get())

if __name__ == '__main__':
    root = tk.Tk()
    my_gui = GetBEHRGuiMain(root)
    # https://stackoverflow.com/questions/1892339/how-to-make-a-tkinter-window-jump-to-the-front
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)
    root.mainloop()