'''
Created on 28 Nov 2014

@author: Craig Griffiths <craig.griffiths@codethink.co.uk>
@copyright: 2014 Codethink Ltd. All rights reserved.
'''

import SocketServer
from DatabaseAccessModule import DatabaseAccessManager

db = DatabaseAccessManager()


class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
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
