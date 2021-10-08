import tkinter as tk
class AboutView:
	def __init__(self,main_object):
		self.main 		= main_object 

		self.window 	= tk.Toplevel(self.main.window,bg="#fff")
		self.window.title("About Ichthus.")
		self.window.resizable(False,False)
		
		self.container = tk.Frame(self.window,bg="#fff")
		self.container.grid(column=1,row=1,sticky="nsew")

		#Ichthus Logo
		self.iheader_img 		= tk.PhotoImage(file="imgs/about_header.png")
		self.header_img 		= tk.Label(self.container,bd=0,image=self.iheader_img)
		self.header_img.image 	= self.iheader_img
		self.header_img.grid(column=1,row=1)

		#About infos
		#self._dev 		= tk.Label(self.container,bg="#fff",text="Version 1.0 - Developed @LQTM(Matheus Henrique Brito Silva, Marcelo Zaldini Hernandes).")
		#self._dev.grid(column=1,row=2,padx=10,pady=5,sticky="w")
		#self._ver 		= tk.Label(self.container,bg="#fff",text="v1.0")
		#self._ver.grid(column=1,row=4,sticky="w")
		#self._lqtm 		= tk.Label(self.container,bg="#fff",text="@LQTM")
		#self._lqtm.grid(column=1,row=4,sticky="e")