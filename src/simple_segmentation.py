#! /usr/bin/python
# -*- coding: utf-8 -*-
#definice konstant
BONES = 1290


# import funkcí z jiného adresáře
import sys
import os.path
path_to_script = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(path_to_script, "../extern/pycat/"))
sys.path.append(os.path.join(path_to_script, "../extern/pycat/extern/py3DSeedEditor/"))
sys.path.append(os.path.join(path_to_script, "../extern/dicom2fem/src"))
#import featurevector

import logging
logger = logging.getLogger(__name__)

import numpy as np
#import scipy.ndimage
import argparse

#from PyQt4.QtCore import Qt
#from PyQt4.QtGui import QApplication, QMainWindow, QWidget,\
#     QGridLayout, QLabel, QPushButton, QFrame, QFileDialog,\
#     QFont, QInputDialog, QComboBox, QRadioButton, QButtonGroup

# ----------------- my scripts --------
import misc
import py3DSeedEditor




class SimpleSegmentation:
    
    def simple_segmentation(self, data3d, voxelsize_mm):
        simple_seg = np.zeros(data3d.shape )

	#definice konvoluční funkce - param a - matice m*n kterou budeme přenásobovat konvoluční maticí, b - Konvoluční maska m*n
	def konvoluce(a, b):
		temp_suma = 0	
		for i in range(a.shape[0]):
			for j in range(a.shape[1]):			
				temp_suma += (a[i][j]*b[i][j]) 
		return temp_suma        
	
	# nalezení kostí
	simple_seg = data3d > BONES 
	simple_seg[(simple_seg.shape[0]/5)*4:simple_seg.shape[0]] = 0
	
	# nalezení páteře
	KONV_MASK = np.ones([3,3], float)
	KONV_MASK = KONV_MASK/9.0	
	operace = 0
	spine_finder = np.zeros([data3d.shape[0],data3d.shape[1]], float)
	for k in range(10):
		for i in range(data3d.shape[0]):
			for j in range(data3d.shape[1]):
				temp_matrix = data3d[j:(j+KONV_MASK.shape[1]),i:(i+KONV_MASK.shape[0]), k]
				temp_matrix = temp_matrix/100
				operace += 1
				#print operace				
				spine_finder[j][i] += konvoluce(temp_matrix, KONV_MASK)
				"""temp_matrix = data3d[i:(i+KONV_MASK.shape[0]), j:(j+KONV_MASK.shape[1]), k]			
#tu je problém nějak musíme z temp_matrix 3d udělat temp_metrix_upravena 2D,
				print type(temp_matrix)
				print temp_matrix.shape
			
				suma_spfi = 0			

#Zajistit aby temp_metrix měla jen 2rozměry, protože jinak bude a[i][j] pole 
			
				print konvoluce(temp_matrix, KONV_MASK)"""
	spine_finder_upraveno = spine_finder > (105)
	######
	spine_finder_upraveno = spine_finder_upraveno*1
	spine_finder_upraveno += np.ones([spine_finder.shape[0],spine_finder.shape[1]])
	
	for id_x in range(simple_seg.shape[0]):
		for id_y in range(simple_seg.shape[1]):
			for id_z in range(simple_seg.shape[2]):
				simple_seg[id_x][id_y][id_z] = simple_seg[id_x][id_y][id_z]*spine_finder_upraveno[id_x][id_y]
				if (spine_finder_upraveno[id_x][id_y] == 2):
		
	import matplotlib.pyplot as plt 	
	plt.figure(figsize=(16, 5))
	plt.subplot(121)
	plt.imshow(spine_finder, cmap = plt.cm.gray)
	plt.subplot(122)
	plt.imshow(spine_finder_upraveno, cmap = plt.cm.gray)
	
		
	return simple_seg

        
def main():

    logger = logging.getLogger()

    logger.setLevel(logging.WARNING)
    ch = logging.StreamHandler()
    logger.addHandler(ch)

    #logger.debug('input params')

    # input parser
    parser = argparse.ArgumentParser(
            description='Module for segmentation of simple anatomical structures')
    parser.add_argument('-i', '--inputfile',
            default='organ.pkl',
            help='path to data dir')

    args = parser.parse_args()

    data = misc.obj_from_file(args.inputfile, filetype = 'pickle')
    data3d = data['data3d']
    voxelsize_mm = data['voxelsize_mm']

    ss = SimpleSegmentation()
    simple_seg = ss.simple_segmentation(data3d, voxelsize_mm)

    #visualization
    pyed = py3DSeedEditor.py3DSeedEditor(data['data3d'], seeds=simple_seg)
    pyed.show()

    # save
    savestring = raw_input('Save output data? (y/n): ')
    if savestring in ['Y', 'y']:
        misc.obj_to_file(data, "resection.pkl", filetype='pickle')


if __name__ == "__main__":
    main()

