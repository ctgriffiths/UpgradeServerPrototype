'''
Created on 28 Nov 2014

@author: Craig Griffiths <craig.griffiths@codethink.co.uk>
@copyright: 2014 Codethink Ltd. All rights reserved.
'''

from subprocess import check_call, call
from os.path import expanduser


def tbdiffCreate(patchDir, sourceDir, targetDir):
    return call(["sudo tbdiff-create", patchDir, sourceDir, targetDir], shell=True)

def mount(imagePath, mountPath):
    print ("making directory")
    check_call( [ 'mkdir', expanduser( mountPath ) ] )
    print ("calling mount")
    return call(["sudo mount", 
                       expanduser(imagePath), 
                       expanduser(mountPath)], shell=True)

def unmount(mountPath):
    return check_call(["sudo umount", mountPath])