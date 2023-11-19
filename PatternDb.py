import sqlite3

# This class handles transaction between the database and the program.
class PatternDb:
    
    def __init__(self, db_file='pattern.db'):
        # This is the constructor of the PatternDb class.
        # Establish connection to database.
        if db_file[-3:] != '.db':
            raise Exception('Database file name must end in .db')
        try:
            self._db_con = sqlite3.connect(db_file)
            self._cursor = self._db_con.cursor()
        except:
            raise Exception('Error establishing connection to the database.')

        # Create Tables
        # Create character_tbl
        self._cursor.execute("CREATE TABLE IF NOT EXISTS character_tbl(chara_id integer primary key, character nvarchar(1) unique not null)")

        # Create character_patterns_tbl
        self._cursor.execute("CREATE TABLE IF NOT EXISTS character_patterns_tbl(chara_id integer not null, row integer, column integer)")

        # Create drawings_tbl
        self._cursor.execute("CREATE TABLE IF NOT EXISTS drawings_tbl(drawing_id integer primary key, drawing_name nvarchar(255) unique not null)")

        # Create drawings_patterns_tbl
        self._cursor.execute("CREATE TABLE IF NOT EXISTS drawings_patterns_tbl(drawing_id integer not null, row integer, column integer)")
        
    def cleanup(self):
        # This method is called before disposing this class. It must handle releasing of resources such as connection string.
        if self._cursor:
            self._cursor.close()
        if self._db_con:
            self._db_con.close()
        
    def get_all_drawings(self):
        # This method returns all drawings available in the database.
        query = self._cursor.execute("SELECT * FROM drawings_tbl ORDER BY drawing_name")
        result = query.fetchall() # This results to a list of tupples in format [(drawing_id, drawing_name)]
        return result

    def get_drawing(self, drawing_id):
        # This method returns a drawing data from id. It should return a tupple of drawing_id and drawing_name
        query = self._cursor.execute("SELECT * FROM drawings_tbl WHERE drawing_id = ?", (drawing_id,))
        result = query.fetchone() # This results to a tupple in format (drawing_id, drawing_name)
        return result

    def get_drawing_pattern(self, drawing_id):
        # This method return the pattern of the drawing obtained from the database searched by parameter drawing_id. It returns a pattern in list of lists format.
        query = self._cursor.execute("SELECT row, column FROM drawings_patterns_tbl WHERE drawing_id = ? ORDER BY row, column ", (drawing_id,))
        result = query.fetchall() # This results to a list of tupples in format [(drawing_id, drawing_name)]
        pattern = self.__convert_to_pattern(result)
        return pattern
        
    def add_drawing(self, drawing_name, drawing_pattern):
        # This method adds a drawing entry and its pattern to the tables.
        is_valid_pattern = self.__validate_pattern(drawing_pattern)

        if is_valid_pattern:
            self._cursor.execute("INSERT INTO drawings_tbl (drawing_name) VALUES (?)", (drawing_name,))
            search_id = self._cursor.execute("SELECT drawing_id FROM drawings_tbl WHERE drawing_name = ?", (drawing_name,))
            result_id = search_id.fetchone()
            drawing_id = result_id[0]

            query_data = self.__format_pattern_to_query(drawing_id, drawing_pattern)
            self._cursor.executemany("INSERT INTO drawings_patterns_tbl (drawing_id, row, column) VALUES (?, ?, ?)", query_data)

            self._db_con.commit()
        else:
            raise Exception('Pattern format is invalid')

    # This method modifies a drawing pattern.
    def modify_drawing(self, drawing_id, drawing_name, drawing_pattern):
        # Validate pattern first
        is_valid_pattern = self.__validate_pattern(drawing_pattern)
        if is_valid_pattern:
            # Update drawing entry
            self._cursor.execute("UPDATE drawings_tbl SET drawing_name = ? WHERE drawing_id = ?", (drawing_name,drawing_id))
            
            # Delete existing pattern first
            self._cursor.execute("DELETE FROM drawings_patterns_tbl WHERE drawing_id = ?", (drawing_id,))
            
            # Insert the updated pattern in list
            query_data = self.__format_pattern_to_query(drawing_id, drawing_pattern)
            self._cursor.executemany("INSERT INTO drawings_patterns_tbl (drawing_id, row, column) VALUES (?, ?, ?)", query_data)

            self._db_con.commit()
        else:
            raise Exception('Pattern is in an invalid format.')

    def delete_drawing(self, drawing_id):
        # This method deletes a drawing pattern from the database.
        self._cursor.execute("DELETE FROM drawings_tbl WHERE drawing_id = ?", (drawing_id,))
        self._cursor.execute("DELETE FROM drawings_patterns_tbl WHERE drawing_id = ?", (drawing_id,))
        self._db_con.commit()
        
    def get_all_characters(self):
        # This method returns all characters in the database. It should return a list of tupples of chara_id and character.
        query = self._cursor.execute("SELECT * FROM character_tbl ORDER BY character")
        result = query.fetchall() 
        return result

    def get_character(self, chara_id):
        # This method returns a character data from id. It should return a tupple of chara_id and character_name
        query = self._cursor.execute("SELECT * FROM character_tbl WHERE chara_id = ?", (chara_id,))
        result = query.fetchone() # This results to a tupple in format (chara_id, character_name)
        return result

    def get_character_pattern(self, character_id=None, character=None):
        # This method return the pattern of a character. It searches the database by looking up the character or its ID. It should return a list of lists.
        #query = self._cursor.execute("SELECT row, column FROM character_patterns_tbl WHERE chara_id = ?", (character_id,))
        #result = query.fetchall()
        pattern = [[], [], [], [], [], [], [], []]

        if character_id is None and character is None:
            raise Exception('You must specificy either a character ID or character')

        if isinstance(character_id, int):
            query = self._cursor.execute("SELECT row, column FROM character_patterns_tbl WHERE chara_id = ? ORDER BY row, column ", (character_id,))
            result = query.fetchall()
            pattern = self.__convert_to_pattern(result)
            return pattern

        elif len(character) == 1:
            search_id = self._cursor.execute("SELECT chara_id FROM character_tbl WHERE character = ?", (character,))
            result_id = search_id.fetchone()

            if result_id is None:
                return pattern
            else:
                res_chara_id = result_id[0]
                query = self._cursor.execute("SELECT row, column FROM character_patterns_tbl WHERE chara_id = ? ORDER BY row, column ", (res_chara_id,))
                result = query.fetchall()
                pattern = self.__convert_to_pattern(result)
                return pattern

        else:
            raise Exception('Invalid parameters passed')
        
    def add_character(self, character, character_pattern):
        # This method adds a character pattern to the database. This feature should not be visible in the web frontend.
        is_valid_pattern = self.__validate_pattern(character_pattern)

        if is_valid_pattern:
            self._cursor.execute("INSERT INTO character_tbl (character) VALUES (?)", (character,))
            search_id = self._cursor.execute("SELECT chara_id FROM character_tbl WHERE character = ?", (character,))
            result_id = search_id.fetchone()
            chara_id = result_id[0]

            query_data = self.__format_pattern_to_query(chara_id, character_pattern)
            self._cursor.executemany("INSERT INTO character_patterns_tbl (chara_id, row, column) VALUES (?, ?, ?)", query_data)

            self._db_con.commit()
        else:
            raise Exception('Pattern format is invalid')
        
    def modify_character(self, character_id, character_pattern):
        # This method modifies a character pattern in the database. This feature should not be visible in the web frontend.
        is_valid_pattern = self.__validate_pattern(character_pattern)
        if is_valid_pattern:
            # Update character entry
            # self._cursor.execute("UPDATE character_tbl SET character = ? WHERE chara_id = ?", (character,chara_id))
            
            # Delete existing pattern first
            self._cursor.execute("DELETE FROM character_patterns_tbl WHERE chara_id = ?", (character_id,))
            
            # Insert the updated pattern in list
            query_data = self.__format_pattern_to_query(character_id, character_pattern)
            self._cursor.executemany("INSERT INTO character_patterns_tbl (chara_id, row, column) VALUES (?, ?, ?)", query_data)

            self._db_con.commit()
        else:
            raise Exception('Pattern is in an invalid format.')
        
    def delete_character(self, character_id):
        # This method removes a character pattern in the database. Although, this feature should not be available at all, it has to exist.
        self._cursor.execute("DELETE FROM character_tbl WHERE chara_id = ?", (chara_id,))
        self._cursor.execute("DELETE FROM character_patterns_tbl WHERE chara_id = ?", (chara_id,))
        self._db_con.commit()

    # This is a private method that will be used to validate that the patterns are in correct format.
    # Patterns should be validated first before they are saved to database.
    def __validate_pattern(self, pattern):
        if pattern is None:
            return False
        elif len(pattern) != 8:
            return False
        else:
            for row in pattern:
                is_valid = all(isinstance(col, int) and 1 <= col <=8 for col in row)
                if is_valid == False:
                    return False
            return True
    
    # This method converts the output of the query from list of tupples to pattern
    def __convert_to_pattern(self, query_result):
        # sample = [(1, 1), (1, 2), (3, 1), (3, 5)]
        pattern = [[], [], [], [], [], [], [], []]

        if query_result is None:
            raise Exception('Query result cannot be None. Consider passing an empty list.')
        # If there are no LEDs on
        if len(query_result) == 0:
            return pattern
        else:
            for led_address in query_result:
                row_num = led_address[0] # Corresponds to row number
                col_num = led_address[1] # Corresponds to column number

                pattern[row_num - 1].append(col_num) # Insert column number to current row_num
                
            return pattern

    # This method formats pattern into list of tupples for query transaction
    def __format_pattern_to_query(self, id, pattern):
        # sample = [[1, 2], [], [1, 5], [], [], [], [], []]
        # sample_id = 1
        query_param = []

        i = 0
        while i < 8:
            if len(pattern[i]) != 0:
                for col in pattern[i]:
                    address = (id, i + 1, col)
                    query_param.append(address)
            i = i + 1
        return query_param # formats sample into [(1,1,1),(1,1,2),(1,3,1),(1,3,5)]