'''
Created on 28 Nov 2014

@author: Craig Griffiths <craig.griffiths@codethink.co.uk>
@copyright: 2014 Codethink Ltd. All rights reserved.
'''

import SocketServer
from DatabaseAccessModule import DatabaseAccessManager
from PatchFileModule import PatchFileManager

db = DatabaseAccessManager()
PatchManager = PatchFileManager()


class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        self.request.sendall("yes")
        Patch = PatchManager.getPatch("base", "build")
        self.request.sendall(str(Patch))


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


def main():
    print("main")
    db.connect()
    db.addImage("base", "x86-64", "/home/craiggriffiths/Downloads/baserock-14.22-base-system-x86_64-generic.img")
    db.addImage("build", "x86-64", "/home/craiggriffiths/Downloads/build-system-x86_64.img")
    print(db.getImagePath("base"))
    print(db.getImagePath("build"))
    print(db.getPatchPath("test1", "test2"))
    HOST, PORT = "localhost", 0
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    print(server.server_address)
    server.serve_forever()

if __name__ == "__main__":
    main()
