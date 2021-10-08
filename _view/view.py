#encoding: utf-8
import os
from functools import partial

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfilenames

import json

import pandas as pd 
import numpy as np

import app_functions 		as AppFunctions
import _view.view_functions as 	ViewFunctions

from _view.view_theme		import View_Theme
from _view.view_history 	import View_History
from _view.view_explist 	import View_ExpList
from _view.view_expsettings import View_ExpSettings

class View:
	''' Window Struc '''
	def __init__(self,main_window):
		#Color adjustments
		self.c_windowbg 	= "#efefef"

		self.c_spacer		= "#097588"

		self.c_bheaderbg 	= "#e6e6e6"
		self.c_bheaderfg 	= "#5d7474"

		self.c_mainbg 				= "#f0f0f0"
		self.c_main_headerbg		= "#f8f8f8"
		self.c_main_headerfg		= "#373737"
		self.c_main_entrybg			= "#e9e9e9"
		self.c_main_shadow 			= ["#4a7f89","#086a7c"]
		self.c_main_analyserbg 		= "#097588" 
		self.c_main_analyserfg 		= "#fff" 
		self.c_main_analyserdtbg 	= "#518c97"

		self.c_historybg 	= "#e3e3e3"
		self.c_hist_shadow 	= ["#086a7c","#4a7f89","#c8c8c8"] #"Shadow" effect
		self.c_hist_titlebg	= self.c_spacer
		self.c_hist_titlefg	= "#b1d0d2"
		self.c_hist_spacer 	= "#518c97"
		self.c_hist_listfg 	= "#494949"
		self.c_hist_lspacer	= "#c8c8c8"
		self.c_hist_openbt 	= "#097588"
		self.c_hist_closebt = "#d23964"



		self.window = main_window
		
		self.set_theme()

		self.set_window()

		self.get_window_property()
		self.set_min_sizes()

		self.set_widgets()

		self.set_main()
		self.set_run_button()


	def set_theme(self):
		View_Theme(self).set_View()

	def set_window(self):
		self.window.title("Ichthus")
		self.window.iconphoto(True, tk.PhotoImage(file="imgs/icon2.png"))
		self.window.iconify()
		self.window.deiconify()
		self.window.state("zoomed")

		self.window["bg"]	= self.c_windowbg

		self.window.grid_columnconfigure(1,weight=1)

		self.window.grid_rowconfigure(4,minsize=400,weight=1)


	def get_window_property(self):
		self.window.update()
		self.window_sizes = {'width':self.window.winfo_width()}
		print(self.window_sizes)

	def set_min_sizes(self):
		#Window min_size
		self.window.minsize(int(self.window_sizes['width']/1.4),563)
		#Main column min_size
		self.window.grid_columnconfigure(1,minsize=(self.window_sizes['width']/2))

	def set_widgets(self):
		''' Set the basic structure of widgets '''
		self.set_header()
		self.set_body()
		self.set_history()


	def set_header(self):
		#Container
		self.header		= tk.Frame(self.window)
		self.header.grid(column=1,row=2,padx=15,sticky="nsew") 

		self.iimg_logo 	= tk.PhotoImage(file="imgs/ichtus_logo_small.png")
		self.img_logo 	= tk.Label(self.header,bg=self.c_windowbg,bd=0,image=self.iimg_logo).grid(column=1,row=1,sticky="w")
		
		#(Text,Command) - To implement
		#self.buttons = [("File",partial(ViewFunctions.init_presets,self)),("")]
		
		#Buttons
		self.b_file		= tk.Button(self.header,bg=self.c_bheaderbg,fg=self.c_bheaderfg,bd=0,text="File")
		#self.b_file.grid(column=2,row=1,sticky="w",pady=10,padx=(15,0),ipadx=5)
		self.b_presets	= tk.Button(self.header,bg=self.c_bheaderbg,fg=self.c_bheaderfg,bd=0,text="Presets",command=partial(ViewFunctions.init_presets,self))
		#self.b_presets.grid(column=3,row=1,sticky="w",pady=10,padx=(15,0),ipadx=5)
		self.b_about	= tk.Button(self.header,bg=self.c_bheaderbg,fg=self.c_bheaderfg,bd=0,text="About",command=partial(ViewFunctions.init_about,self))
		self.b_about.grid(column=4,row=1,sticky="w",pady=10,padx=(15,0),ipadx=5)

		#Spacers
		#(Top)
		tk.Frame(self.window,bg=self.c_spacer,height=2).grid(column=1,row=1,sticky="nsew")

		#(Bottom)
		tk.Frame(self.window,bg=self.c_spacer,height=1).grid(column=1,row=3,pady=2,padx=(5,6),sticky="nsew")

	#To implement
	def _set_header_buttons(self):
		pass

	def set_body(self):
		self.body 		= tk.Frame(self.window,bg=self.c_mainbg, highlightthickness=1,highlightbackground="#ddd",highlightcolor="#ddd")
		self.body.grid(column=1,row=4,padx=(5,6),pady=5,sticky="nsew")

		self.body.grid_columnconfigure(1,weight=2,minsize=700)
		self.body.grid_rowconfigure(3,weight=1) #Main body responsive

	def set_history(self):
		''' Set the 'history' object and pass self object '''
		self.jobs_obj 	= View_History(self)

	def set_main(self):
		''' Set the 'main' object and '''
		self.main_obj 	= View_MainManager(self)


	def set_run_button(self):
		''' Grid the 'Run experiment' button '''

		self.buttonbd 			= tk.Frame(self.window,highlightthickness=1,highlightbackground=self.runbtbd,highlightcolor=self.runbtbd)
		self.buttonbd.grid(column=1,row=5,sticky="ne",padx=10,pady=(5,10))

		self.irun_button 		= tk.PhotoImage(file="imgs/run_icon.png")

		if self.window_sizes['width'] < 1600:
			self.irun_button 		= tk.PhotoImage(file="imgs/run_icon_min.png")

		self.run_button 		= tk.Button(self.buttonbd,text=" Run ",font=("Arial",15),compound="left",image=self.irun_button,bd=0,bg=self.runbtbg,activebackground=self.runbtbg,fg=self.runbtfg,activeforeground=self.runbtfg,command=lambda : ViewFunctions.start_analysis(self))
		self.run_button.image 	= self.irun_button
		self.run_button.grid(ipadx=2,ipady=1)

	def get_values(self):
		return self.main_obj.get_values()



