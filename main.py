'''
Created on 28 Nov 2014

@author: Craig Griffiths <craig.griffiths@codethink.co.uk>
@copyright: 2014 Codethink Ltd. All rights reserved.
'''

import SocketServer
from DatabaseAccessModule import DatabaseAccessManager
from PatchFileModule import PatchFileManager

' _Test parameters_ '
SourceImageName = "base"
SourceImagePath = "/home/craiggriffiths/Downloads/baserock-14.22-base-system-x86_64-generic.img"
TargetImageName = "build"
TargetImagepath = "/home/craiggriffiths/Downloads/build-system-x86_64.img"

LogPrefix = "MAIN:\t"
db = DatabaseAccessManager()
PatchManager = PatchFileManager()


class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        print(LogPrefix + "Client connected")
        Patch = PatchManager.getPatch(SourceImageName, TargetImageName)
        self.request.sendall(str(Patch))

        '''
        Send the file back over the socket, only enable this if your resulting
        patch is small otherwise it will take a while over telnet.
        '''
        '''
        f = open(Patch)
        self.request.sendall(f.read())
        '''
        print(LogPrefix + "Request Served")


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


def main():
    print(LogPrefix + "Program Entry Point")
    db.connect()
    db.addImage(SourceImageName, "x86-64", SourceImagePath)
    db.addImage(TargetImageName, "x86-64", TargetImagepath)
    HOST, PORT = "localhost", 0
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    print(LogPrefix + "Listening on: " + str(server.server_address))
    server.serve_forever()

if __name__ == "__main__":
    main()
