from flask import Flask, render_template, url_for, flash, redirect, request
from subprocess import call
import RPi.GPIO as GPIO
import sqlite3, PatternDb, ast, LedMatrix, threading, time

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

# Sample Patterns
#square_pattern = [[1,2,3,4,5,6,7,8],[1,8],[1,8],[1,8],[1,8],[1,8],[1,8],[1,2,3,4,5,6,7,8]]
#checkered_pattern = [[1, 3, 5, 7], [2, 4, 6, 8], [1, 3, 5, 7], [2, 4, 6, 8], [1, 3, 5, 7], [2, 4, 6, 8], [1, 3, 5, 7], [2, 4, 6, 8]]
blank = [[], [], [], [], [], [], [], []]


# Matrix initiation
rows = [31, 37, 13, 35, 3, 12, 5, 10]
columns = [36, 7, 8, 32, 11, 33, 38, 40]
matrix = LedMatrix.Matrix(rows,columns)
matrix.update_pattern(blank)

# Shutdown button initiation
button = 15
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Shutdown control
def shutdown():
    matrix.cleanup()
    call("sudo shutdown now", shell=True)

def button_read():
    while True:
        time.sleep(0.001)
        state = GPIO.input(button)
        i = 0
        while i < 1000 and state == 1:
            time.sleep(0.001)
            i = i + 1
            state = GPIO.input(button)
            if i == 1000:
                shutdown()
                return;

shutdown_thread = threading.Thread(target=button_read)
shutdown_thread.start()

@app.route("/", methods=['GET', 'POST'])
def home():
    try:
        if request.method == 'POST':
            submitted_pattern = request.form['patternbox']
            is_valid, processed_pattern = validate_list(submitted_pattern)

            if is_valid:
                matrix.stop_lights()
                matrix.update_pattern(processed_pattern)
                matrix.start_lights()
                
            pattern = processed_pattern;
        else:
            pattern = matrix.get_current_pattern(); # Get Pattern from Matrix class

        return render_template('home.html', title='Homepage', active_pattern=pattern)
    except:
        return render_template('error.html', title='Error')

@app.route("/settings", methods=['GET', 'POST'])
def settings():
    request.get_data()

    # Load Characters
    my_db = PatternDb.PatternDb()
    all_characters = my_db.get_all_characters()
    my_db.cleanup()

    if request.method == 'POST':
        mode = request.form.get('operation')
        if (mode == 'shutdown'):
            matrix.cleanup()
            call("sudo shutdown now", shell=True)
        elif (mode == 'reboot'):
            matrix.cleanup()
            call("sudo reboot now", shell=True)

    return render_template('settings.html', title='Settings', characters=all_characters)



@app.route("/characters", methods=['GET', 'POST'])
def characters():
    request.get_data()
    pattern = matrix.get_current_pattern() # Get Pattern from Matrix class
    char = ''

    if request.method == 'POST':
        char = request.form['charabox']

        my_db = PatternDb.PatternDb()
        pattern = my_db.get_character_pattern(character=char)
        my_db.cleanup();

        # Implement Display Update
        matrix.stop_lights()
        matrix.update_pattern(pattern)
        matrix.start_lights()

    return render_template('characters.html', title='Characters', char=char, active_pattern=pattern)

@app.route("/add-character", methods=['GET', 'POST'])
def add_character():
    request.get_data()

    if request.method == 'POST':
        new_character = request.form['character']
        new_pattern_str = request.form['patternbox']

        is_valid, new_pattern = validate_list(new_pattern_str)

        if is_valid:
            try:
                my_db = PatternDb.PatternDb()
                my_db.add_character(new_character, new_pattern)
                return redirect("/settings")
            except sqlite3.IntegrityError:
                return render_template('add_character.html', title='Add Character', is_hidden='')
            except:
                return render_template('error.html', title='Error')
            finally:
                my_db.cleanup()
        else:
            return render_template('error.html', title='Error')
    else:
        return render_template('add_character.html', title='Add Character', is_hidden='hidden')

