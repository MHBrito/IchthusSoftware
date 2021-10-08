import tkinter as tk
import _view.view_functions as ViewFunctions

from _view.view_theme import View_Theme
from functools import partial

class View_ExpList():
	def __init__(self,body_container):
		#Color Scheme
		self.set_theme()

		#Experiment body container
		self.body_container 	= body_container 

		self.selected_files 	= []

		#Widget container
		self.set_container() 
		self.set_list_container()
		self.set_list()

	def set_theme(self):
		View_Theme(self).set_expList()

	def set_container(self):
		''' Grid the external container of the list '''
		self.ext_container = tk.Frame(self.body_container,bg=self.bg_color,highlightthickness=1,highlightbackground="#ddd",highlightcolor="#ddd")
		self.ext_container.grid(column=2,row=1,padx=(0,13),pady=6,sticky="nsew")
		self.ext_container.grid_columnconfigure(1,weight=1)
		self.ext_container.grid_rowconfigure(1,weight=1)

	def set_list_container(self):
		''' Grid the internal container of the list '''
		#List container - To be able to clear the list
		self.list_container 	= tk.Frame(self.ext_container,bg=self.bg_color)
		self.list_container.grid(column=1,row=1,sticky="nsew",padx=5,pady=2)
		self.list_container.grid_columnconfigure(1,weight=1) #Fill horizontally

		#Row 99 - To "Empty list" container fill vertically
		self.list_container.grid_rowconfigure(99,weight=1)

	def set_list(self):
		''' Grid the list with the paths or the empty list button '''
		if len(self.selected_files) > 0:
			self.clear_list()
			self.grid_list()
		else:
			self.clear_list()
			self.grid_empty_list()			


	def clear_list(self):
		''' Resets list container '''
		self.list_container.destroy()
		self.set_list_container()


	def grid_empty_list(self):
		''' Grid 'Empty list' button '''
		self.empty_button	 	= tk.Button(self.list_container,text=("Empty list. Please click to select files."),font=("Arial",13),command=lambda : self.add_elements(),bd=0,bg=self.empty_btbg,activebackground=self.empty_btbg,fg=self.empty_btfg,activeforeground=self.empty_btfg)
		self.empty_button.grid(column=1,row=99,ipadx=10,ipady=4)


	def add_elements(self):
		''' Adds an element to the list of selected files '''
		a = ViewFunctions.open_files()
		if a:
			if len(a) + len(self.selected_files) <= 5:
				self.selected_files = self.selected_files + list(a)
				self.set_list()
			else:
				ViewFunctions.show_message("The number of files exceeds the limit (5).")


	def del_element(self,index):
		''' Delete a list element '''
		del self.selected_files[index]
		self.set_list()


	def grid_list(self):
		''' Grid list with selected files '''

		for i,path in enumerate(self.selected_files):
			element_cont = tk.Frame(self.list_container,bg=self.listbg,height=20)
			element_cont.grid(column=1,row=i+1,pady=2,sticky="ew")
			element_cont.grid_columnconfigure(2,weight=1)

			element_dt 	 = tk.Frame(element_cont,height=38,width=5,bg=self.listdtbg)
			element_dt.grid(column=1,row=1)

			element_text = tk.Label(element_cont,text=f"{path}",fg=self.listfg,bg=self.listbg,font=("Arial",12),anchor="e")
			element_text.grid(column=2,row=1,padx=5,sticky="w")

			ielement_del = tk.PhotoImage(file="imgs/list_close.png")
			element_del  = tk.Button(element_cont,image=ielement_del,bd=0,bg=self.listdelbg,command=partial(self.del_element,i))
			element_del.grid(column=3,row=1,padx=4,pady=3,ipadx=8,ipady=0,sticky="ns")
			element_del.image = ielement_del


	def get_values(self):
		''' Returns paths of selected files '''
		return self.selected_files
