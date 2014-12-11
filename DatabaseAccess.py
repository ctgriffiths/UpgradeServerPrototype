'''
Created on 28 Nov 2014

@author: Craig Griffiths <craig.griffiths@codethink.co.uk>
@copyright: 2014 Codethink Ltd. All rights reserved.
'''

import psycopg2
import datetime


class DatabaseAccessManager(object):

    connection = None

    def __init__(self):
        print("created database manager")

    def connect(self):
        conn_string = """host='localhost' port='5432' dbname='upgrade_server'
                        user='postgres' password='password'"""
        print ("Connecting to database:\n --> %s" % conn_string)
        self.connection = psycopg2.connect(conn_string)
        print ("Connected\n")

    def getPatchDirectory(self, sourceImage, targetImage):
        if self.connect is None:
            return "ERROR: Connection not initialised"
        cursor = self.connection.cursor()
        cursor.execute("""SELECT * FROM patches WHERE source_image=%s
                        AND target_image=%s;""",
                        (sourceImage, targetImage))
        return cursor.fetchone()

    def getImageDirectory(self, imageName):
        if self.connect is None:
            return "ERROR: Connection not initialised"
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM images WHERE name=%s;",
                       (imageName,))
        return cursor.fetchone()

    def addPatch(self, name, sourceImage, targeImage, file_path):
        cursor = self.connection.cursor()
        try:
            cursor.execute("INSERT INTO patches VALUES (%s, %s, %s, %s, %s)",
                           (name, sourceImage, targeImage,
                            datetime.date(2005, 11, 18), file_path))
        except psycopg2.IntegrityError:
            print("Integrity Error (addPatch): Rolling back transaction.")
            self.connection.rollback()
        else:
            self.connection.commit()

    def addImage(self, name, architecture, file_path):
        cursor = self.connection.cursor()
        try:
            cursor.execute("INSERT INTO images VALUES (%s, %s, %s, %s)",
                           (name, architecture, datetime.date(2005, 11, 18),
                            file_path))
        except psycopg2.IntegrityError:
            print("Integrity Error (addImage): Rolling back transaction.")
            self.connection.rollback()
        else:
            self.connection.commit()
