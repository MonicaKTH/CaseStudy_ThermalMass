import json

from zerobnl.kernel import Node

import numpy as np
import fmipp
import os.path


class MyNode(Node):
	"""docstring for MyNode"""

	def __init__(self):
		super().__init__()  # Keep this line, it triggers the parent class __init__ method.


		# This is where you define the attribute of your model, this one is pretty basic.
		# FMU loading
		work_dir = os.path.split(os.path.abspath(__file__))[0]  # define working directory
		model_name = 'COGplant'  # define FMU model name
		path_to_fmu = os.path.join(work_dir, model_name + '.fmu')  # path to FMU		
		uri_to_extracted_fmu = fmipp.extractFMU(path_to_fmu, work_dir)  # extract FMU		
		logging_on = False
		time_diff_resolution = 1e-9		
		self.fmu = fmipp.FMUCoSimulationV1(uri_to_extracted_fmu, model_name, logging_on, time_diff_resolution)
		print( 'successfully loaded the FMU' )

		## FMU instantiation
		start_time = 0.
		stop_time = 450.*8.*24.  # 24 hours
		self.step_size = 450. # 1 hour
		self.tempo=self.step_size
		instance_name = "trnsys_fmu_test"
		visible = False
		interactive = False
		status = self.fmu.instantiate(instance_name, start_time, visible, interactive)
		assert status == fmipp.fmiOK        
		print( 'successfully instantiated the FMU' )	

		## FMU initialization
		stop_time_defined = True
		status = self.fmu.initialize(start_time, stop_time_defined, stop_time)
		assert status == fmipp.fmiOK        
		#fmu.setRealValue( 'Treturn', 40. ) # Very important to initialize 
		print( 'successfully initialized the FMU' )  

	def set_attribute(self, attr, value):
		"""This method is called to set an attribute of the model to a given value, you need to adapt it to your model."""
		super().set_attribute(attr, value)  # Keep this line, it triggers the parent class method.

		#setattr(self, attr, value)
		self.fmu.setRealValue(attr, value)
		assert self.fmu.getLastStatus() == fmipp.fmiOK  

	def get_attribute(self, attr):
		"""This method is called to get the value of an attribute, you need to adapt it to your model."""
		super().get_attribute(attr)  # Keep this line, it triggers the parent class method.

		#return getattr(self, attr)		
		return self.fmu.getRealValue(attr)

	def step(self, value):
		"""This method is called to make a step, you need to adapt it to your model."""
		super().step(value)  # Keep this line, it triggers the parent class method.

		new_step=True		
		print('Time',self.tempo)		
		status = self.fmu.doStep(self.tempo-self.step_size, self.step_size, new_step)        
		assert status == fmipp.fmiOK  
		self.tempo=self.tempo+self.step_size


if __name__ == "__main__":
    node = MyNode()
    node.run()