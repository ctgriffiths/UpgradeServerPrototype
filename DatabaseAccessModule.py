'''
Created on 28 Nov 2014

@author: Craig Griffiths <craig.griffiths@codethink.co.uk>
@copyright: 2014 Codethink Ltd. All rights reserved.
'''

import psycopg2
import datetime

LogPrefix = "DBM:\t"

class Singleton(type):
    def __call__(self, *args, **kwargs):
        try:
            return self.__instance
        except AttributeError:
            self.__instance = super(Singleton, self).__call__(*args, **kwargs)
            return self.__instance


class DatabaseAccessManager():
    __metaclass__ = Singleton

    connection = None

    def __init__(self):
        print(LogPrefix + "Created Database Manager")

    def connect(self):
        conn_string = """host='localhost' port='5432' dbname='upgrade_server'
                        user='postgres' password='password'"""
        print (LogPrefix + "Connecting to database:\n\t --> %s" % conn_string)
        self.connection = psycopg2.connect(conn_string)
        print (LogPrefix + "Connected")

    def getPatchPath(self, sourceImage, targetImage):
        if self.connect is None:
            return "ERROR: Connection not initialised"
        cursor = self.connection.cursor()
        cursor.execute("""SELECT file_path FROM patches WHERE source_image=%s
                        AND target_image=%s;""", (sourceImage, targetImage))
        record = cursor.fetchone()
        if record:
            return record[0]
            'fetchone() returns a list of 1 item so we want the first value'
        else:
            return None

    def getImagePath(self, imageName):
        if self.connect is None:
            return "ERROR: Connection not initialised"
        cursor = self.connection.cursor()
        cursor.execute("SELECT file_path FROM images WHERE name=%s;",
                       (imageName,))
        record = cursor.fetchone()
        if record:
            return record[0]
            'fetchone() returns a list of 1 item so we want the first value'
        else:
            return None

    def addPatch(self, name, sourceImage, targeImage, file_path):
        cursor = self.connection.cursor()
        try:
            cursor.execute("INSERT INTO patches VALUES (%s, %s, %s, %s, %s)",
                           (name, sourceImage, targeImage,
                            datetime.date(2005, 11, 18), file_path))
        except psycopg2.IntegrityError:
            print(LogPrefix + "Integrity Error (addPatch): Rolling back transaction.")
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
            print(LogPrefix + "Integrity Error (addImage): Rolling back transaction.")
            self.connection.rollback()
        else:
            self.connection.commit()
