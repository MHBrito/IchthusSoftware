# encoding: utf-8
__author__  = '@MBrito'

#Dataframes and some operations
import pandas as pd
import numpy as np

#Remove columns from MzMine File (toDf function)
import openpyxl

#Store and open data (Hist)
import json
from pathlib import Path
import os
import random


from datetime import datetime as dt
from tkinter import messagebox

from core import Core

import _view.view_functions as ViewFunctions 



#Useful functions:
def extfile(string):
	''' Return the extension of a file '''

	s = []
	if string[len(string)-1] == "/" or string[len(string)-1] == "\\":
		print("The path given is a directory.")
	else:
		for i in range(len(string)-1,-1,-1):
			if string[i] == ".":
				s.reverse()
				return ''.join(s)
				break
			elif i == 0:
				print("The file has no extension.")
			s.append(string[i])


#Incomplete Function
def error_handle(message,error,warning=True,type_=0,log=False):
	#Type = 0 -> 
	#Type = 1 -> File not found

	#Console Out
	print(error)

	#User out
	if warning == True:
		ViewFunctions.show_error(message,title=f"Error:")
	

def toDf(arq,analizer):
	''' Open the file and return a datagram with table values ​​based on the file format '''

	a = extfile(arq)
	if a == "xlsx":
		if analizer == "MzMine":
			sheet = (openpyxl.load_workbook(filename=arq)).active
			columns = [cell.value for cell in sheet[2]]
			sheet.delete_rows(idx=1,amount=2)
			return pd.DataFrame(sheet.values,columns=columns)
		return pd.read_excel(pd.ExcelFile(str(arq)))
	elif a == "csv":
		ViewFunctions.show_message("CSV format is not supported in this version")
		raise
	elif a == "odf":
		ViewFunctions.show_message("ODF format is not supported in this version")
		raise
	else:
		ViewFunctions.show_message(f"'.{a}' Format not supported")
		raise


def trunc(num, digits):
	''' Truncate function '''

	sp = str(num).split('.')
	return float('.'.join([sp[0], sp[1][:digits]]))


def mean(itr):
	lista = []
	for i in itr:
		if i != None:
			float(i)
			lista.append(i)
		if sum(lista)>0:
			result = sum(lista)/len(lista)
		else:
			result = None
	return result


def save_dataframe(_format,file_path,dataframe,sheet_name):
	''' Save a dataframe in an excel file '''

	sheet_name = sheet_name[:30] #Limit to 30 chars because Excel worksheet name limit 

	if _format == "excel":
		writer           = pd.ExcelWriter(file_path)
		dataframe.to_excel(writer,sheet_name)
		writer.save()



