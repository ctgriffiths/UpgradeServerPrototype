'''
Created on 28 Nov 2014

@author: Craig Griffiths <craig.griffiths@codethink.co.uk>
@copyright: 2014 Codethink Ltd. All rights reserved.
'''

import threading
import SocketServer
import uuid
import time
from DatabaseAccess import DatabaseAccessManager
from tbdiffWrapper import tbdiffCreate

db = DatabaseAccessManager()
PatchJobs = list()
PatchJobsLock = threading.Lock()


class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        getPatch("image1", "image2")
        self.request.sendall("complete")
        '''
        while (1):
            test code, echo response back to client indefinitely, actual patch
            request protocol will be implemented here.

            self.data = self.request.recv(1024).strip()
            print("{} wrote:".format(self.client_address[0]))
            print(self.data)
            self.request.sendall(self.data.upper() + "\n")
            '''


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


def getPatch(SourceImage, TargetImage):
    '''
    If patch has already been created return the file, if not create the patch
    and return it.  If the patch is currently being created then wait for the
    signal that it is complete then return that result rather than generating
    a new patch for every request.
    '''
    PatchDir = db.getPatchDirectory(SourceImage, TargetImage)
    if PatchDir is not None:
        return PatchDir

    PatchName = SourceImage + TargetImage

    CreatePatch = False
    with PatchJobsLock:
        if PatchName in PatchJobs:
            print("already there")
        else:
            CreatePatch = True
            PatchJobs.append(PatchName)
            print("added" + PatchName)

    if CreatePatch is True:
        print("creating patch")
        time.sleep(10) 
        with PatchJobsLock:
            db.addPatch(PatchName, SourceImage, TargetImage, "file-path")
            PatchJobs.remove(PatchName)
        

def createPatch(SourceImage, TargetImage):
    '''
    Create a new patch file from the two images given, store its details in the
    database and return the file path to the patch file.
    '''
    SourceDir = db.getImageDirectory(SourceImage)
    TargetDir = db.getImageDirectory(TargetImage)

    PatchName = str(uuid.uuid4())
    PatchDir = "PatchDir/" + PatchName

    tbdiffCreate(PatchDir, SourceDir, TargetDir)


def main():
    print("main")
    db.connect()
    db.addImage("test5", "x86", "/root/")
    db.addPatch("patch1", "test1", "test2", "/root/")
    print(db.getImageDirectory("test"))
    print(db.getPatchDirectory("test1", "test2"))

    """tbdiffCreate("1","2","3")"""

    HOST, PORT = "localhost", 0
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    print(server.server_address)
    server.serve_forever()

if __name__ == "__main__":
    main()
