import sqlite3
import os.path
import os

class Recorder:
    DEFAULT_DB_LOCATION = "recorder.db"

    QUERY_CREATE_TABLE_USER = '''CREATE TABLE user(
user_id INTEGER PRIMARY KEY,
user_name TEXT UNIQUE,
user_password TEXT
);'''

    QUERY_CREATE_TABLE_DEPOSIT = '''CREATE TABLE deposit(
deposit_id INTEGER PRIMARY KEY,
deposit_name TEXT,
user_id INTEGER,
FOREIGN KEY(user_id) REFERENCES user(user_id)
);'''

    ## RECORDERS

    def recordNewUser(self, userName, userPassword):
        self.__executeAndCommit("INSERT INTO user(user_name, user_password) VALUES(?, ?)", (userName, userPassword))

    def recordNewDeposit(self, depositName, userName):
        userID = self.getUseridByUsername(userName)
        if not userID is None:
            self.__executeAndCommit("INSERT INTO deposit(deposit_name, user_id) VALUES(?, ?)", (depositName, userID))

    
    ## UPDATERS
    # TODO: Implement correct user object
    def updateUser(self, user):
        # TODO: fetch user_id -> udpate all values or return None
        pass

    # TODO: Implement correct deposit object
    def updateDeposit(self, deposit):
        # TODO: fetch deposit_id -> udpate all values or return None
        pass

    ## DELETERS
    def deleteUserByUsername(self, userName):
        self.__deleteBy("user", "user_name", userName)

    def deleteDepositByDepositname(self, depositName):
        self.__deleteBy("deposit", "deposit_name", depositName)

    ## DATA FETCHERS
    def getUseridByUsername(self, userName):
        return self.__selectValueBy("user", "user_id", "user_name", userName)

    def getUserpasswordByUsername(self, userName):
        return self.__selectValueBy("user", "user_password", "user_name", userName)

    def getDepositidByDepositname(self, depositName):
        return self.__selectValueBy("deposit", "deposit_id", "deposit_name", depositName)
    
    def getUserNameByDepositName(self, depositName):
        return self.__getFirstFieldBy("SELECT user_name FROM user NATURAL JOIN deposit WHERE deposit_name=?", (depositName, ))

    def __init__(self, dbLocation=None):
        super().__init__()
        self.dbLocation = self.DEFAULT_DB_LOCATION if dbLocation is None else dbLocation
        dbExists = self.__isDBExists()
        self.connector = sqlite3.connect(self.dbLocation)
        self.cursor = self.connector.cursor()
        if not dbExists:
            self.__createDB()

    def __del__(self):
        self.connector.close()

    def __isDBExists(self): 
        return os.path.isfile(self.dbLocation)

    def __createDB(self):
        for query in (self.QUERY_CREATE_TABLE_USER, self.QUERY_CREATE_TABLE_DEPOSIT):
            self.cursor.execute(query)
        self.connector.commit()
    
    def __getFirstFieldBy(self, query, data):
        self.cursor.execute(query, data)
        result = self.cursor.fetchone()
        if result is None:
            return None
        else:
            return result[0]

    def __deleteBy(self, table, value_name, value):
        self.__executeAndCommit('''DELETE FROM {table:s} WHERE {value_name}=?'''.format(
            table=table, value_name=value_name
        ), (value, ))

    def __selectValueBy(self, table, extractedValueName, valueName, value):
        return self.__getFirstFieldBy('''SELECT {extracted_value_name:s} FROM {table:s} WHERE {value_name}=?'''.format(
            extracted_value_name=extractedValueName ,table=table, value_name=valueName
        ), (value, ))

    def __executeAndCommit(self, query, data=()):
        self.cursor.execute(query, data)
        self.connector.commit()

## DEBUGGING
if __name__ == "__main__":
    os.remove(Recorder.DEFAULT_DB_LOCATION)
    r = Recorder()
    r.recordNewUser("toto", "toto_password")
    r.recordNewUser("tata", "tata_password")
    r.recordNewDeposit("toto_project", "toto")
    print(r.getUseridByUsername("toto"))
    print(r.getUserpasswordByUsername("toto"))
    print(r.getDepositidByDepositname("toto_project"))
    print(r.getUserNameByDepositName("toto_project"))

    print("====")
    print(r.getUseridByUsername("tata"))
    r.deleteUserByUsername("tata")
    print(r.getUseridByUsername("tata"))