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
        Patch = PatchManager.getPatch("test5", "test4")
        self.request.sendall(str(Patch))


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


def main():
    print("main")
    db.connect()
    print(db.getImageDirectory("test"))
    print(db.getPatchDirectory("test1", "test2"))
    HOST, PORT = "localhost", 0
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    print(server.server_address)
    server.serve_forever()

if __name__ == "__main__":
    main()