class Analysis():
	def __init__(self,data):
		self.data = data

	def init_analysis(self):
		
		if self._fill_check() and self._verify_data_type():
			
			try:
				if self._prepare_analysis():
					ViewFunctions.show_message('Analysis has started.')
				self._run_core()
				self._backup_data() #After Core to avoid losses due to storage errors.
				self._store_data()

			except Exception as e:
				ViewFunctions.show_message('An error occurred.')
				raise e
				return False
			
			ViewFunctions.show_message('The analysis is complete.')
			return True


	def _fill_check(self):
		''' Check that all information has been filled in '''

		if self.data['name'] == '':
			ViewFunctions.show_message("Enter job name.")
			return False
		elif self.data['author'] == '':
			ViewFunctions.show_message("Insert the author.")
			return False
		elif self.data['analyser_opt'] == '':
			ViewFunctions.show_message("Choose the data process algorithm.")
			return False
		elif self.data['threshold_param'] == '':
			ViewFunctions.show_message("Choose threshold parameter.")
			return False
		elif self.data['threshold_param'] == 'S/N' and self.data['analyser_opt'] == 'MzMine':
			ViewFunctions.show_message("MzMine doesn't have 'S/N' as column. Please select another threshold parameter.")
			return False
		elif self.data['mz_tol']['active'] == '':
			ViewFunctions.show_message("Set the m/z tolerance for actives.")
			return False
		elif self.data['mz_tol']['inactive'] == '':
			ViewFunctions.show_message("Set the m/z tolerance for inactives (Control).")
			return False
		elif self.data['rt_tol']['active'] == '':
			ViewFunctions.show_message("Set the rt tolerance for actives.")
			return False
		elif self.data['rt_tol']['inactive'] == '':
			ViewFunctions.show_message("Set the rt tolerance for inactives (Control).")
			return False
		elif self.data['th_opt']['active'] == '':
			ViewFunctions.show_message("Select the type of threshold for actives.")
			return False
		elif self.data['th_opt']['inactive'] == '':
			ViewFunctions.show_message("Select the type of threshold for inactives.")
			return False
		elif self.data['th_value']['active'] == '':
			ViewFunctions.show_message("Insert threshold value for actives.")
			return False
		elif self.data['th_value']['inactive'] == '':
			ViewFunctions.show_message("Insert threshold value for inactives.")
			return False
		elif len(self.data['file_paths']['active']) == 0:
			ViewFunctions.show_message("Select active files.")
			return False
		elif len(self.data['file_paths']['inactive']) == 0:
			ViewFunctions.show_message("Select inactive (control) files.")
			return False
		else:
			return True


	def _verify_data_type(self):
		''' Check the type of data containing values '''

		try:
			self.data['th_value']['active'] 	= int(self.data['th_value']['active'])
			self.data['th_value']['inactive'] 	= int(self.data['th_value']['inactive'])
	
		except:
			ViewFunctions.show_message("Threshold value must be an integer.")
			return False
		try:
			self.data['mz_tol']['active'] 		= float(self.data['mz_tol']['active'])
			self.data['mz_tol']['inactive'] 	= float(self.data['mz_tol']['inactive'])
	
		except:
			ViewFunctions.show_message("m/z tolerance value must be a number.")
			return False
		try:
			self.data['rt_tol']['active'] 		= float(self.data['rt_tol']['active'])
			self.data['rt_tol']['inactive'] 	= float(self.data['rt_tol']['inactive'])
	
		except:
			ViewFunctions.show_message("RT tolerance value must be a number.")
			return False

		#If no exception is thrown.	
		return True

	def _prepare_analysis(self):
		''' Transform active and inactive list files into dataframes '''

		self.data['name'] = self.data['name'].strip("' ")
		self.data['active_dataframes'] 		= [toDf(i,self.data['analyser_opt']) for i in self.data['file_paths']['active']]
		self.data['inactive_dataframes']	= [toDf(i,self.data['analyser_opt']) for i in self.data['file_paths']['inactive']]
		return True

	def _run_core(self):
		#Core return the data with dataframe 'Result'
		self.core_obj 	= Core(self.data)
		self.data.update({'result_dataframe':self.core_obj.get_result()})

	def _store_data(self):
		''' Store analysis data in 'Jobs' '''

		self.history_obj = History()
		self.history_obj.add(self.data)

	def _backup_data(self):
		''' Store a backup in .xlsx '''

		datetime		= dt.now()
		datetime_txt	= datetime.strftime("%Y.%m.%d %H.%M")
		file_name		= "{} - {}".format(datetime_txt,self.data['name'])
		file_path		= 'out/'+file_name+'.xlsx'
		
		#Save the excel file
		save_dataframe('excel',file_path,self.data['result_dataframe'],self.data['name'])




