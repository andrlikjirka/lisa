#! /usr/bin/python
# -*- coding: utf-8 -*-



# import funkcí z jiného adresáře
import sys
import os.path

path_to_script = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(path_to_script, "../extern/pyseg_base/src/"))
sys.path.append(os.path.join(path_to_script, "../extern/pycat/extern/py3DSeedEditor/"))
sys.path.append(os.path.join(path_to_script, "../src/"))
import unittest

import numpy as np


import organ_segmentation
import dcmreaddata1 as dcmr

class OrganSegmentationTest(unittest.TestCase):
    interactiveTest = False


    @unittest.skipIf(not interactiveTest, "interactive test")
    def test_viewer_seeds(self):

        from seed_editor_qt import QTSeedEditor
        from PyQt4.QtGui import QApplication
        import numpy as np
        img3d = (np.random.rand(30,30,30)*10).astype(np.int16)
        seeds = (np.zeros(img3d.shape)).astype(np.int8)
        seeds[12:18,9:16, 3:6] = 1
        seeds[19:22,21:27, 3:6] = 2
#, QMainWindow
        app = QApplication(sys.argv)
        pyed = QTSeedEditor(img3d, seeds=seeds)
        pyed.exec_()


        deletemask = pyed.getSeeds()
        #import pdb; pdb.set_trace()

        
        #pyed = QTSeedEditor(deletemask, mode='draw')
        #pyed.exec_()

        app.exit()
    #@unittest.skip("demonstrating skipping")
    @unittest.skipIf(not interactiveTest, "interactive test")
    def test_whole_organ_segmentation_interactive(self):
        """
        Interactive test uses dicom data for segmentation
        """
        dcmdir = os.path.join(path_to_script,'./../sample_data/matlab/examples/sample_data/DICOM/digest_article/')
        oseg = organ_segmentation.OrganSegmentation(dcmdir, working_voxelsize_mm = 4)
        
# manual seeds setting
        print ("with left mouse button select some pixels of the brain")
        print ("with right mouse button select some pixels of other tissues and background")

        oseg.interactivity()

        volume = oseg.get_segmented_volume_size_mm3()
        print volume

        self.assertGreater(volume,50000)
        self.assertLess(volume,1200000)


#        roi_mm = [[3,3,3],[150,150,50]]
#        oseg.ni_set_roi()
#        coordinates_mm = [[110,50,30], [10,10,10]]
#        label = [1,2]
#        radius = [5,5]
#        oseg.ni_set_seeds(coordinates_mm, label, radius)
#
#        oseg.make_segmentation()

    def test_box_segmentation(self):
        """
        Function uses organ_segmentation  for synthetic box object 
        segmentation.
        """
        #dcmdir = os.path.join(path_to_script,'./../sample_data/matlab/examples/sample_data/DICOM/digest_article/')
# data
        img3d = np.random.rand(64,64,32) * 5
        img3d[12:32,5:25,4:24] = img3d [12:32,5:25,4:24] + 15

#seeds
        seeds = np.zeros([64,64,32], np.int8)
        seeds [13:31,22:25,9:12] = 1
        seeds [6:9,3:32,9:12] = 2
#[mm]  10 x 10 x 10
        #voxelsize_mm = [1,4,3]
        voxelsize_mm = [5,5,5]
        metadata = {'voxelsizemm': voxelsize_mm}

        oseg = organ_segmentation.OrganSegmentation(None,\
                data3d=img3d, metadata = metadata, \
                seeds = seeds, \
                working_voxelsize_mm = 10)
        

        # oseg.seeds = seeds
        #oseg.make_gc()
# manual seeds setting
        #print ("with left mouse button select some pixels of the brain")
        #print ("with right mouse button select some pixels of other tissues and background")

        oseg.ninteractivity()

        volume = oseg.get_segmented_volume_size_mm3()
        
        #import pdb; pdb.set_trace()

        #mel by to být litr. tedy milion mm3
        self.assertGreater(volume,900000)
        self.assertLess(volume,1100000)

    def test_volume_resize(self):

        pass


    #@unittest.skipIf(True,"interactive test")
    @unittest.skipIf(not interactiveTest, "interactive test")
    def test_vincentka_06_slice_thickness_interactive(self):
        """
        Interactive test. SliceThickness is not voxel depth. If it is, this 
        test will fail.
        """
        #dcmdir = os.path.join(path_to_script,'./../sample_data/matlab/examples/sample_data/DICOM/digest_article/')
        dcmdir = os.path.expanduser('~/data/medical/data_orig/vincentka/13021610/10200000/')
        dcmdir = os.path.expanduser('~/data/medical/data_orig/vincentka/13021610/12460000/')
        oseg = organ_segmentation.OrganSegmentation(dcmdir, working_voxelsize_mm = 4)
        
# manual seeds setting
        print ("with left mouse button select some pixels of the bottle content")
        print ("with right mouse button select some pixels of background")

        oseg.interactivity()

        volume = oseg.get_segmented_volume_size_mm3()
        #print volume

        self.assertGreater(volume,550000)
        self.assertLess(volume,850000)

    def setUp(self):
        """ Nastavení společných proměnných pro testy  """
        self.assertTrue(True)


    # @TODO dodělat přidávání uzlů pomocí mm
    #@unittest.skipIf(not interactiveTest, "interactive test")
    def test_add_seeds_mm(self):
        """
        Function uses organ_segmentation object for segmentation
        """
        dcmdir = os.path.join(path_to_script,'./../sample_data/matlab/examples/sample_data/DICOM/digest_article/')
        oseg = organ_segmentation.OrganSegmentation(dcmdir, working_voxelsize_mm = 4)

        oseg.add_seeds_mm([120],[120],[60], 1, 25)
        oseg.add_seeds_mm([25],[100],[60], 2, 25)

        # pro kontrolu lze odkomentovat
        #oseg.interactivity()

        oseg.ninteractivity()

        volume = oseg.get_segmented_volume_size_mm3()
        
        #import pdb; pdb.set_trace()

        #mel by to být litr. tedy milion mm3
        self.assertGreater(volume,800000)
        self.assertLess(volume,1200000)

        #roi_mm = [[3,3,3],[150,150,50]]
        #oseg.ni_set_roi()
        #coordinates_mm = [[110,50,30], [10,10,10]]
        #label = [1,2]
        #radius = [5,5]
        #oseg.ni_set_seeds(coordinates_mm, label, radius)

        #oseg.make_segmentation()

        #oseg.noninteractivity()
        pass

    @unittest.skip("demonstrating skipping")
    def test_dicomread_and_graphcut(self):
        """
        Test dicomread module and graphcut module
        """
        dcmdir = os.path.join(path_to_script,'./../sample_data/matlab/examples/sample_data/DICOM/digest_article/')
        data3d, metadata = dcmr.dcm_read_from_dir(dcmdir)

        #print ("Data size: " + str(data3d.nbytes) + ', shape: ' + str(data3d.shape) )

        igc = pycat.ImageGraphCut(data3d, zoom = 0.5)
        seeds = igc.seeds
        seeds[0,:,0] = 1
        seeds[60:66,60:66,5:6] = 2
        igc.noninteractivity(seeds)


        igc.make_gc()
        segmentation = igc.segmentation
        self.assertTrue(segmentation[14, 4, 1] == 0)
        self.assertTrue(segmentation[127, 120, 10] == 1)
        self.assertTrue(np.sum(segmentation==1) > 100)
        self.assertTrue(np.sum(segmentation==0) > 100)
        #igc.show_segmentation()

if __name__ == "__main__":
    unittest.main()