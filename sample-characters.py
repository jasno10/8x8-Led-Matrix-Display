# This is an example on how to add, modify, and remove characters in the database

# First, import the module
import PatternDb

if __name__ == "__main__":
    # Instantiate the PatternDb class
    # PatternDb(db_file='pattern.db')
    my_db = PatternDb.PatternDb()

    # Now that we have instantiated the PatternDb class, we can now use all its available features.

    # Let's define three character patterns
    greaterThan_pattern = [[],[],[1,8],[2,7],[3,6],[4,5]]
    lessThan_pattern = [[],[],[4,5],[3,6],[2,7],[1,8]]
    questionMark_pattern = [[],[],[2],[1],[1,4,5,7],[2,3]]
    equalSign_pattern = [[],[],[3,5],[3,5],[3,5],[3,5],[],[]]
    smiley_pattern = [[3,4,5,6],[2,7],[1,3,5,8],[6,8],[6,8],[1,3,5,8],[2,7],[3,4,5,6]]
    sadsmile_pattern = [[3,4,5,6],[2,7],[1,3,5,6,8],[5,8],[5,8],[1,3,5,6,8],[2,7],[3,4,5,6]]
    heart_pattern = [[3,4],[2,3,4,5],[1,2,3,4,5,6,7],[2,3,4,5,6,7,8],[2,3,4,5,6,7,8],[1,2,3,4,5,6,7],[2,3,4,5],[3,4]]
    fish_pattern = [[3,4,5,6],[2,7],[1,4,8],[1,8],[1,8],[2,7],[3,4,5,6],[2,3,4,5,6,7]]
    amongus_pattern = [[],[],[3,4,5,6],[2,3,4,5,6,7],[2,3,4,5,6],[2,3,4,5,6,7],[3,4],[]]
    target_pattern = [[],[2,3,4,5,6,7],[2,7],[2,4,5,7],[2,4,5,7],[2,7],[2,3,4,5,6,7],[]]
    cross_pattern = [[2,3,4,5],[3,4],[1,3,4,8],[1,2,3,4,5,6,7,8],[1,2,3,4,5,6,7,8],[1,3,4,8],[3,4],[2,3,4,5]]
    bomb_pattern = [[],[5,6,7],[4,5,6,7,8],[4,5,6,7,8],[3,4,5,6,7,8],[2,4,5,6,7,8],[1,5,6,7],[]]
    christmasTree_pattern = [[6,7],[5,6,7],[3,4,5,6,7],[1,2,3,4,5,6,7,8],[1,2,3,4,5,6,7,8],[3,4,5,6,7],[5,6,7],[6,7]]
    snowflake_pattern = [[],[2,5,8],[3,5,7],[4,5,6],[2,3,4,5,6,7,8],[4,5,6],[3,5,7],[2,5,7]]
    snowhouse_pattern = [[5,6,7,8],[4],[3,7,8],[2],[3,7,8],[4],[5,6,7,8],[2,3]]

    # Note that there must be eight lists in the pattern and all lists can only contain integers 1 to 8.
    # The numbers correspond to the column number. If you wish to turn off all columns for a row, set it to an empty list.

    # Now that we have a pattern, we have to call a function in PatternDb class to add the patterns.
    # add_drawing(drawing_name, drawing_pattern)
    my_db.add_character('>', greaterThan_pattern)
    my_db.add_character('<', lessThan_pattern)
    my_db.add_character('?', questionMark_pattern)
    # If the pattern is valid and the character name is not yet in the database, it should not throw an exception.

    # Now that we have character patterns in the database now, we can query all or one of the character patterns.
    all_characters = my_db.get_all_characters()
    # all_character should contain [(1, 'greater'), (2, 'lessThan'), (3, 'question')]
    # Note that chara_id may differ.
    # Use this function to enumerate the characters in the database.
    # Note that this does not include the patterns and get_character_pattern() must be called.

    # If you need to get only one character, you can query it via its chara_id
    ##lessThan_character = my_db.get_character(2)
    # lessThan_character should contain (2, 'lessThan')

    # To get a pattern, you can get it using its chara_id
    lessThan_character_pattern = my_db.get_character_pattern(2)
    # LessThan_character_pattern should be similar to lessThan_pattern

    # If you need to update the pattern, call this function:
    # modify_character(chara_id, character_name, character_pattern)
    # The parameters chara_id refer to the unique identifier of the character, character_name is the new character name,
    # and character_pattern is the new pattern
    my_db.modify_character(2, 'Blank', [[], [], [], [], [], [], [], []])
    # The drawing with drawing_id=2 should now have updated drawing name and drawing pattern with no LEDs turned on.

    # To delete a pattern,
    # delete_chara(chara_id)
    # chara_id parameter refers to the unique identifier of the drawing.
    my_db.delete_character(2)
    # The character entry and its pattern should now be deleted.

    # After using the PatternDb class, be sure to properly dispose of it.
    # This closes the connection to the database.
    my_db.cleanup()
