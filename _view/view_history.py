import tkinter as tk
import tkinter.ttk as ttk
import app_functions as AppFunctions
import _view.view_functions as ViewFunctions
from functools import partial

class View_History():
	''' Sets the front-end of the history '''
	def __init__(self,view_object):
		self.view 			= view_object

		#Colors
		self.historybg 		= view_object.c_historybg

		self.shadow_colors	= view_object.c_hist_shadow

		self.titlebg 		= view_object.c_hist_titlebg
		self.titlefg 		= view_object.c_hist_titlefg
		self.title_spacerbg	= view_object.c_hist_spacer

		self.list_fg 		= view_object.c_hist_listfg
		self.list_openbg	= view_object.c_hist_openbt
		self.list_closebg 	= view_object.c_hist_closebt
		self.list_spacerbg 	= view_object.c_hist_lspacer

		self.history_obj	= AppFunctions.History()
		self.history_data 	= self.history_obj.get()

		self._set_history()


	def _set_history(self):
		self.set_container()
		self.set_hist_shadow() #Shadow Effect

		self.set_header()
		self._set_body()

		self._set_canvas_container()
		self.set_list_container()

		self.set_list() #List of "Old Experiments"
		self.list_fit()


	def set_container(self):
		''' Set 'Jobs' container '''

		self.container = tk.Frame(self.view.window,bg=self.historybg)
		self.container.grid(column=2,row=1,rowspan=5,sticky="nsew")
		#self.container['width'] = (self.view.window_sizes['width']/4)
		#self.container.grid_propagate(False)

		self.container.grid_columnconfigure(2,weight=1)
		self.container.grid_rowconfigure(3,weight=1)

	def set_hist_shadow(self):
		#History "Shadow" effect
		for i in range(len(self.shadow_colors)):
			tk.Frame(self.container,bg=self.shadow_colors[i],width=2).grid(column=1,row=i+1,sticky="ns")


	def set_header(self):
		self.header 	= tk.Frame(self.container,bg=self.titlebg,height=50)
		self.header.grid(column=2,row=1,sticky="nsew")

		self.title_spacer	= tk.Frame(self.container,bg=self.title_spacerbg,height=5).grid(column=2,row=2,sticky="nsew")

		self.title_img 		= tk.PhotoImage(file="imgs/label_history.png")

		if self.view.window_sizes['width'] < 1600:
			self.title_img 	= tk.PhotoImage(file="imgs/label_history_min.png")
	
		self.title 			= tk.Label(self.header,bg=self.titlebg,image=self.title_img)
		self.title.image 	= self.title_img
		self.title.grid(column=1,row=1,pady=(8,0),padx=(1,0),sticky="nsew")

	def _set_body(self):
		self.body 		= tk.Frame(self.container,bg=self.historybg)
		self.body.grid(column=2,row=3,sticky='nsew')
		self.body.grid_rowconfigure(1,weight=1)


	def _set_canvas_container(self):
		s = ttk.Style()
		s.configure('Frame1.TFrame',borderwidth=0,background=self.historybg)
		self.scroll_container = ttk.Frame(self.body,style="Frame1.TFrame")
		self.canvas = tk.Canvas(self.scroll_container,bd=0,bg=self.historybg,width=self.view.window_sizes['width']/4.8)
		self.scrollbar = ttk.Scrollbar(self.scroll_container, orient="vertical", command=self.canvas.yview)
		self.scrollable_frame = ttk.Frame(self.canvas,style="Frame1.TFrame")

		self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

		self.canvas.create_window((0,0), window=self.scrollable_frame, anchor="nw")

		self.canvas.configure(yscrollcommand=self.scrollbar.set)

		self.scroll_container.grid(column=1,row=1,sticky="nsew")
		self.scroll_container.grid_rowconfigure(1,weight=1)
		self.canvas.grid(column=1,row=1,sticky="nsew")
		self.scrollbar.grid(column=2,row=1,sticky="ns")


	def set_list_container(self):
		#Scrollable History

		self.list_cont 		 = tk.Frame(self.scrollable_frame,bg=self.historybg)
		self.list_cont.grid(column=1,row=1,pady=(4,2),sticky="nsew")
		self.list_cont.grid_columnconfigure(1,weight=1)



	def set_list(self):
		''' Cria e povoa a list de elementos do histórico '''
		self.list 			= []

		for i,data in enumerate(self.history_data):
			self.list.append({})

			#List element container
			self.list[i]['cont']		= tk.Frame(self.list_cont,bg=self.historybg,width=self.view.window_sizes['width']/5)
			self.list[i]['cont'].grid(column=1,row=i,padx=(5,5),sticky="nsew")
			self.list[i]['cont'].grid_columnconfigure(1,weight=1)

			if self.view.window_sizes['width'] > 1600:
				self.list[i]['title'] 			= tk.Label(self.list[i]['cont'],text=f"{data['name']}",bg=self.historybg, fg=self.list_fg,font=("Arial",13),anchor="w",width=22).grid(column=1,row=1,sticky="w")
				self.list[i]['date'] 			= tk.Label(self.list[i]['cont'],text=f"{data['date']} at {data['time']}",bg=self.historybg,fg=self.list_fg,font=("Arial",12)).grid(column=1,row=2,sticky="w")
			
			elif self.view.window_sizes['width'] < 1600:
				self.list[i]['title'] 			= tk.Label(self.list[i]['cont'],text=f"{data['name']}",bg=self.historybg, fg=self.list_fg,font=("Arial",13),anchor="w",width=20).grid(column=1,row=1,sticky="w")
				self.list[i]['date'] 			= tk.Label(self.list[i]['cont'],text=f"{data['date']} at {data['time']}",bg=self.historybg,fg=self.list_fg,font=("Arial",11)).grid(column=1,row=2,sticky="w")

			#Button container
			self.list[i]['button_cont'] 	= tk.Frame(self.list[i]['cont'],bg=self.historybg)
			self.list[i]['button_cont'].grid(column=2,row=1,rowspan=2,padx=7,pady=(2,0))
			

			self.list[i]['open_imagem'] 	= tk.PhotoImage(file="imgs/icon_open.png")
		
			if self.view.window_sizes['width'] < 1600:
				self.list[i]['open_imagem'] 	= tk.PhotoImage(file="imgs/icon_open_min.png")

			self.list[i]['open_button'] 	= tk.Button(self.list[i]['button_cont'],image=self.list[i]['open_imagem'],bd=0,bg=self.list_openbg,activebackground=self.list_openbg,command=partial(ViewFunctions.init_viewer,self.view,data['data_id']))
			self.list[i]['open_button'].image = self.list[i]['open_imagem']
			self.list[i]['open_button'].grid(column=2,row=1,padx=1)


			self.list[i]['delete_imagem'] 	= tk.PhotoImage(file="imgs/icon_delete.png")
			
			if self.view.window_sizes['width'] < 1600:
				self.list[i]['delete_imagem'] 	= tk.PhotoImage(file="imgs/icon_delete_min.png")

			self.list[i]['delete_button'] 	= tk.Button(self.list[i]['button_cont'],image=self.list[i]['delete_imagem'],bd=0,bg=self.list_closebg,activebackground=self.list_closebg,command=partial(self.delete_job,data['data_id']))
			self.list[i]['delete_button'].image = self.list[i]['delete_imagem']
			self.list[i]['delete_button'].grid(column=3,row=1)

			
			self.list[i]['spacer'] 			= tk.Frame(self.list[i]['cont'],bg=self.list_spacerbg,height=1).grid(column=1,row=3,columnspan=3,pady=(6,4),padx=3,sticky="ew")

	def list_fit(self):
		self.scrollable_frame.update()
		self.canvas.config(width=self.scrollable_frame.winfo_width())
		self.canvas.update()

	def delete_job(self,_id):
		if ViewFunctions.get_confirmation("You are about to delete a Job.") == True:
			self.history_obj.delete(_id)
			self.refresh_list()

	def refresh_list(self):
		self.history_obj	= AppFunctions.History()
		self.history_data 	= self.history_obj.get()

		self.list_cont.destroy()

		self.set_list_container()
		self.set_list()
		self.list_fit()