class Presets():
	def __init__(self):
		self.load_presets()

	def load_presets(self):
		try:
			with open('presets.json','r') as file:
				self.presets = json.load(file)
		except Exception as e:
			self.create_presets()
			self.load_presets()
			error_handle(e,"Presets have been reset - presets file not found.")

	def create_presets(self):
		self.default_values = {
			'theme':'light',
			'3dgraph':'scatter',
			'analyser_opt':'FindMolFeat',
			'threshold_param':'S/N',
			'threshold_opt':{'active':'relative','inactive':'relative'},
			'threshold_value':{'active':'10','inactive':'10'},
			'mz_tolerance':{'active':'0.005','inactive':'0.005'},
			'rt_tolerance':{'active':'0.1','inactive':'0.1'}
		} 

		with open('presets.json','w') as file:
			json.dump(self.default_values,file,indent=3)
	
	def get(self):
		return self.presets



class History():
	def __init__(self):
		self._verify_paths()
		self._load_metadata()


	def _verify_paths(self):
		''' Checks if the directories exist and if they don't, creates them. '''
		Path("hist/").mkdir(parents=True,exist_ok=True)
		Path("hist/data").mkdir(parents=True,exist_ok=True)


	def _load_metadata(self):
		''' Loads history metafile '''
		try:
			with open('hist/meta.json','r') as load_metaf:
				self.meta_file = json.load(load_metaf)
				self.metadata = self.meta_file['metadata_list']

		except Exception as exc:
			error_handle(exc,warning=False,type_=1,log=True)
			self.metadata = []
			
			if ViewFunctions.get_confirmation("Jobs metafile invalid or not found. Create new Jobs file?"):
				self._create_metafile()
	

	def _create_metafile(self):
		''' Create "Jobs" metafile '''
		with open('hist/meta.json','w+') as create_metaf:
			json.dump({"id":{"type_file":"ichthus_meta_hist"},"metadata_list":[]},create_metaf)
	

	def get(self,order='reverse'):
		''' Return Metadata '''

		#'self.metadata.reverse()' generates future manipulation problems
		if order == 'reverse':
			return self.metadata[::-1]

		return self.metadata


	def add(self,data):
		''' Add data to history '''

		#Generates the current date and time
		datetime   	= dt.now()
		date_txt   	= datetime.strftime("%Y.%m.%d")
		time_txt 	= datetime.strftime("%H.%M")

		#project data file id
		data_id = random.randint(1000,9999)

		#If there is already a file with this ID, it generates another ID
		if os.path.isfile(f"hist/data/{data_id}.json"):
			while os.path.isfile(f"hist/data/{data_id}.json"):
				data_id = random.randint(1000,9999)

		#Analysis Metadata
		meta = {
				'name':data['name'],
				'author': data['author'],
				'threshold_opt':data['th_opt'],
				'threshold_value':data['th_value'],
				'rt_tol':data['rt_tol'],
				'mz_tol':data['mz_tol'],
				'date':date_txt,
				'time':time_txt,
				'duration':None,
				'active_paths':data['file_paths']['active'],
				'inactive_paths':data['file_paths']['inactive'],
				'data_id': data_id,
				'comment':''
		}

		self.metadata.append(meta)

		self.meta_file['metadata_list'] = self.metadata
		with open(f'hist/meta.json','w+') as meta_file:
			json.dump(self.meta_file, meta_file, indent=3)

		'''
			Data file
		'''
		
		#Transform from datagram to dictionary and store
		store_data = {
			"actives":list(map(lambda n: n.to_dict(),data['active_dataframes'])),
			"inactives":list(map(lambda n: n.to_dict(),data['inactive_dataframes'])),
			"result":data['result_dataframe'].to_dict()
		}


		with open(f'hist/data/{data_id}.json','w+') as data_file:
			json.dump(store_data,data_file,indent=3)
		

	def delete(self,_id):
		''' Delete a 'job' from metadata list '''
		for i,x in enumerate(self.metadata):
			if x["data_id"] == _id:
				del self.metadata[i]

				with open('hist/meta.json','w+') as create_metaf:
					json.dump(self.meta_file,create_metaf,indent=3)

				experiment_data = Path(f'hist/data/{_id}.json')
				experiment_data.unlink()
