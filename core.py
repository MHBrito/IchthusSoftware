from datetime import datetime as dt
from tkinter import messagebox

#Dataframes and some operations
import pandas as pd
import numpy as np

#Remove columns from MzMine File (toDf function)
import openpyxl

#Useful Modules
import app_functions as AppFunctions
from _view import view_functions as ViewFunctions

class Init_core:
	def __init__(self,data:dict):
		self.data = data

		self.set_metadata()
		self.set_data()

	def set_metadata(self):

		self.data_analyser 			= self.data['analyser_opt']
		self.threshold_param 		= self.data['threshold_param']
		self.threshold_type 		= self.data['th_opt'] #Dict
		self.threshold_value		= self.data['th_value'] #Dict

		self.rt_tolerance			= self.data['rt_tol'] #Dict
		self.mz_tolerance			= self.data['mz_tol'] #Dict

	def set_data(self):
		self.dataframes 			= {}
		self.dataframes['active'] 	= self.data['active_dataframes']
		self.dataframes['inactive']	= self.data['inactive_dataframes']

class Core(Init_core):
	def __init__(self,data:dict):
		super().__init__(data)


	def get_result(self):
		self.result = self._run_analysis()
		return self.result


	def _run_analysis(self):
		''' Defines the columns that will be used '''
		if self.data_analyser == "MzMine":
			threshold_column 	= "Peak height (Intensity)"
			rt_column 			= "RT (min)"
			mz_column   		= "m/z"
			area_column 		= "Peak area"
			print("MzMine")
		elif self.data_analyser == "FindMolFeat":
			threshold_column 	= self.threshold_param
			rt_column 			= "RT [min]"
			mz_column   		= "m/z"
			area_column 		= "Area"
			print("FindMolFeat")
		else:
			return AppFunctions.handle_error("Unexpected analyzer")

		for exp_type,th_type in self.threshold_type.items():
			if th_type == "absolute":
				self.dataframes[exp_type]		= [x[x[threshold_column] > self.threshold_value[exp_type]] for x in self.dataframes[exp_type]]

			elif th_type == "relative" or th_type == "no_threshold":
				#Sorts according to the threshold column (In the case of MzMine it is unnecessary, but... why not?)
				self.dataframes[exp_type] 		= [(x.sort_values(by=threshold_column,ascending=False)) for x in self.dataframes[exp_type]]

				#Returns only those in "threshold%"
				self.dataframes[exp_type]		= [x[:int(x.shape[0] - x.shape[0] * (self.threshold_value[exp_type]/100))] for x in self.dataframes[exp_type]]

				#Re-order by RT
				self.dataframes[exp_type]		= [(x.sort_values(by=rt_column)) for x in self.dataframes[exp_type]]

		#Creating the table with the results
		results_df = {}
		results_df['Affinity Ratio'] 		= []
		results_df['A(RT)'] 				= []
		results_df['m/z'] 					= []
		results_df['A(Active Area)'] 		= []
		results_df['A(Inactive Area)'] 		= []

		#Column creation
		for x in self.dataframes.items():
			for i,exp in enumerate(x[1]):
				i += 1
				results_df[f'RT ({i}-{x[0][:1].upper()})'] 		= []
				results_df[f'Area ({i}-{x[0][:1].upper()})'] 	= []
				results_df[f'm/z ({i}-{x[0][:1].upper()})'] 	= []

		#results_df = pd.DataFrame(results_df)
			
		for i,data in enumerate(self.dataframes['active']):
			print(f"Iterating over table: {i}")
			#Iterate to the last table
			if i == len(self.dataframes['active'])-1:
				break	
			#Iterates over selected table rows
			for row_index,rt,area,mz in zip(data.index,data[rt_column],data[area_column],data[mz_column]):
				#Table
				temp = {}
				
				for temp_x in self.dataframes.items():
					for temp_i,temp_exp in enumerate(temp_x[1]):
						temp_i += 1
						temp[f'RT ({temp_i}-{temp_x[0][:1].upper()})'] 		= None
						temp[f'Area ({temp_i}-{temp_x[0][:1].upper()})'] 	= None
						temp[f'm/z ({temp_i}-{temp_x[0][:1].upper()})'] 	= None
				
				ion_info = [[],[]]
				ativos_off = False
				#For each row of the selected table, it looks for corresponding ions in the other active tables.
				#print("Start of searches in other tables")
				for tipo,tab_data in self.dataframes.items():
					itol_rt = self.rt_tolerance[tipo]
					itol_mz = self.mz_tolerance[tipo]
					for index,x in enumerate(tab_data):
						if (index <= i and tipo == "active"):
							continue
						#print(f"Type tables {tipo}")
						rtcut = x[(x[rt_column] > rt-itol_rt) & (x[rt_column] < rt+itol_rt)]
						mzcut = rtcut[(rtcut[mz_column] < mz+itol_mz) & (rtcut[mz_column] > mz-itol_mz)]

						if len(list(mzcut.values)) >= 1:
							if len(list(mzcut.values)) > 1:
								data_index = mzcut.iloc[(mzcut[mz_column]-mz).abs().argsort()[:2]]
								data_index = (data_index.index.tolist())[0] #Data_index.index?? Kkkk
								temp[f'RT ({index+1}-{tipo[:1].upper()})'] 		= mzcut.loc[data_index, rt_column]
								temp[f'Area ({index+1}-{tipo[:1].upper()})']	= mzcut.loc[data_index, area_column]
								temp[f'm/z ({index+1}-{tipo[:1].upper()})']    	= mzcut.loc[data_index, mz_column]
								print("More than one find")

							else:
								temp[f'RT ({index+1}-{tipo[:1].upper()})'] 		= (mzcut[rt_column].values)[0]
								temp[f'Area ({index+1}-{tipo[:1].upper()})']	= (mzcut[area_column].values)[0]
								temp[f'm/z ({index+1}-{tipo[:1].upper()})']    	= (mzcut[mz_column].values)[0]

							#Inserts the ion into the temporary list of ions within tolerance
							ion_info[0].append(tipo)
							ion_info[1].append(index)

							#print(f"Index of the ion found: {int(mzcut.index[0])}")
							self.dataframes[tipo][index] = (self.dataframes[tipo][index].drop(mzcut.index[0])).reset_index(drop=True)

						elif index == len(self.dataframes['active'])-1 and temp == {} and tipo == "active":
							#print("Nothing found")
							ativos_off = True
							
					if ativos_off:
						break


				if (ion_info[0].count('active') >= 1 and ion_info[0].count('inactive') >= 1) or ion_info[0].count('inactive') >= 2:
					#Assign data from the table being iterated
					#(Since it doesn't iterate directly over the inactives...)
					temp[f'RT ({i+1}-A)']		= rt
					temp[f'Area ({i+1}-A)']		= area
					temp[f'm/z ({i+1}-A)']		= mz
					
					for temp_title_exp,temp_data_exp in temp.items():
						results_df[temp_title_exp].append(temp_data_exp)

					#Insert the mean of rt in the result
					average_rt			= AppFunctions.mean([*[temp[f'RT ({x}-A)'] for x in range(1,len(self.dataframes['active'])+1)],*[temp[f'RT ({x}-I)'] for x in range(1,len(self.dataframes['inactive'])+1)]])
					results_df['A(RT)'].append(average_rt)

					#Calculates m/z averages
					average_mz			= AppFunctions.mean([*[temp[f'm/z ({x}-A)'] for x in range(1,len(self.dataframes['active'])+1)],*[temp[f'm/z ({x}-I)'] for x in range(1,len(self.dataframes['inactive'])+1)]])
					results_df['m/z'].append(AppFunctions.trunc(average_mz,4))

					#Area averages
					av_active_area 		= AppFunctions.trunc(AppFunctions.mean([temp[f'Area ({x}-A)'] for x in range(1,len(self.dataframes['active'])+1)]),2)
					av_inactive_area	= AppFunctions.trunc(AppFunctions.mean([temp[f'Area ({x}-I)'] for x in range(1,len(self.dataframes['inactive'])+1)]),2)
					
					#Insert in result
					results_df['A(Active Area)'].append(av_active_area)
					results_df['A(Inactive Area)'].append(av_inactive_area)

					#Calculates the average of the areas and inserts in the result
					results_df['Affinity Ratio'].append(av_active_area/av_inactive_area)

					#print("Final dict")
				else:
					pass
					#print("Nothing was found")

		#for x,i in results_df.items():
		#	print(f"Size of {x} é: {len(i)}")

		results_df = pd.DataFrame(results_df).sort_values(by="A(RT)")
		results_df['A(RT)'] = results_df['A(RT)'].apply(lambda x: AppFunctions.trunc(x,2))
		results_df['Affinity Ratio'] = results_df['Affinity Ratio'].apply(lambda x: AppFunctions.trunc(x,2))
		return results_df

