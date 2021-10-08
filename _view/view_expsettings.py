import tkinter as tk
import tkinter.ttk as ttk

import app_functions 		as AppFunctions

from _view.view_theme 		import View_Theme
from _view.view_explist 	import View_ExpList 

class View_ExpSettings():
	def __init__(self,container,window_sizes):
		#Experiments (Both active and inactive) container
		self.container = container
		#App window sizes
		self.window_sizes = window_sizes
		
		self._set_theme()

		self._set_exp_settings()

		self._set_default_values()

	def _set_theme(self):
		View_Theme(self).set_expSettings()

	def _set_exp_settings(self):
		'''  '''
		#Store Tk structure of settings...
		self.exp_settings 	= {'active':{},'inactive':{}}

		for i,_type in enumerate(self.exp_settings): 
			#set '_type' Tk structures
			self.exp_settings[_type]['cont'] = tk.Frame(self.container)
			self.exp_settings[_type]['cont'].grid(column=1,row=i,sticky='nsew')
			self.exp_settings[_type]['cont'].grid_columnconfigure(1,weight=1)


			#Header of experiment '_type' area
			self.exp_settings[_type]['header_cont'] = tk.Frame(self.exp_settings[_type]['cont'],bg=self.headerbg)
			self.exp_settings[_type]['header_cont'].grid(column=1,row=1,sticky="nsew")

			#Label and detail
			self.exp_settings[_type]['header_dt'] 	= tk.Frame(self.exp_settings[_type]['header_cont'],bg=self.headerdtbg,width=8).grid(row=1,column=1,sticky="ns",pady=9)


			if _type == "inactive":
				self.exp_label = f"{_type} (Control)"
			else:
				self.exp_label = _type

			self.exp_settings[_type]['header_label']= tk.Label(self.exp_settings[_type]['header_cont'],bg=self.headerbg,fg=self.headerfg,text=f"{_type} experiment settings:",font=('Arial',15)).grid(column=2,row=1,sticky="e",padx=6,pady=(12,8))


			#Body of experiment '_type' area
			self.exp_settings[_type]['body_cont'] 	= tk.Frame(self.exp_settings[_type]['cont'])
			self.exp_settings[_type]['body_cont'].grid(column=1,row=2,sticky="nsew")
			self.exp_settings[_type]['body_cont'].grid_columnconfigure(2,weight=1,minsize=(self.window_sizes['width']/6))
			self.exp_settings[_type]['body_cont'].grid_columnconfigure(2,minsize=(self.window_sizes['width']/6))


			#Settings container
			self.exp_settings[_type]['set_cont'] 	= tk.Frame(self.exp_settings[_type]['body_cont'])
			self.exp_settings[_type]['set_cont'].grid(column=1,row=1,sticky="nsew",padx=13,pady=12)


			#Threshold options and value container
			self.exp_settings[_type]['th_cont']		= tk.Frame(self.exp_settings[_type]['set_cont'])
			self.exp_settings[_type]['th_cont'].grid(column=1,row=1,padx=5)

			#Threshold Label
			self.create_exp_lb(self.exp_settings[_type]['th_cont'],1,'title','Threshold')

			#Value Label and entry
			self.create_exp_lb(self.exp_settings[_type]['th_cont'],2,'subtitle','Value')
			self.exp_settings[_type]['th_value'] 	= tk.Entry(self.exp_settings[_type]['th_cont'],width=8,font=("Arial",12),justify="right",bd=0,bg=self.entrybg,highlightthickness=3,highlightbackground=self.entrybg,highlightcolor=self.entrybg)
			self.exp_settings[_type]['th_value'].grid(column=2,row=2,padx=(30,10))

			#Type
			self.create_exp_lb(self.exp_settings[_type]['th_cont'],3,'subtitle','Type')
			self.exp_settings[_type]['th_opt'] 		= tk.StringVar()
			
			#To implement - A function to create tk.Rbutton
			self.s_thRb 	= ttk.Style()
			self.s_thRb.configure('Th.TRadiobutton',background=self.rbuttonbg,foreground=self.labelfg,font=("Arial",13))

			self.exp_settings[_type]['th_rel'] 		= ttk.Radiobutton(self.exp_settings[_type]['th_cont'], text="Relative",style='Th.TRadiobutton', variable=self.exp_settings[_type]['th_opt'], value="relative")
			self.exp_settings[_type]['th_rel'].grid(column=2,row=4,sticky="w",padx=(28,10),pady=(0,4))

			self.exp_settings[_type]['th_abs'] 		= ttk.Radiobutton(self.exp_settings[_type]['th_cont'], text="Absolute",style='Th.TRadiobutton', variable=self.exp_settings[_type]['th_opt'], value="absolute")
			self.exp_settings[_type]['th_abs'].grid(column=2,row=5,sticky="w",padx=(28,10),pady=(0,4))


			#Mz and Rt options container
			self.exp_settings[_type]['mzRt_cont']	= tk.Frame(self.exp_settings[_type]['set_cont'])
			self.exp_settings[_type]['mzRt_cont'].grid(column=2,row=1,padx=10,sticky="nsew")

			self.create_exp_lb(self.exp_settings[_type]['mzRt_cont'],1,'title','Mz Tolerance')
			self.exp_settings[_type]['mz_tol']		= tk.Entry(self.exp_settings[_type]['mzRt_cont'],width=8,font=("Arial",12),justify="right",bd=0,bg=self.entrybg,highlightthickness=3,highlightbackground=self.entrybg,highlightcolor=self.entrybg)
			self.exp_settings[_type]['mz_tol'].grid(column=2,row=1,padx=(28,10))

			self.create_exp_lb(self.exp_settings[_type]['mzRt_cont'],2,'title','Rt Tolerance')
			self.exp_settings[_type]['rt_tol']		= tk.Entry(self.exp_settings[_type]['mzRt_cont'],width=8,font=("Arial",12),justify="right",bd=0,bg=self.entrybg,highlightthickness=3,highlightbackground=self.entrybg,highlightcolor=self.entrybg)
			self.exp_settings[_type]['rt_tol'].grid(column=2,row=2,padx=(28,10))


			#Store list object
			self.exp_settings[_type]['list'] = View_ExpList(self.exp_settings[_type]['body_cont'])


	def create_exp_lb(self,container,row,option_type,value):
		''' Create the labels for the configuration options '''

		if option_type 	== "title":
			detail_color 		= self.labeldtbg2 #Dark green	
			detail_margin		= (0,3)

		elif option_type == "subtitle":
			detail_color 		= self.labeldtbg1 #Ligth green
			detail_margin		= (5,3)

		label_cont 	= tk.Frame(container)
		label_cont.grid(column=1,row=row,sticky="w")

		label_detail= tk.Frame(label_cont,bg=detail_color,width=8).grid(column=1,row=1,sticky="ns",pady=(7,3),padx=detail_margin)
		
		label 		= tk.Label(label_cont,fg=self.labelfg,text=f"{value}:",font=("Arial",13)).grid(column=2,row=1,sticky="w",pady=(3,0))

	def _set_default_values(self):
		self.presets = AppFunctions.Presets()
		self.presets = self.presets.get()

		for _type,th_opt in self.presets['threshold_opt'].items():
			if th_opt == 'relative':
				self.exp_settings[_type]['th_rel'].invoke()
			elif th_opt == 'absolute':
				self.exp_settings[_type]['th_abs'].invoke()	

		for _type,th_value in self.presets['threshold_value'].items():
			self.exp_settings[_type]['th_value'].insert(0,th_value)

		for _type,mz_tol in self.presets['mz_tolerance'].items():
			self.exp_settings[_type]['mz_tol'].insert(0,mz_tol)

		for _type,rt_tol in self.presets['rt_tolerance'].items():
			self.exp_settings[_type]['rt_tol'].insert(0,rt_tol)

	def get_values(self):
		''' description '''

		self.data = {'mz_tol':{},'rt_tol':{},'th_opt':{},'th_value':{},'file_paths':{}}

		for _type in self.exp_settings:
			self.data['mz_tol'][_type]		 = self.exp_settings[_type]['mz_tol'].get()
			self.data['rt_tol'][_type]		 = self.exp_settings[_type]['rt_tol'].get()
			self.data['th_opt'][_type]		 = self.exp_settings[_type]['th_opt'].get()
			self.data['th_value'][_type]	 = self.exp_settings[_type]['th_value'].get()
			self.data['file_paths'][_type] 	 = self.exp_settings[_type]['list'].get_values()

		return self.data

