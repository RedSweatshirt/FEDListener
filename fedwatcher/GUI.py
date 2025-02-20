import tkinter
import tkinter.filedialog
from tkinter import messagebox as tkMessageBox
import os
import pandas as pd
import numpy as np
import tkinter.ttk as ttk
import datetime
from configparser import ConfigParser
from src.fedwatcher import Fedwatcher
import re
import datetime
import webbrowser
from PIL import ImageTk, Image
import time

class App():
	def __init__(self, window, window_title):
		# aesthetics -------
		self.window = window
		self.window.title(window_title)
		self.bg_color = "#424547"
		self.fg_color = "#E1ECF2"
		self.window.configure(bg=self.bg_color)
		self.button_color = "#7E8487"
		self.start_color = "#C9FFCB"
		self.stop_color = "#FF959D"
		self.button_width = 30
		self.left_pad = 20

		# find out where GUI.py is located
		dir_path = os.path.dirname(os.path.realpath(__file__))
		version_path = os.path.join(os.path.dirname(dir_path), "version.txt")

		# TODO: version
		#self.version = "0.0.1"
		#self.version = "version.txt".readline()
		with open(version_path, 'r') as f:
			self.version = f.readline()

		# top menu
		self.menu_top = tkinter.Frame(self.window, bg=self.bg_color)
		image1 = Image.open(os.path.join(dir_path, 'img/64.png'))
		self.test = ImageTk.PhotoImage(image1)
		self.logo = tkinter.Label(self.menu_top, image=self.test)
		self.logo.image = self.test
		# Position image
		#self.label1.place(x=20, y=20)
		self.app_title = tkinter.Label(self.menu_top, text = "FEDWatcher", font = ("Helvetica", 20), bg = self.bg_color, fg = self.fg_color)
		# Middle menu left -------
		# also explore menu bar ?
		# https://pythonspot.com/tk-menubar/
		self.menu_left = tkinter.Frame(self.window, width=80, height=80, bg=self.bg_color)
		self.menu_left_upper = tkinter.Frame(self.menu_left, width=80, height=80, bg=self.bg_color, highlightcolor="black", highlightthickness=0)
		
		self.menu_left_title = tkinter.Label(self.menu_left_upper,
		 text="Experiment Info",
		 font=("Helvetica", 16), bg=self.bg_color, fg = self.fg_color)
		
		self.exp_name = tkinter.Label(self.menu_left_upper,
		 text="Exp. Name:", pady=5, bg=self.bg_color, width=10, fg = self.fg_color)
		self.exp_entry = tkinter.Entry(self.menu_left_upper, width=20)
		self.treatment_label = tkinter.Label(self.menu_left_upper,
		 text="Treatment:", pady=5, bg=self.bg_color, width=10, fg = self.fg_color)
		self.email_label = tkinter.Label(self.menu_left_upper,
		 text="Email:", pady=5, bg=self.bg_color, width=10)
		self.email_entry = tkinter.Entry(self.menu_left_upper, width=20)
		self.password_label = tkinter.Label(self.menu_left_upper,
		 text="Password:", pady=5, bg=self.bg_color, width=10)
		self.password_entry = tkinter.Entry(self.menu_left_upper, show="*", width=20)

		self.telegram_var = tkinter.BooleanVar()
		self.telegram_checkbox = tkinter.Checkbutton(self.menu_left_upper, text="Activate Telegram Bot", variable=self.telegram_var)


		# Checkbox for remembering
		#self.remember = tkinter.IntVar(value = 0)
		#self.delete = tkinter.IntVar(value = 1)

		#self.delete_check = tkinter.Checkbutton(self.menu_left_upper, text='Do not remember me',
		#	variable=self.delete, onvalue=1, offvalue=0, command=self.delete_info, 
		#	bg = self.bg_color, fg = self.fg_color, pady = 5, selectcolor = "#000000")
		#self.remember_check = tkinter.Checkbutton(self.menu_left_upper, text='Remember me',
		#	variable=self.remember, onvalue=1, offvalue=0, command=self.remember_info, 
		#	bg = self.bg_color, fg = self.fg_color, pady = 1, selectcolor = "#000000")


		# make the grid of entries
		# labels
		self.exp_name.grid(row=1, column=0,sticky="ne")
		self.email_label.grid(row=2,column=0,sticky="ne")
		self.password_label.grid(row=3, column=0, sticky="ne")
		# entries
		self.exp_entry.grid(row=1,column=1, sticky='ew',padx=1)
		self.email_entry.grid(row=2,column=1, sticky='ew',padx=1)
		self.password_entry.grid(row=3,column=1, sticky='ew',padx=1)
		# checkbox
		self.telegram_checkbox.grid(row=4, column=1, sticky='ne', padx=1)
		#self.delete_check.grid(row=4, column=1, sticky='ne', padx=1)
		#self.remember_check.grid(row=5, column=1, sticky='ne', padx=1)

		# insert and delete stuff -------
		#self.insert_button = tkinter.Button(self.menu_left_upper, text="Insert",
		#                                    command=self.insert_data,
		#                                    width=4, bg=self.button_color,
		#                                    highlightbackground="black")
		#self.delete_button = tkinter.Button(self.menu_left_upper, text='Delete',
        #                               command=self.delete_entry,
        #                               state=tkinter.DISABLED,
        #                               width=4, bg=self.button_color,
        #                               highlightbackground="black")
		# make an empty label for space
		self.spacer_label = tkinter.Label(self.menu_left_upper,
		 text="", pady=5, bg=self.bg_color, width=2)
		self.spacer_label.grid(row=0,column=2, pady=5)
		#self.insert_button.grid(row=4,column=3, pady=5)
		#self.delete_button.grid(row=4,column=4, sticky='nsew', pady=5)

		# right area ----------
		self.menu_right = tkinter.Frame(self.window, bg=self.bg_color)

		self.menu_right_title = tkinter.Label(self.menu_right,
		 text="Experiment Control", bg=self.bg_color, fg = self.fg_color,
		font=("Helvetica", 16))
		self.menu_right_title.pack()
	
		# Buttons -----
		self.create_project = tkinter.Button(self.menu_right,
		 text="Create Project",
		 command=self.create_new_project,
		 pady=20, bg=self.button_color,fg = self.fg_color, 
		highlightbackground="black",
		width = self.button_width)
		self.create_project.pack(pady=5)
		# load previous button
		self.load_previous = tkinter.Button(self.menu_right,
		 text="Load Project",
		 command=self.load_config,
		 pady=20, bg=self.button_color, fg = self.fg_color,
		highlightbackground="black",
		width = self.button_width)
		self.load_previous.pack(pady=5)
		# start experiment
		self.exp_button = tkinter.Button(self.menu_right,
		 text="Start Experiment",
		 command=self.start_experiment,
		 state=tkinter.DISABLED,
		 pady=20, bg=self.start_color, fg = self.fg_color, activebackground = "#00B306",
		highlightbackground="black",
		width = self.button_width)
		self.exp_button.pack(pady=5)
		# stop experiment
		self.exp_stop_button = tkinter.Button(self.menu_right,
		 text="Stop Experiment",
		 command=self.stop_experiment,
		 state=tkinter.DISABLED,
		 pady=20, bg=self.stop_color, fg = self.fg_color, activebackground='#E61523',
		highlightbackground="black",
		width = self.button_width)
		self.exp_stop_button.pack(pady=5)

		# Bottom area ----
		self.bottom_area = tkinter.Frame(self.window)
		self.bottom_text = tkinter.Label(self.bottom_area, text = "FEDWatcher v" + self.version + " is released under MIT license.", bg=self.bg_color, fg=self.fg_color)
		self.bottom_wiki = tkinter.Label(self.bottom_area, text="Check the Wiki", cursor="hand2")
		self.bottom_wiki.bind("<Button-1>", lambda e: open_url("https://github.com/matiasandina/FEDWatcher/wiki"))

		# on closing, ask before closing
		self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

		# Grid arrangements ####
		self.menu_top.grid(row=0, column=0, sticky="w", padx=self.left_pad)
		self.logo.pack(side="left")
		self.app_title.pack(side="left")
		self.menu_left.grid(row=1, column=0, sticky="nsew", padx=self.left_pad)
		# we want to use pack here
		self.menu_left_upper.pack(side="top", fill="both", expand=True)
		self.menu_left_title.grid(row=0,column=0)
		# if we use the grid method the menu_left_upper will get confined 
		#self.menu_left_upper.grid(row=1, column=0, sticky="nsew")
		self.menu_right.grid(row=1, column=1, sticky="nsew")
		# this gives priority to entry boxes
		# because of this, they will resize and fill space with the menu_left_upper
		self.menu_left_upper.grid_columnconfigure(1, weight=1)

		self.bottom_area.grid(row=2, column=0, sticky='w', padx=self.left_pad)
		self.bottom_text.pack()
		self.bottom_wiki.pack()

		self.uart_port_var = tkinter.StringVar()
		self.uart_port_var.set("UART2")  # default value
		self.checkbox_bg = "#424547"  # Dark grey background
		self.checkbox_fg = "#E1ECF2"  # Light grey foreground
		self.checkbox_select_color = "#333333"  # Darker grey for selected checkbox
		self.setup_uart_checkboxes()


	def get_mac(self):
		# This is good for Raspberry PIs, not good for other OS !
		# possible interfaces ['wlan0', 'eth0']
		#try:
		path_to_mac = '/sys/class/net/'+ 'wlan0' +'/address'
		mac = open(path_to_mac).readline()
		mac = mac.replace("\n", "")
		#except:
		#	try:
				# interface wlp2s0 for debugging outside of Pi
		#		mac=open('/sys/class/net/wlp2s0/address').readline()
		#	except:
		#		mac = "00:00:00:00:00:00"
		# mac = mac[0:17]
		return mac

	# button callbacks ------
	def create_new_project(self):
		self.all_set = self.check_input()
		if self.all_set:
			# choose directories first
			self.rootdir = tkinter.filedialog.askdirectory(title="Choose Project Directory", initialdir = os.path.expanduser('~'))
			self.exp_dir = os.path.join(self.rootdir, self.exp_entry.get())
			# create directory if needed
			if not os.path.isdir(self.exp_dir):
				print("Creating Experiment Directory within Project Directory")
				os.mkdir(self.exp_dir)
			# create the config
			self.create_config()
			self.exp_button.config(state="normal")
		return


	def load_config(self):
		# choose directories first
		self.exp_dir = tkinter.filedialog.askdirectory(title="Choose Previous Experiment Directory", initialdir = os.path.expanduser('~'))
		#self.expdir = os.path.join(self.rootdir, self.exp_entry.get())
		# check for previous configs
		files = os.listdir(self.exp_dir)
		# get config files in exp folder
		configs = [file for file in files if "config" in file]
		if len(configs) > 0:
			print("Adding new session to previous experiment")
			self.rootdir = os.path.dirname(self.exp_dir)
			# get the old experiment name from the folder structure
			exp_name = os.path.basename(self.exp_dir)
			self.exp_entry.delete(0, tkinter.END)
			self.exp_entry.insert(0, exp_name)
			# Create config
			self.create_config()
			# only now we enable the experiment button
			self.exp_button.config(state="normal")
			self.all_set = True 
		else:
			print("No previous configuration found. Create a new project")
			self.create_new_project()

	def setup_uart_checkboxes(self):
		self.uart_frame = tkinter.Frame(self.menu_left, bg=self.bg_color, highlightthickness=1, highlightbackground=self.fg_color)
		self.uart_frame.pack(fill="both", expand=True)

		# Convert all packing to grid within the frame.
		title_label = tkinter.Label(self.uart_frame, text="Select UART Ports:", fg=self.fg_color, bg=self.bg_color)
		title_label.grid(row=0, column=0, sticky='w')  # Start grid at row 0

		# Dictionary of UART ports and their descriptions
		# Extra spaces look messed up, but it actually aligns on tkinter grid !
		self.uart_ports = {
			"/dev/serial0": "UART0 -- GPIO 14 (TX) & 15 (RX)",
			"/dev/ttyAMA1": "UART1 -- GPIO 14 (TX) & 15 (RX)",
			"/dev/ttyAMA2": "UART2 -- GPIO   0 (TX) &   1 (RX)",
			"/dev/ttyAMA3": "UART3 -- GPIO   4 (TX) &   5 (RX)",
			"/dev/ttyAMA4": "UART4 -- GPIO   8 (TX) &   9 (RX)"
		}
		self.uart_port_vars = {}
		row_count = 1  # Start row_count at 1 to accommodate title

		# Checkbox for selecting all ports
		self.all_ports_var = tkinter.BooleanVar()
		all_ports_cb = tkinter.Checkbutton(self.uart_frame, text="All", variable=self.all_ports_var, command=self.select_all_ports,
											fg=self.fg_color, bg=self.bg_color, selectcolor=self.checkbox_select_color,
											activebackground=self.bg_color, activeforeground=self.fg_color,
											highlightthickness=0)
		all_ports_cb.grid(row=row_count, column=0, sticky='w')
		row_count += 1

		# Checkboxes for each UART port
		for port, description in self.uart_ports.items():
			var = tkinter.BooleanVar()
			# TODO:
			# for whatever reason there's a 3 white space alignment that I cannot resolve right now
			port_name = f"{port}   " if 'serial' in port else port
			cb = tkinter.Checkbutton(self.uart_frame, text=f"{port_name} -- {description}", variable=var,
										fg=self.fg_color, bg=self.bg_color, selectcolor=self.checkbox_select_color,
										activebackground=self.bg_color, activeforeground=self.fg_color,
										highlightthickness=0)
			cb.grid(row=row_count, column=0, sticky='w')
			self.uart_port_vars[port] = var
			row_count += 1

	def select_all_ports(self):
		# If "All" is selected, update all other checkboxes to match
		for var in self.uart_port_vars.values():
			var.set(self.all_ports_var.get())

	def start_experiment(self):
		self.exp_stop_button.config(state="normal") 
		# Gather the selected UART ports
		selected_ports = [port for port, var in self.uart_port_vars.items() if var.get()]
		if not selected_ports:
			# If no port is selected, maybe use a default or show a warning
			tkinter.messagebox.showinfo("Port Selection", "No UART port selected. Please select at least one.")
			return
		if self.all_set:
			# Start FEDWatcher ---
			print("FEDWatcher init...")
			self.fw = Fedwatcher()
			if len(self.email_entry.get()) > 0:
				email_ok = self.fw.register_email(email=self.email_entry.get(), password=self.password_entry.get())
				# run fedwatcher
				print("FEDWatcher will run with notifications to " + self.email_entry.get())
			if self.telegram_var.get():
				self.fw.tg_enabled = True
				tg_ok = self.fw.find_telegram_keys()
				print("FEDWatcher will run with notifications. Check your Telegram!")
			
			print("Starting FEDWatcher")
			self.fw.run(configpath=self.configpath)
		else:
			tkinter.messagebox.showinfo("Something went wrong",
			 "This will never happen (?)")


	def check_input(self):
		entry = self.exp_entry.get()
		if entry == "":
			tkinter.messagebox.showinfo("Invalid Entry", "Entry cannot be empty.")
			return False			
		accepted_patterns = re.compile(r'[a-zA-Z_0-9]')
		rejected = [char for char in entry if not accepted_patterns.match(char)]
		if len(rejected) > 0:
			tkinter.messagebox.showinfo("Invalid Entry", "Please only use alphanumeric characters in your experiment name. No spaces or symbols.")
			return False
		else:
			return True


	def create_config(self):
		# Get session number
		self.session_n = self.make_session_n()
		# make proper config name
		self.configpath = os.path.join(self.exp_dir, "config_" + self.session_n + ".ini")


		# Create config
		config = ConfigParser()
		config.read(self.configpath)
		config.add_section('fedwatcher')
		config.set('fedwatcher', 'exp_name', self.exp_entry.get())
		config.set('fedwatcher', 'root_dir', self.rootdir)
		config.set('fedwatcher', 'exp_dir', self.exp_dir)
		config.set('fedwatcher', 'session_num', self.session_n)
		config.set('fedwatcher', 'exp_start', datetime.datetime.now().replace(microsecond=0).isoformat())

		# TODO: add 
		# if check_input():
			# write
		# else:
			# throw error 
		with open(self.configpath, 'w') as f:
			config.write(f)
		return "Config was saved"

	def make_session_n(self):
		'''
		This function lists the configs in the directory and returns a proper session number as string
		This strig gets appended to the end of the config ini to denote sessions
		'''
		files = os.listdir(self.exp_dir)
		# get config files in exp folder
		configs = [file for file in files if "config" in file]
		# if there's no config (new project)
		if len(configs) < 1:
			new_session = "00"
		else:
			# looking for two digits here
			pattern = re.compile(r'\d{2}')
			# find the stuff
			number_match = [pattern.findall(x) for x in configs]
			# transform to integer and do the math
			session_int = [int(x[0]) for x in number_match if len(x) > 0]
			session_max = max(session_int)
			new_session = str(session_max + 1).zfill(2)
		return new_session

	def stop_experiment(self):
		# this stops fedwatcher but doesn't close ports
		self.fw.stop()
		config = ConfigParser()
		config.read(self.configpath)
		config.set('fedwatcher', 'exp_end', datetime.datetime.now().replace(microsecond=0).isoformat())
		with open(self.configpath, 'w') as f:
			config.write(f)
		print("Fedwatcher has been stopped!")
		return

	# # email info
	# def remember_info(self):
	# 	# toggle the other option
	# 	self.delete.set(value = 0)
	# 	return
	# def delete_info(self):
	# 	# toggle the other option
	# 	self.remember.set(value = 0)
	# 	return

	def on_closing(self):
		if tkMessageBox.askyesno("Quit", "Do you want to quit?"):
			# # kill the password saving
			# if self.remember.get() == 0:
			# 	print("Erasing email information")
			# 	self.fw.delete_email()
			# this first stops fedwatcher, fedwatcher will handle data saving
			if hasattr(self, 'fw') and self.fw.running:
				self.stop_experiment()
				time.sleep(0.5)
				self.fw.exit_gracefully()
			self.window.destroy()

def create_app(root):
	App(window = root, window_title = "FEDWatcher")

def open_url(url):
    webbrowser.open_new(url)


if __name__ == '__main__':
	# hard-coded current directory
	#os.chdir("/home/pi/homecage_quantification")
	# This only works on windows
	root = tkinter.Tk()
	#image = Image.open(os.path.join(os.getcwd(), 'img/64.png'))
	dir_path = os.path.dirname(os.path.realpath(__file__))
	image = Image.open(os.path.join(dir_path, 'img/64.png'))
	img = ImageTk.PhotoImage(image)
	root.tk.call('wm', 'iconphoto', root._w, img)
	#root.iconphoto(False,img)
	# widthxheight+300+300 pxposition from the leftcorner of the monitor
	root.geometry("800x550+300+300")
	# resize columns with window
	root.columnconfigure(0, weight=1, minsize=200)
	root.columnconfigure(1, weight=1, minsize=200)
	# set minimum height for row 0 and 2
	root.rowconfigure(0, minsize=80, weight=1)
	root.rowconfigure(1, minsize=300, weight=8)
	root.rowconfigure(2, minsize=70, weight=1)
	# set window min size
	root.minsize(520, 40)
	root.after(0, create_app, root)
	root.mainloop()
	

