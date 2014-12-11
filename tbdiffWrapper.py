'''
Created on 28 Nov 2014

@author: Craig Griffiths <craig.griffiths@codethink.co.uk>
@copyright: 2014 Codethink Ltd. All rights reserved.
'''

from subprocess import call


def tbdiffCreate(patchDir, sourceDir, targetDir):
    return call(["tbdiff-create", patchDir, sourceDir, targetDir])