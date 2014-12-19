'''
Created on 12 Dec 2014

@author: Craig Griffiths <craig.griffiths@codethink.co.uk>
@copyright: 2014 Codethink Ltd. All rights reserved.
'''

import threading
import uuid
from DatabaseAccessModule import DatabaseAccessManager
from tbdiffWrapper import tbdiffCreate, mount


class PatchFileManager():

    class PatchJob():

        def __init__(self, PatchName):
            self.PatchName = PatchName
            self.JobComplete = threading.Event()

        @property
        def PatchName(self):
            return self.PatchName

    def __init__(self):
        self.db = DatabaseAccessManager()
        self.PatchJobs = list()
        self.PatchJobsLock = threading.Lock()
        print("PatchFileManager created.")

    def getPatch(self, SourceImage, TargetImage):
        '''
        If patch has already been created return the file, if not create the
        patch and return it.  If the patch is currently being created then wait
        for the signal that it is complete then return that result rather than
        generating a new patch for every request.
        '''
        PatchDir = self.db.getPatchPath(SourceImage, TargetImage)
        if PatchDir is not None:
            return PatchDir

        PatchName = SourceImage + TargetImage

        CreatePatch = False
        CurrentPatchJob = None

        with self.PatchJobsLock:
            for job in self.PatchJobs:
                if job.PatchName == PatchName:
                    CurrentPatchJob = job
                    break
            else:
                CreatePatch = True
                newJob = self.PatchJob(PatchName)
                self.PatchJobs.append(newJob)
                CurrentPatchJob = newJob
                print("added" + PatchName)

        if CreatePatch is False:
            CurrentPatchJob.JobComplete.wait()
            print("Waited, now job is complete!")
        else:
            print("creating patch")
            self.__createPatch(SourceImage, TargetImage, CurrentPatchJob)

        PatchDir = self.db.getPatchPath(SourceImage, TargetImage)
        if PatchDir is not None:
            return PatchDir

    def __createPatch(self, SourceImage, TargetImage, CurrentPatchJob):
        '''
        Create a new patch file from the two images given, store its details in
        the database and return the file path to the patch file.
        '''
        
        SourcePath = self.db.getImagePath(SourceImage)
        TargetPath = self.db.getImagePath(TargetImage)
        
        '''
        Create a sub volume for the two images before running tbdiff. Check how
        this is currently handled in system version manager.  This ideally
        should be files system agnostic so consider mounting images as a fall
        back.
        '''
        
        SourceMountPoint = "/tmp/" + str(uuid.uuid4())
        TargetMountPoint = "/tmp/" + str(uuid.uuid4())
        
        print (SourcePath)
        print (SourceMountPoint)
        mount(SourcePath, SourceMountPoint)
        print (TargetPath)
        print (TargetMountPoint)
        mount(TargetPath, TargetMountPoint)
        
        PatchName = str(uuid.uuid4())
        print("Using patchname: " + PatchName)
        PatchPath = "/" + PatchName
        
        tbdiffCreate(PatchPath, SourcePath, TargetPath)
        
        CurrentPatchJob.JobComplete.set()
        with self.PatchJobsLock:
            self.db.addPatch(PatchName, SourceImage, TargetImage, PatchPath)
            self.PatchJobs.remove(CurrentPatchJob)