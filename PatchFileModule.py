'''
Created on 12 Dec 2014

@author: craiggriffiths
'''

import threading
import uuid
import time
from DatabaseAccessModule import DatabaseAccessManager
from tbdiffWrapper import tbdiffCreate

class PatchFileManager():
    
    def __init__(self):
        
        self.db = DatabaseAccessManager()
        self.PatchJobs = list()
        self.PatchJobsLock = threading.Lock()
        print("PatchFileManager created.")

    def getPatch(self, SourceImage, TargetImage):
        '''
        If patch has already been created return the file, if not create the patch
        and return it.  If the patch is currently being created then wait for the
        signal that it is complete then return that result rather than generating
        a new patch for every request.
        '''
        PatchDir = self.db.getPatchDirectory(SourceImage, TargetImage)
        if PatchDir is not None:
            return PatchDir

        PatchName = SourceImage + TargetImage

        CreatePatch = False
        with self.PatchJobsLock:
            if PatchName in self.PatchJobs:
                print("already there")
            else:
                CreatePatch = True
                self.PatchJobs.append(PatchName)
                print("added" + PatchName)

        if CreatePatch is True:
            print("creating patch")
            time.sleep(10) 
            with self.PatchJobsLock:
                self.db.addPatch(PatchName, SourceImage, TargetImage, "file-path")
                self.PatchJobs.remove(PatchName)
        

def createPatch(self, SourceImage, TargetImage):
    '''
    Create a new patch file from the two images given, store its details in the
    database and return the file path to the patch file.
    '''
    SourceDir = self.db.getImageDirectory(SourceImage)
    TargetDir = self.db.getImageDirectory(TargetImage)

    PatchName = str(uuid.uuid4())
    PatchDir = "PatchDir/" + PatchName

    tbdiffCreate(PatchDir, SourceDir, TargetDir)
