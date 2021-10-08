class View_Theme():
	def __init__(self,_object):
		self.obj = _object

	def set_View(self):
		self.obj.runbtbg	= "#fff"
		self.obj.runbtfg	= "#353535"
		self.obj.runbtbd	= "#ddd"

	def set_expList(self):
		self.obj.bg_color 	= "#f7f7f7"
		self.obj.empty_btbg = "#dedede"
		self.obj.empty_btfg = "#353535"
		self.obj.listbg 	= "#e9e9e9"
		self.obj.listfg 	= "#424141"
		self.obj.listdtbg 	= "#dcdcdc"
		self.obj.listdelbg 	= "#d23964"

	def set_expSettings(self):
		self.obj.headerbg 	= "#e9e9e9"
		self.obj.headerfg 	= "#3c3c3c"
		self.obj.headerdtbg = "#097588" 
		self.obj.labelfg 	= "#484848"
		self.obj.rbuttonbg  = "#f0f0f0"
		self.obj.labeldtbg1 = "#518c97"
		self.obj.labeldtbg2 = "#097588"
		self.obj.entrybg 	= "#e9e9e9"

	def set_presetsView(self):
		self.obj.bg_color 	= "#efefef"
		self.obj.labeldtbg1 = "#518c97" #To mod
		self.obj.labeldtbg2 = "#097588"	#To mod
		self.obj.labelfg 	= "#484848"	#To mod