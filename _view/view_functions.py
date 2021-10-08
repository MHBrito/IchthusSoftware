import viewer
import _view.about 
import _view.presets

import app_functions as AppFunctions

import tkinter as tk

import threading

import concurrent.futures

import time


def init_viewer(self,data_id):
	self.window.iconify()
	viewer.create_viewer(data_id)

def init_about(self):
	_view.about.AboutView(self)

def init_presets(self):
	_view.presets.PresetsView(self)
	
def start_analysis(self):
	''' Initiate analysis '''
	def analysis_thread(self):
		data 				= self.get_values()
		analysis 			= AppFunctions.Analysis(data)
		analysis_result 	= analysis.init_analysis()

		if analysis_result == True:
			self.jobs_obj.refresh_list()
	#analysis_thread(self)
	
	executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
	future = executor.submit(analysis_thread,self)
	

def open_files():
	a = tk.filedialog.askopenfilenames()
	if a == '':
		a = False
	return a

def show_message(message,title="Messages:"):
	m = threading.Thread(target=tk.messagebox.showinfo,args=(title,message))
	m.start()

def show_error(message,title="Error:"):
	r = threading.Thread(target=tk.messagebox.showerror,args=(title,message))
	r.start()

def get_confirmation(message,title="Warning:"):
	return tk.messagebox.askokcancel(title,message)