class View_Main():
	def __init__(self,view_object):
		self.view 			= view_object

		self.mainbg 		= view_object.c_mainbg

		self.headerbg 		= view_object.c_main_headerbg
		self.headerfg 		= view_object.c_main_headerfg
		self.entrybg 		= view_object.c_main_entrybg

		self.header_shadowbg= view_object.c_main_shadow

		self.analyserbg 	= view_object.c_main_analyserbg
		self.analyserfg 	= view_object.c_main_analyserfg
		self.analyser_dtbg 	= view_object.c_main_analyserdtbg #Analyser detail

	def create_main(self):
		self.set_container()
		self.set_header()
		self.set_body()
		self._set_default_values()


	def set_container(self):
		self.container = tk.Frame(self.view.body)
		self.container.grid(column=1,row=1,sticky="nsew")
		self.container.grid_columnconfigure(1,weight=1)


	def set_header(self):
		self.header 		= tk.Frame(self.container,bg=self.headerbg)
		self.header.grid(column=1,row=1,sticky="nsew")

		self.header.grid_columnconfigure(2,weight=1)

		self.name_label 	= tk.Label(self.header,bg=self.headerbg,fg=self.headerfg,text="Title:",font=("Arial",14))
		self.name_label.grid(column=1,row=1,pady=20,padx=15)

		self.name_entry 	= tk.Entry(self.header,bg=self.entrybg,fg=self.headerfg,font=("Arial",13),bd=0,highlightthickness=4,highlightbackground=self.entrybg,highlightcolor=self.entrybg)
		#self.name_entry['width'] = 27
		self.name_entry.grid(column=2,row=1,sticky="ew")

		self.author_label 	= tk.Label(self.header,bg=self.headerbg,fg=self.headerfg,text="Author:",font=("Arial",14))
		self.author_label.grid(column=3,row=1,padx=(30,15),sticky="ew")

		self.author_entry 	= tk.Entry(self.header,width=15,bg=self.entrybg,fg=self.headerfg,font=("Arial",13),bd=0, highlightthickness=4,highlightcolor=self.entrybg,highlightbackground=self.entrybg)
		self.author_entry.grid(column=4,row=1,padx=(0,20),sticky="ew")

		#Shadow effect
		self.header_sw_cont = tk.Frame(self.container)
		self.header_sw_cont.grid(column=1,row=2,sticky="nsew")
		self.header_sw_cont.grid_columnconfigure(2,weight=1)

		self.header_shadow1 = tk.Frame(self.header_sw_cont,bg=self.header_shadowbg[0],height=3,width=6)
		self.header_shadow1.grid(column=1,row=1,sticky="nsew")

		self.header_shadow2 = tk.Frame(self.header_sw_cont,bg=self.header_shadowbg[1],height=3)
		self.header_shadow2.grid(column=2,row=1,sticky="nsew")


	def set_body(self):
		self.body_container = tk.Frame(self.container)
		self.body_container.grid(column=1,row=2,sticky="nsew")
		self.body_container.grid_columnconfigure(1,weight=1)

		self.set_analyser_options()
		self.set_exp_settings()


	def set_analyser_options(self):
		''' Set data algorithm option select '''

		self.analyser_cont 	= tk.Frame(self.body_container,bg=self.analyserbg)
		self.analyser_cont.grid(column=1,row=3,sticky="nsew")

		self.analyser_detail= tk.Frame(self.analyser_cont,bg=self.analyser_dtbg,width=6).grid(column=1,row=1,sticky="ns")
		self.analyser_label = tk.Label(self.analyser_cont,bg=self.analyserbg,fg=self.analyserfg,text="Data process algorithm:",font=("Arial",14)).grid(column=2,row=1,pady=(8,9),padx=(8,5),sticky="e")

		self.analyser_opt 	= tk.StringVar()
		
		self.s_analyser_rb 	= ttk.Style()
		self.s_analyser_rb.configure('Rbg.TRadiobutton',background=self.analyserbg,foreground=self.analyserfg,font=("Arial",13))
		
		self.analyser_rb1 	= ttk.Radiobutton(self.analyser_cont, text="MzMine",style='Rbg.TRadiobutton', variable=self.analyser_opt, value="MzMine", command=lambda:(self.th_param_rb2.configure(state="disabled"), self.th_param_rb1.invoke()))
		self.analyser_rb1.grid(column=3,row=1,sticky="e",padx=7)

		self.analyser_rb2 	= ttk.Radiobutton(self.analyser_cont, text="Find Molecular Features",style='Rbg.TRadiobutton', variable=self.analyser_opt, value="FindMolFeat", command=lambda:(self.th_param_rb2.configure(state="enabled"), self.th_param_rb2.invoke()))
		self.analyser_rb2.grid(column=4,row=1,sticky="e",padx=7)

		self.separator 		= tk.Frame(self.analyser_cont,width=1,bg=self.analyser_dtbg).grid(column=5,row=1,sticky="ns",padx=(3,1),pady=8)

		self.threshold_param 		= tk.StringVar()

		self.threshold_label= tk.Label(self.analyser_cont,bg=self.analyserbg,fg=self.analyserfg,text="Threshold parameter:",font=("Arial",14)).grid(column=6,row=1,pady=(8,9),padx=(8,5),sticky="e")

		self.th_param_rb1 	= ttk.Radiobutton(self.analyser_cont, text="Intensity",style='Rbg.TRadiobutton', variable=self.threshold_param, value="Intensity")
		self.th_param_rb1.grid(column=7,row=1,sticky="e",padx=7)

		self.th_param_rb2 	= ttk.Radiobutton(self.analyser_cont, text="S/N",style='Rbg.TRadiobutton', variable=self.threshold_param, value="S/N")
		self.th_param_rb2.grid(column=8,row=1,sticky="e",padx=7)

	def set_exp_settings(self):
		#Container of both active and inactive settings (and list)
		self.settings_cont 	= tk.Frame(self.body_container)
		self.settings_cont.grid(column=1,row=5,sticky='nsew')
		self.settings_cont.grid_columnconfigure(1,weight=1) #Fill horizontally

		#Experiment settings object
		self.exp_settings 	= View_ExpSettings(self.settings_cont,self.view.window_sizes)

	def _set_default_values(self):
		self.presets = AppFunctions.Presets()
		self.presets = self.presets.get()

		if self.presets['analyser_opt']		 == 'FindMolFeat':
			self.analyser_rb2.invoke()
		elif self.presets['analyser_opt']	 == 'MzMine':
			self.analyser_rb1.invoke()

		if self.presets['threshold_param'] == 'Intensity':
			self.th_param_rb1.invoke()
		elif self.presets['threshold_param'] == 'S/N':
			self.th_param_rb2.invoke()

	def get_values(self):
		''' description '''

		self.data = {
			'name':self.name_entry.get(),
			'author':self.author_entry.get(),
			'analyser_opt':self.analyser_opt.get(),
			'threshold_param':self.threshold_param.get()
			}

		#Get experiments settings and filepaths list
		self.data.update(self.exp_settings.get_values())

		return self.data



class View_MainManager(View_Main):
	def __init__(self,view_object):
		super().__init__(view_object)
		self.page_open = None
		self.set_page("Main")


	def set_page(self,id_page):
		if id_page == "Main" and not self.page_open == "Main":
			#self.close_page(self.page_open)

			super().create_main()

			self.page_open = "Main"
		
		else:
			pass

window			= tk.Tk()
viewApp			= View(window)
window.mainloop()