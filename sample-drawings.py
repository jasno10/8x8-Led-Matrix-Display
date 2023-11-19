# This is an example on how to add, modify, and remove drawings in the database

# First, import the module
import PatternDb

if __name__ == "__main__":
    # Instantiate the PatternDb class
    # PatternDb(db_file='pattern.db')
    my_db = PatternDb.PatternDb()

    # Now that we have instantiated the PatternDb class, we can now use all its available features.

    # Let's define two patterns
    checkered_pattern = [[1, 3, 5, 7], [2, 4, 6, 8], [1, 3, 5, 7], [2, 4, 6, 8], [1, 3, 5, 7], [2, 4, 6, 8], [1, 3, 5, 7], [2, 4, 6, 8]]
    square_pattern = [[1,2,3,4,5,6,7,8],[1,8],[1,8],[1,8],[1,8],[1,8],[1,8],[1,2,3,4,5,6,7,8]]
    #LETTERS
    A = [[3,4,5,6][2,7][2,7][2,7][2,3,4,5,6,7][2,7][2,7][2,7]]
    B = [[2,3,4,5,6][2,7][2,7][2,3,4,5,6][2,7][2,7][2,7][2,3,4,5,6]]
    C = [[3,4,5,6][2,7][2][2][2][2][2,7][3,4,5,6]]
    D = [[2,3,4,5,6][2,7][2,7][2,7][2,7][2,7][2,7][2,3,4,5,6]]
    E = [[2,3,4,5,6,7][2][2][2,3,4,5,6][2][2][2][2,3,4,5,6,7]]
    F = [[2,3,4,5,6,7][2][2][2,3,4,5,6][2][2][2][2]]
    G = [[3,4,5,6,][2,7][2][2,5,6,7][2,5,6,7][2,7][2,7][3,4,5,6]]
    H = [[2,7][2,7][2,7][2,3,4,5,6,7][2,3,4,5,6,7][2,7][2,7][2,7]]
    I = [[2,3,4,5,6,7][4,5][4,5][4,5][4,5][4,5][4,5][2,3,4,5,6,7]]
    J = [[3,4,5,6,7][7][7][7][7][2,7][2,7][3,4,5,6]]
    K = [[2,7][2,7][2,6][2,3,4,5][2,6][2,7][2,7][2,7]]
    L = [[2][2][2][2][2][2][2][2,3,4,5,6,7]]
    M = [[2,7][2,3,6,7][2,4,5,7][2,7][2,7][2,7][2,7][2,7]]
    N = [[2,7][2,7][2,3,7][2,4,7][2,5,7][2,6,7][2,7][2,7]]
    O = [[3,4,5,6][2,7][2,7][2,7][2,7][2,7][2,7][3,4,5,6]]
    P = [[2,3,4,5,6][2,7][2,7][2,7][2,3,4,5,6][2][2][2]]
    Q = [[3,4,5,6][2,7][2,7][2,7][2,4,7][2,5,7][2,6,7][3,4,5,6,7]]
    R = [[2,3,4,5,6][2,7][2,7][2,3,4,5,6][2,7][2,7][2,7][2,7]]
    S = [[3,4,5,6][2,7][2][2,3,4,5,6][3,4,5,6,7][7][2,7][3,4,5,6]]
    T = [[2,3,4,5,6,7][4,5][4,5][4,5][4,5][4,5][4,5][4,5]]
    U = [[2,7][2,7][2,7][2,7][2,7][2,7][2,7][3,4,5,6]]
    V = [[2,7][2,7][2,7][2,7][2,7][2,7][3,6][4,5]]
    W = [[2,7][2,7][2,7][2,7][2,7][2,4,5,7][2,3,6,7][2,7]]
    X = [[2,7][2,7][3,6][4,5][4,5][3,6][2,7][2,7]]
    Y = [[2,7][2,7][3,6][4,5][4,5][4,5][4,5][4,5]]
    Z = [[2,3,4,5,6,7][7][6][5][4][3][2][2,3,4,5,6,7]]
    #NUMBERS
    num1 = [[4][3,4][4][4][4][4][4][3,4,5]]
    num2 = [[4,5,6][3,7][7][6][5][4][3][3,4,5,6,7]]
    num3 = [[4,5,6][3,7][7][5,6][7][7][3,7][4,5,6]]
    num4 = [[5,6][4,6][3,6][2,6][2,3,4,5,6,7][6][6][6]]
    num5 = [[2,3,4,5,6,7][2][2][2][2,3,4,5,6][7][7][2,3,4,5,6]]
    num6 = [[3,4,5,6][2,7][2][2][2,3,4,5,6][2,7][2,7][3,4,5,6]]
    num7 = [[3,4,5,6,7][7][6][5][5][5][5][5]]
    num8 = [[3,4,5,6][2,7][2,7][2,7][3,4,5,6][2,7][2,7][3,4,5,6]]
    num9 = [[3,4,5,6][2,7][2,7][3,4,5,6,7][7][7][2,7][3,4,5,6]]
    num0 = [[3,4,5,6][2,7][2,3,7][2,4,7][2,5,7][2,6,7][2,7][3,4,5,6]]
    
    # Note that there must be eight lists in the pattern and all lists can only contain integers 1 to 8.
    # The numbers correspond to the column number. If you wish to turn off all columns for a row, set it to an empty list.

    # Now that we have a pattern, we have to call a function in PatternDb class to add the patterns.
    # add_drawing(drawing_name, drawing_pattern)
    my_db.add_drawing('Checkered', checkered_pattern)
    my_db.add_drawing('Square', square_pattern)
    # If the pattern is valid and the drawing name is not yet in the database, it should not throw an exception.

    # Now that we have drawing patterns in the database now, we can query all or one of the drawing patterns.
    all_drawings = my_db.get_all_drawings()
    # all_drawings should contain [(1, 'Checkered'), (2, 'Square')]
    # Note that drawing_id may differ.
    # Use this function to enumerate the drawings in the database.
    # Note that this does not include the patterns and get_drawing_pattern() must be called.

    # If you need to get only one drawing, you can query it via its drawing_id
    square_drawing = my_db.get_drawing(2)
    # square_drawing should contain (2, 'Square')

    # To get a pattern, you can get it using its drawing_id
    square_drawing_pattern = my_db.get_drawing_pattern(2)
    # square_drawing_pattern should be similar to square_pattern

    # If you need to update the pattern, call this function:
    # modify_drawing(drawing_id, drawing_name, drawing_pattern)
    # The parameters drawing_id refer to the unique identifier of the drawing, drawing_name is the new drawing name,
    # and drawing_pattern is the new pattern
    my_db.modify_drawing(2, 'Blank', [[], [], [], [], [], [], [], []])
    # The drawing with drawing_id=2 should now have updated drawing name and drawing pattern with no LEDs turned on.

    # To delete a pattern,
    # delete_drawing(drawing_id)
    # drawing_id parameter refers to the unique identifier of the drawing.
    my_db.delete_drawing(2)
    # The drawing entry and its pattern should now be deleted.

    # After using the PatternDb class, be sure to properly dispose of it.
    # This closes the connection to the database.
    my_db.cleanup()