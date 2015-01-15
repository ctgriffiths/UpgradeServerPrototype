'''
Created on 28 Nov 2014

@author: Craig Griffiths <craig.griffiths@codethink.co.uk>
@copyright: 2014 Codethink Ltd. All rights reserved.
'''

from subprocess import call

LogPrefix = "TBDW:\t"

def tbdiffCreate(patchDir, sourceDir, targetDir):
    print (LogPrefix + "Creating patch: " + patchDir)
    return call(["tbdiff-create", patchDir, sourceDir, targetDir])


def mount(imagePath, mountPath):
    print (LogPrefix + "Making directory: " + mountPath)
    call(['mkdir', mountPath])
    print (LogPrefix + "Mounting image: " + imagePath)
    return call(["mount", imagePath, mountPath])


def unmount(mountPath):
    print (LogPrefix + "Unmounting: " + mountPath)
    return call(["umount", mountPath])
