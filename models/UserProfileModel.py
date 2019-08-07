class UserProfileModel:
    _timeCreated = ''
    _userID = ''
    _username = ''
    _password   = ''
    _status = -1

    def __init__(self, username = '', password = "") :
        ''' Constructor for this class. '''
        # Create some member animals
        self._username = username
        self._password = password
        
    def getInsertQuery(self) :
        return """
                  INSERT INTO UserProfile 
                  (TimeCreated, UserID, Username, Password, Status)
                  VALUES (toTimestamp(now()), now(), ?, ?, 1);
               """

    def getValuesAsList(self) :
        return [self._username, self._password]

    def getSelectQuery(self, attributes) :
        rawQuery = "SELECT "

        if(len(attributes) == 0) :
            rawQuery += "* "
        else :
            for key in attributes.keys() :
                rawQuery += "%s, " % key
        
        rawQuery += "FROM UserProfile ;"

        return rawQuery
