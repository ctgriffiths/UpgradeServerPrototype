'''
Created on 28 Nov 2014

@author: Craig Griffiths <craig.griffiths@codethink.co.uk>
@copyright: 2014 Codethink Ltd. All rights reserved.
'''


def tbdiffCreate(patchDir, sourceDir, targetDir):
    print ("Please run: tbdiff-create " + patchDir + " "
                                        + sourceDir + " "
                                        + targetDir)
    raw_input("Press Enter when the command completes...")

def mount(imagePath, mountPath):
    print ("Please run: mkdir " + mountPath)
    raw_input("Press Enter when the command completes...")

    print ("Please run: mount " + imagePath + " " + mountPath)
    raw_input("Press Enter when the command completes...")

def unmount(mountPath):
    print ("Please run: umount " + mountPath)
    raw_input("Press Enter when the command completes...")