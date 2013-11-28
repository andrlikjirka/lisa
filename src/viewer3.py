#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
VTK Viewer pro 3D zobrazeni

# program mozne spustit ve dvou rezimech View a Cut
# Vstupní soubor může být soubor pickle nebo už vygenerovaný vtk
# Je mozne zobrazovat cela jatra, nebo hlavni portalni zilu prikazy : liver, porta
# Priklady :
# viewer3.py -vtk mesh_new.vtk -mode 'View' -slab 'liver'
# viewer3.py -pkl vessels002.pkl -mode 'Cut'  -slab 'porta'
'''

from optparse import OptionParser
import sys
import vessel_cut
import numpy as np
import numpy as nm
import scipy.ndimage
import argparse

from PyQt4 import QtCore, QtGui
from PyQt4 import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtk import *
from Tkinter import *
import seg2fem

import misc
import py3DSeedEditor
import show3
import qmisc

# pouzivane promenne 
plane = vtk.vtkPlane()
normal = None
coordinates = None
planew = None
iren = vtk.vtkRenderWindowInteractor()
renWin = vtk.vtkRenderWindow()
surface = vtk.vtkDataSetSurfaceFilter()
app = QApplication(sys.argv)
window = QtGui.QWidget()
okno = QtGui.QWidget()





        
class Viewer():
    
    
    '''
    QVTKViewer(segmentation)
    QVTKViewer(segmentation, voxelsize_mm) # zobrazí vše, co je větší než nula
    QVTKViewer(segmentation, voxelsize_mm, slab) # umožňuje přepínat mezi více rovinami

    qv = QVTKViewer(segmentation, voxelsize_mm, slab, mode='select_plane')
    point = qv.getPlane()
    
    #def __init__(self, inputdata, voxelsize_mm=None, slab=None, mode='view', callbackfcn=None):
        self.inputdata = inputdata
        self.voxelsize_mm = voxelsize_mm
        self.slab = slab
        self.mode = mode
        self.callbackfcn = callbackfcn

    #def __init__(self,segmentation,voxelsize_mm):
        self.segmentation = segmentation
        self.voxelsize_mm = voxelsize_mm
    '''
    def __init__(self, inputfile, mode):
        self.vtk_filename = inputfile
        self.mode = mode

        pass

##------------------------------------------------------------------------------------------    
    def set_normal(self,normal):
        self.normal = normal
        
    def set_coordinates(self,coordinates):
        self.coordinates = coordinates
##------------------------------------------------------------------------------------------
    def generate_mesh(self,segmentation,voxelsize_mm,degrad = 4):
        segmentation = segmentation[::degrad,::degrad,::degrad]
        segmentation = segmentation[:,::-1,:]
        print("Generuji data...")
        mesh_data = seg2fem.gen_mesh_from_voxels_mc(segmentation, voxelsize_mm*degrad)
        if True:
            for x in xrange (10):
                mesh_data.coors = seg2fem.smooth_mesh(mesh_data)
        print("Done")
        vtk_file = "mesh_new.vtk"
        mesh_data.write(vtk_file)
        return vtk_file
##------------------------------------------------------------------------------------------
    '''
    Args:
        inputdata: 3D numpy array 
        voxelsize_mm: Array with voxel dimensions (default=None)
        slab: Dictionary with description of labels used in inputdata
        mode: 'view' or 'select_plane'
        callbackfcn: function which may affect segmentation

    '''
##------------------------------------------------------------------------------------------
    def Plane(self):
        planeWidget = vtk.vtkImplicitPlaneWidget() 
        planeWidget.SetInteractor(iren) 
        planeWidget.SetPlaceFactor(1.5)
        planeWidget.SetInput(surface.GetOutput())
        planeWidget.PlaceWidget()
        planeWidget.TubingOff()
        planeWidget.OutsideBoundsOff()
        planeWidget.ScaleEnabledOff()
        planeWidget.OutlineTranslationOff()
        planeWidget.AddObserver("InteractionEvent", self.Cutter)
            
        planeWidget.On()
        #window.setLayout(grid)

        self.planew = planeWidget
            
        #window.show()
        #iren.Initialize()
        #renWin.Render()
        #iren.Start()
##------------------------------------------------------------------------------------------

    def callback(self,button):
        print button
            
    def Cutter(self,obj, event):
        global plane, selectActor
        obj.GetPlane(plane)

    def liver_view(self):
        print('Zobrazuji liver')
        vessel_cut.View('liver')

    def vein_view(self):
        print('Zobrazuji vein')
        vessel_cut.View('porta')

    def liver_cut(self):
        global normal
        global coordinates
        # pokud bylo stisknuto tlacitko Cut pred Plane, vypise chybu
        try:
            self.set_normal(self.planew.GetNormal())
            self.set_coordinates(self.planew.GetOrigin())
            #print(self.normal)
            #print(self.coordinates)
        except AttributeError:
            print('Neexistuje rovina rezu - Plane')

    # slouzi k nastaveni velikosti voxelu
    def Set_voxel_size(self):
        '''
        rozmer_x = QtGui.QInputDialog()
        rozmer_y = QtGui.QInputDialog()
        rozmer_z= QtGui.QInputDialog()
        #.rozmer_x.getInteger(window,'Voxel_size', 'Rozmer voxelu v x:', QLineEdit.Normal)
        #rozmer_y.getInteger(window, 'Voxel_size', 'Rozmer voxelu v y:', QLineEdit.Normal)
        #rozmer_z.getInteger(window, 'Voxel_size', 'Rozmer voxelu v z:', QLineEdit.Normal)
        okno.setWindowTitle("Voxel_size")
        layout = QtGui.QGridLayout()
        okno.setLayout(layout)
        rozmer_x.setOptions(QInputDialog.NoButtons)
        rozmer_y.setOptions(QInputDialog.NoButtons)
        rozmer_z.setOptions(QInputDialog.NoButtons)
        ok_button = QtGui.QPushButton()
        ok_button.setText('Ok')
        layout.addWidget(rozmer_x,0,2) 
        layout.addWidget(rozmer_y,1,2)      
        layout.addWidget(rozmer_z,2,2)
        layout.addWidget(ok_button,3,2)
        okno.connect(ok_button, QtCore.SIGNAL("clicked()"),(lambda y:lambda: self.close() )('Stisknuto : ok'))
        okno.show()
        renWin.Render()
        iren.Start()
        renWin.Finalize()
   
        #promen_z = QInputDialog()
        #winter = QtCore.QStringList()
        #winter = 'December, January, February'
        #print winter
        #promen_z.setComboBoxItems(winter)
        print(rozmer_x)
        print(rozmer_y)
        print(rozmer_z)

        '''
            
##------------------------------------------------------------------------------------------
    def buttons(self,window,grid):
        '''
        window.resize(80,55)
        layout = QtGui.QVBoxLayout()
        buttons = QtGui.QDialogButtonBox(window)
        buttons.setGeometry(QtCore.QRect(0, 0, 100, 100))
        buttons.setOrientation(QtCore.Qt.Vertical)
        buttons.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Ok)
        buttons.setObjectName(("buttonBox"))
        grid.addWidget(buttons)
        '''
        '''
        # Button liver
        button_liver = QtGui.QPushButton()
        button_liver.setText(unicode('liver'))
        grid.addWidget(button_liver, 1, 0)
        window.connect(button_liver, QtCore.SIGNAL("clicked()"),(lambda y:lambda: self.callback(y) )('Stisknuto : liver'))
        #button_liver.clicked.connect(self.liver_view)
        button_liver.show()

        # Button vein
        button_vein = QtGui.QPushButton()
        button_vein.setText(unicode('vein'))
        grid.addWidget(button_vein, 2, 0)
        window.connect(button_vein, QtCore.SIGNAL("clicked()"),(lambda y:lambda: self.callback(y) )('Stisknuto : vein'))
        #button_vein.clicked.connect(self.vein_view)
        button_vein.show()
        '''
        
        # Button plane
        button_plane = QtGui.QPushButton()
        button_plane.setText(unicode('plane'))
        grid.addWidget(button_plane, 3, 0)
        window.connect(button_plane, QtCore.SIGNAL("clicked()"),(lambda y:lambda: self.callback(y) )('Stisknuto : plane'))
        button_plane.clicked.connect(self.Plane)
        button_plane.show()

        # Button cut
        button_cut = QtGui.QPushButton()
        button_cut.setText(unicode('cut'))
        grid.addWidget(button_cut, 4, 0)
        button_cut.clicked.connect(self.liver_cut) 
        button_cut.show()
        
        #iren.Initialize()
        window.show()
        renWin.Render()
        iren.Start()
        # vypina okno View
        renWin.Finalize()

        
##-----------------------------------------------------------------------------------------    
    def View(self,vtk_filename,accept):

        # Renderer and InteractionStyle
        ren = vtk.vtkRenderer()	
        renWin.AddRenderer(ren)

        iren.SetRenderWindow(renWin)
        iren.SetInteractorStyle(MyInteractorStyle())
        
        # VTK file
        reader = vtk.vtkUnstructuredGridReader()
        reader.SetFileName(vtk_filename)
        reader.Update()

        # VTK surface
        surface.SetInput(reader.GetOutput())
        surface.Update()

        # Cutter
        clipper = vtk.vtkClipPolyData()
        clipper.SetInput(surface.GetOutput())
        clipper.SetClipFunction(plane)
        #clipper.GenerateClipScalarsOn()
        clipper.GenerateClippedOutputOn()

        clipMapper = vtk.vtkPolyDataMapper()
        clipMapper.SetInput(clipper.GetOutput())

        backProp = vtk.vtkProperty()

        clipActor = vtk.vtkActor()
        clipActor.SetMapper(clipMapper)
        clipActor.GetProperty().SetColor(1.0,0.0,0.0)
        clipActor.SetBackfaceProperty(backProp)
        
        cutEdges = vtk.vtkCutter()
        cutEdges.SetInput(surface.GetOutput())
        cutEdges.SetCutFunction(plane)
        cutEdges.GenerateCutScalarsOn()

        cutStrips = vtk.vtkStripper()
        cutStrips.SetInput(cutEdges.GetOutput())
        cutStrips.Update()

        cutPoly = vtk.vtkPolyData()
        cutPoly.SetPoints(cutStrips.GetOutput().GetPoints())
        cutPoly.SetPolys(cutStrips.GetOutput().GetLines())

        cutTriangles = vtk.vtkTriangleFilter()
        cutTriangles.SetInput(cutPoly)
        
        cutMapper = vtk.vtkPolyDataMapper()
        cutMapper.SetInput(cutTriangles.GetOutput())
        
        cutActor = vtk.vtkActor()
        cutActor.SetMapper(cutMapper)
        cutActor.GetProperty().SetColor(1.0,0.0,0.0)

        mapper = vtk.vtkDataSetMapper()
        mapper.SetInput(surface.GetOutput())
        mapper.ScalarVisibilityOff()
        

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().EdgeVisibilityOn()
        # nastavi barvu linek UnstructuredGrid
        actor.GetProperty().SetColor(0.0,0.0,1.0)
        #sirka linek u objektu 
        actor.GetProperty().SetLineWidth(0.1)
        actor.GetProperty().SetRepresentationToWireframe()
        ren.AddActor(clipActor)
        #ren.AddActor(cutActor)
        ren.AddActor(actor)

        # pri rezani se nezobrazi okno protoze iren se inicializuje pouze v buttons, nutno
        # ho inicializovat i tady
        if accept:  
            iren.Initialize()
            renWin.Render()
            iren.Start()
            renWin.Finalize()

##------------------------------------------------------------------------------------------


class MyInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
        def __init__(self,parent=None):
            self.parent = parent
            self.AddObserver("LeftButtonPressEvent",self.LeftButtonPressEvent)
            self.AddObserver("RightButtonPressEvent",self.RightButtonPressEvent)
                 
        def LeftButtonPressEvent(self,obj,event):
            print "Left Button pressed"
            self.Rotate()
            self.OnLeftButtonDown()
            
        def RightButtonPressEvent(self,obj,event):
            print "Right Button pressed"
            self.Pan()
            self.OnRightButtonDown()
        
        e = '%prog [options]\n' + __doc__.rstrip()
help = {
    'in_file': 'input pkl file',
}

    
def main():
    parser = argparse.ArgumentParser(description='Simple VTK Viewer')
    parser.add_argument('-pkl','--picklefile', default=None,
                      help='File as .pkl')
    parser.add_argument('-vtk','--vtkfile', default=None,
                      help='File as .vtk')
    parser.add_argument('-mode','--mode', default=None,
                      help='Mode for construction plane of resection')
    parser.add_argument('-slab','--slab', default = 'liver',
                      help='liver or porta - view')
    args = parser.parse_args()

    #if args.picklefile is None:
    #   raise IOError('No input data!')

    
    # vytvoreni okna
    window = QtGui.QWidget()
    grid = QtGui.QGridLayout()
    window.setWindowTitle("3D liver")
    window.setLayout(grid)
    # vytvoreni vieweru a generovani dat
    viewer = Viewer(args.picklefile,args.mode)
    accept = False
    # dotaz na zadani rozmeru voxelu
    if args.picklefile:
        zadani_rozmeru = raw_input('Chcete zadat rozmery voxelu? (A)no, (N)e (standardni rozmer 1x1x1) : ')
        if zadani_rozmeru == 'A':
            rozmer_x = float(raw_input('Zadejte rozmer x: '))
            rozmer_y = float(raw_input('Zadejte rozmer y: '))
            rozmer_z = float(raw_input('Zadejte rozmer z: '))
        else:
            rozmer_x = 1.0
            rozmer_y = 1.0
            rozmer_z = 1.0
        print ('x : ' ,rozmer_x, ' y : ' ,rozmer_y, ' z : ' ,rozmer_z)
            
        data = misc.obj_from_file(args.picklefile, filetype = 'pickle')
        #segmentation = data['segmentation']
        mesh = viewer.generate_mesh(data['segmentation'] == data['slab'][args.slab],nm.array([rozmer_x, rozmer_y, rozmer_z]))
        if args.mode == 'View' or args.mode == None:
            accept = True
            viewer.View(mesh,accept)
        if args.mode == 'Cut':
            #viewer = QVTKViewer(data['segmentation'], data['voxelsize_mm'], data['slab'])
            accept = False
            viewer.Set_voxel_size()
            viewer.View(mesh,accept)
            viewer.buttons(window,grid)
                        
    if args.vtkfile:
        if args.mode == 'View' or args.mode == None:
            accept = True
            viewer.View(args.vtkfile,accept)
        if args.mode == 'Cut':
            accept = False
            #viewer = QVTKViewer(data['segmentation'], data['voxelsize_mm'], data['slab'])
            viewer.Set_voxel_size()
            viewer.View(args.vtkfile,accept)
            viewer.buttons(window,grid)

    
    app.exec_()
    sys.exit(app.exec_())
    #print viewer.getPlane()

if __name__ == "__main__":
    main()

##------------------------------------------------------------------------------------------
    
