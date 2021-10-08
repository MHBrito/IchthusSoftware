import tkinter as tk
from _view.view_theme import View_Theme



class PresetsView:
	def __init__(self,main_object):
		self.main 	= main_object 

		self._set_theme()
		self._set_toplevel_object()
		self._set_container()
		self._set_options()


	def _set_theme(self):
		View_Theme(self).set_presetsView()

	def _set_toplevel_object(self):
		self.window 	= tk.Toplevel(self.main.window,bg=self.bg_color)
		self.window.title("Ichthus presets")
		self.window.resizable(False,False)
	
	def _set_container(self):
		self.container = tk.Frame(self.window,bg=self.bg_color)
		self.container.grid(column=1,row=1,sticky="nsew")

	def _set_options(self):
		self._set_th_options()

	def _set_th_options(self):

		self.th_opt_cont 	= tk.Frame(self.container)
		self.th_opt_cont.grid(column=1,row=1,sticky="nsew")
		self.create_exp_lb("Active threshold",self.container,1,"title")
		self.create_exp_lb("Value",self.container,2,"subtitle")
		self.create_exp_lb("Type",self.container,3,"subtitle")

	def create_exp_lb(self,text,container,row,option_type):
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
		
		label 		= tk.Label(label_cont,fg=self.labelfg,text=f"{text}:",font=("Arial",13)).grid(column=2,row=1,sticky="w",pady=(3,0))

