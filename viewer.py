import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont
from tkinter import messagebox

import os
import json

import app_functions as AppFunctions
import pandas as pd 
import numpy as np

import matplotlib.pyplot as plt

import plotly.offline as py
import plotly.graph_objs as go
from mpl_toolkits.mplot3d import axes3d

class Viewer(object):
	def __init__(self,viewer_window,data_id):
		#General adjustments
		self.color2 = "#d1dede"
		self.color_wbg = "#efefef"

		self.window = viewer_window

		#Set the id for history search file
		self.data_id = data_id

		#Get data and metadata of history archive
		self.get_metadata()
		self.get_data()

		#Setup viewer window
		self.set_window()


		#print(f"self.window :{self.window.winfo_width()}")

		self.main_cont = tk.Frame(self.window,bg ="#fff")
		self.main_cont.grid(column=1,row=1,sticky="nsew")
		self.main_cont.grid_columnconfigure(1,weight=1)
		self.main_cont.grid_rowconfigure(2,weight=1)

		self._set_header()

		self.spreadsheet_header = []
		for index,column in enumerate(self.analysis_file['result']):
			self.spreadsheet_header.append(column)

		self.spreadsheet_data = []		
		for index, row in self.analysis_dataframe.iterrows():
			self.spreadsheet_data.append(tuple(row[i] for i in self.analysis_dataframe.columns))

		# the test data ...
		listbox = self.multiColumn_listbox(self.main_cont,self.meta_file,self.analysis_dataframe)


	def get_metadata(self):
		if os.path.isfile("hist/meta.json"):
			visual_file		= open("hist/meta.json")
			meta_file		= json.load(visual_file)
			visual_file.close()
		
		#Pega o índice das informações "meta" do experimento no arquivo meta.json
		for i,x in enumerate(meta_file['metadata_list']):
			if x["data_id"] == self.data_id:
				index = i
		self.meta_file = meta_file['metadata_list'][index]


	def get_data(self):
		if os.path.isfile(f"hist/data/{self.data_id}.json"):
			visual_file		= open(f"hist/data/{self.data_id}.json")
			self.analysis_file 	= json.load(visual_file)
			visual_file.close()

		self.analysis_dataframe = pd.DataFrame(self.analysis_file['result'])


	def set_window(self):
		self.window.state("zoomed")
		self.window.title(f"Viewer: {self.meta_file['name']}")
		self.window["bg"]	= self.color_wbg

		#Grid config
		self.window.grid_columnconfigure(1,weight=1)
		self.window.grid_rowconfigure(1,weight=1)
		self.window.update()


	def _set_header(self):
		''' Sets the window header '''
		header 	= tk.Frame(self.main_cont,bg="#fefefe")
		header.grid(column=1,row=1,padx=5,sticky="nsew")
		header.grid_columnconfigure(1,weight=1)

		title 	= tk.Label(header,bg="#fefefe",justify="left",text=f"#Job: {self.meta_file['name']}",font=("Arial",14))
		title.grid(column=1,row=1,sticky="w",pady=(15,0)) 
		info_cont 	= tk.Frame(header,bg="#fff")
		info_cont.grid(column=1,row=2,sticky="nsew",pady=5)
		self.found_ions 		= tk.Label(info_cont,bg="#fff",justify="left",text=f"Found ions: {self.analysis_dataframe.shape[0]}")
		self.found_ions.grid(column=1,row=1,sticky="w")

		self.separator1 	= tk.Frame(info_cont,bg="#ccc",width=1).grid(column=2,row=1,padx=20,pady=2,sticky="ns")

		self.max_ar 		= tk.Label(info_cont,bg="#fefefe",justify="left",text=f"Maximum affinity ratio: {self.analysis_dataframe['Affinity Ratio'].max()}")
		self.max_ar.grid(column=3,row=1,sticky="w")
		
		self.separator2 	= tk.Frame(info_cont,bg="#ccc",width=1).grid(column=4,row=1,padx=20,pady=2,sticky="ns")

		self.min_ar 		= tk.Label(info_cont,bg="#fefefe",justify="left",text=f"Minimum affinity ratio: {self.analysis_dataframe['Affinity Ratio'].min()}")
		self.min_ar.grid(column=5,row=1,sticky="w")


		self.graph3d_button 	= tk.Button(header,fg="#2b3939",bd=0,text="3dGraph [AR x RT x M/z]",command=lambda : self._show_graph_3d("Retention Time","m/z","Affinity Ratio",self.analysis_dataframe['A(RT)'],self.analysis_dataframe['m/z'],self.analysis_dataframe['Affinity Ratio'])).grid(column=2,row=1,rowspan=2,ipadx=35,padx=5,pady=10,sticky="nsew")

		self.separator3 		= tk.Frame(header,bg="#ccc",width=1).grid(column=3,row=1,rowspan=2,padx=20,pady=8,sticky="ns")

		self.graph2d_armz_btn 	= tk.Button(header,fg="#2b3939",bd=0,text="2dGraph [AR x RT]",command=lambda : self._show_graph_2d("Retention Time","Affinity Ratio",self.analysis_dataframe['A(RT)'],self.analysis_dataframe['Affinity Ratio'])).grid(column=4,row=1,rowspan=2,ipadx=35,padx=5,pady=10,sticky="nsew")
		self.graph2d_arrt_btn 	= tk.Button(header,fg="#2b3939",bd=0,text="2dGraph [AR x M/z]",command=lambda : self._show_graph_2d("m/z","Affinity Ratio",self.analysis_dataframe['m/z'],self.analysis_dataframe['Affinity Ratio'])).grid(column=5,row=1,rowspan=2,ipadx=35,padx=5,pady=10,sticky="nsew")

		self.separator4 		= tk.Frame(header,bg="#ccc",width=1).grid(column=6,row=1,rowspan=2,padx=20,pady=8,sticky="ns")

		self.export_button 		= tk.Button(header,bg="#097588",fg="#fff",bd=0,text="Export result",command=lambda : self._export_data()).grid(column=7,row=1,rowspan=2,ipadx=35,padx=5,pady=10,sticky="nsew")

	def _export_data(self):
		self.export_filepath 	= tk.filedialog.asksaveasfilename(confirmoverwrite=True,defaultextension='.xlsx', \
			filetypes=[('Excel','.xlsx')])

		AppFunctions.save_dataframe("excel",self.export_filepath,self.analysis_dataframe,self.meta_file['name'])

	def _show_graph_2d(self,xlabel,ylabel,axisx,axisy):	
		plt.scatter(axisx,axisy)
		plt.ylabel(ylabel)
		plt.xlabel(xlabel)
		plt.show()

	def _show_graph_3d(self,xlabel,ylabel,zlabel,axisx,axisy,axisz):
		fig 		= plt.figure()
		ax 			= fig.add_subplot(projection='3d')

		xs = axisx
		ys = axisy
		zs = axisz

		ax.scatter(xs, ys, zs)
		ax.set_xlabel(xlabel)
		ax.set_ylabel(ylabel)
		ax.set_zlabel(zlabel)	

		plt.show()

	def multiColumn_listbox(self,container,meta_file,analysis_dataframe):
		"""use a ttk.TreeView as a multicolumn ListBox"""
		self.tree 					= None
		self.main_cont 				= container
		self.meta_file 				= meta_file
		self.analysis_dataframe 	= analysis_dataframe
		self._setup_widgets()
		self._build_tree()


	def _setup_widgets(self):
		'''
			Setup TreeView Container
		'''
		self.tree_cont = ttk.Frame(self.main_cont)
		self.tree_cont.grid(column=1,row=2,sticky="nsew")

		# create a treeview with dual scrollbars
		self.tree = ttk.Treeview(self.tree_cont,columns=self.spreadsheet_header, show="headings")

		#Scrollbars Setting
		vsb = ttk.Scrollbar(self.tree_cont,orient="vertical", command=self.tree.yview)
		hsb = ttk.Scrollbar(self.tree_cont,orient="horizontal", command=self.tree.xview)
		self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
		#Grid everything
		self.tree.grid(column=0, row=0, sticky='nsew', in_=self.tree_cont)
		vsb.grid(column=1, row=0, sticky='ns', in_=self.tree_cont)
		hsb.grid(column=0, row=1, sticky='ew', in_=self.tree_cont)
		self.tree_cont.grid_columnconfigure(0, weight=1)
		self.tree_cont.grid_rowconfigure(0, weight=1)

	def _build_tree(self):
		for col in self.spreadsheet_header:
			#col.title() its bad because of the m/z.
			self.tree.heading(col, text=col,
				command=lambda c=col: sortby(self.tree, c, 0))
			# adjust the column's width to the header string
			self.tree.column(col,
				width=tkFont.Font().measure(col.title()))

		for item in self.spreadsheet_data:
			self.tree.insert('', 'end', values=item)
			# adjust column's width if necessary to fit each value
			for ix, val in enumerate(item):
				col_w = tkFont.Font().measure(val)
				if self.tree.column(self.spreadsheet_header[ix],width=None)<col_w:
					self.tree.column(self.spreadsheet_header[ix], width=col_w)


def sortby(tree, col, descending):
	"""sort tree contents when a column header is clicked on"""
	# grab values to sort
	data = [(tree.set(child, col), child) \
		for child in tree.get_children('')]
	# if the data to be sorted is numeric change to float
	#data =  change_numeric(data)
	# now sort the data in place
	
	data = [tuple([float(i[0]),i[1]]) for i in data]
	data.sort(reverse=descending)
	for ix, item in enumerate(data):
		tree.move(item[1], '', ix)
	# switch the heading so it will sort in the opposite direction
	tree.heading(col, command=lambda col=col: sortby(tree, col, \
		int(not descending)))

def create_viewer(data_id):
	window = tk.Tk()
	app = Viewer(window,data_id)
	window.mainloop()