@app.route("/modify-character", methods=['GET', 'POST'])
def modify_character():
    request.get_data()
    id = request.args.get('id')

    if id == '' or id is None:
        return redirect("/settings")

    character_id = int(id)

    if request.method == 'POST':
        id = request.form['chara-id']
        new_pattern_str = request.form['patternbox']
        
        is_valid, new_pattern = validate_list(new_pattern_str)

        if is_valid:
            try:
                my_db = PatternDb.PatternDb()
                my_db.modify_character(int(id), new_pattern)
                return redirect("/settings")
            except sqlite3.IntegrityError:
                return render_template('modify_character.html', title='Modify Character', character_id=character_data[0], character=character_data[1], character_pattern=character_data_pattern, is_hidden='')
            finally:
                my_db.cleanup()
        else:
            return render_template('error.html', title='Error')

    else:
        my_db = PatternDb.PatternDb()
        character_data = my_db.get_character(character_id)
        character_data_pattern = my_db.get_character_pattern(character_id)

        my_db.cleanup()
        return render_template('modify_character.html', title='Modify Character', character_id=character_data[0], character=character_data[1], character_pattern=character_data_pattern, is_hidden='hidden')


@app.route("/drawings", methods=['GET', 'POST'])
def drawings():
    try:
        pattern = matrix.get_current_pattern() # Get Pattern from Display
        my_db = PatternDb.PatternDb()
        drawings = my_db.get_all_drawings()
        my_db.cleanup()

        if request.method == 'POST':
            my_db = PatternDb.PatternDb()
            requested_drawing_id = int(request.form['drawing'])
            new_pattern = my_db.get_drawing_pattern(requested_drawing_id)
            my_db.cleanup()
        
            # Implement Display Update
            matrix.stop_lights()
            matrix.update_pattern(new_pattern)
            matrix.start_lights()

            return render_template('drawings.html', title='Drawings', drawings=drawings, active_pattern=new_pattern)
        else:
            return render_template('drawings.html', title='Drawings', drawings=drawings, active_pattern=pattern)
    except:
        return render_template('error.html', title='Error')

@app.route('/modify_drawing', methods=['GET', 'POST'])
def modify_drawing():
    try:
        request.get_data()

        id = request.args.get('id')

        if id == '' or id is None:
            return redirect("/drawings")

        drawing_id = int(id)

        my_db = PatternDb.PatternDb()
        drawing_data = my_db.get_drawing(drawing_id)
        drawing_data_pattern = my_db.get_drawing_pattern(drawing_id)
        my_db.cleanup()

        if request.method == 'POST':
            delete_mode = request.form.get('delete')
            new_name = request.form['drawing-name']
            id = request.form['drawing-id']
            new_pattern_str = request.form['patternbox']
            
            my_db = PatternDb.PatternDb()

            # Deletion
            if delete_mode == 'true':
                try:
                    my_db.delete_drawing(int(id))
                    return redirect("/drawings")
                except:
                    return render_template('error.html', title='Error')
                finally:
                    my_db.cleanup()

            # Modification
            else:
                is_valid, new_pattern = validate_list(new_pattern_str)
                if is_valid:
                    try:
                        my_db.modify_drawing(int(id), new_name, new_pattern)
                        return redirect("/drawings")
                    except sqlite3.IntegrityError:
                        return render_template('modify_drawing.html', title='Modify Drawing', drawing_id=drawing_data[0], drawing_name=drawing_data[1], drawing_pattern=drawing_data_pattern, is_hidden='')
                    except:
                        return render_template('error.html', title='Error')
                    finally:
                        my_db.cleanup()
        else:
            return render_template('modify_drawing.html', title='Modify Drawing', drawing_id=drawing_data[0], drawing_name=drawing_data[1], drawing_pattern=drawing_data_pattern, is_hidden='hidden')
    except:
        return render_template('error.html', title='Error')

@app.route('/add_drawing', methods=['GET', 'POST'])
def add_drawing():
    try:
        request.get_data()
        if request.method == 'POST':
            new_name = request.form['drawing-name']
            new_pattern_str = request.form['patternbox']

            is_valid, new_pattern = validate_list(new_pattern_str)

            if is_valid:
                try:
                    my_db = PatternDb.PatternDb()
                    my_db.add_drawing(new_name, new_pattern)
                    return redirect("/drawings")
                except sqlite3.IntegrityError:
                    return render_template('add_drawing.html', title='Add Drawing', is_hidden='')
                except:
                    return render_template('error.html', title='Error')
                finally:
                    my_db.cleanup()
            else:
                return render_template('error.html', title='Error')
        else:
            return render_template('add_drawing.html', title='Add Drawing', is_hidden='hidden')
    except:
        return render_template('error.html', title='Error')


def validate_list(list_str):
    try:
        parsed_structure = ast.literal_eval(list_str)
        if isinstance(parsed_structure, list) and all(isinstance(sublist, list) for sublist in parsed_structure):
            return True, parsed_structure
        else:
            raise Exception('The pattern parsed from POST is invalid.')
    except:
        raise Exception('The pattern parsed from POST is invalid.')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
