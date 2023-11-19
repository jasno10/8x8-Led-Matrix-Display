import RPi.GPIO as GPIO
import time
import threading

class Matrix:
    pattern = None
    is_running = False

    #Switch rows and/or columns on or off
    def Switch(self, state, row=None, column=None):

        # Check if row and column parameters are None. Throw exception if both are None.
        if row is None and column is None:
            raise Exception('Either ROW or COLUMN must be defined')

        # Check state parameter
        if state == True or state == False:
            state = state
        elif state.upper() == 'ON':
            state = True
        elif state.upper() == 'OFF':
            state = False
        else:
            raise Exception('state must be either "ON", "OFF", or boolean')
        
        # For 1088AS LED Matrix
        if self.model == '1088AS':

            # Turn ON
            if state == True:
                if column is not None:
                    GPIO.output(column, GPIO.HIGH) #Column Must be HIGH to Turn ON
                
                if row is not None:
                    GPIO.output(row, GPIO.LOW) #Row Must be LOW to Turn ON

            # Turn OFF  
            elif state == False:
                if column is not None:
                    GPIO.output(column, GPIO.LOW) #Column Must be LOW to Turn OFF
                
                if row is not None:
                    GPIO.output(row, GPIO.HIGH) #Row Must be HIGH to Turn OFF

        # For 1088BS LED Matrix
        elif self.model == '1088BS':

            # Turn ON
            if state == True:
                if column is not None:
                    GPIO.output(column, GPIO.LOW) #Column Must be LOW to Turn ON
                
                if row is not None:
                    GPIO.output(row, GPIO.HIGH) #Row Must be HIGH to Turn ON

            # Turn OFF  
            elif state == False:
                if column is not None:
                    GPIO.output(column, GPIO.HIGH) #Column Must be HIGH to Turn OFF
                
                if row is not None:
                    GPIO.output(row, GPIO.LOW) #Row Must be LOW to Turn OFF

    def run_lights(self):
        current_state = self.is_running
        while current_state:
            with self.thread_lock:
                current_pattern = self.pattern
                current_state = self.is_running
                i=0
                for row in self.ALL_ROW:
                    # Turn on current Row
                    self.Switch(True, row=row)

                    # Turn on columns
                    for col in current_pattern[i]:
                        columnNum = self.ALL_COL[col-1]
                        self.Switch(True, column = columnNum)
                        # time.sleep(0.5) # uncomment to see modulation
                
                    time.sleep(0.0001)

                    # Turn off columns
                    for col in self.ALL_COL:
                        self.Switch(False, column = col)
                        # time.sleep(0.5) # uncomment to see modulation

                    # Turn off current Row
                    # time.sleep(0.001)
                    self.Switch(False, row=row)
                    i = i + 1

    def start_lights(self):
        if self.pattern == None:
            raise Exception('pattern is not defined')
        elif len(self.pattern) != 8:
            raise Exception('pattern must contain 8 lists')

        self.is_running = True

        if self.run_thread is None:
            self.run_thread = threading.Thread(target=self.run_lights)
            self.run_thread.start()

    def stop_lights(self):
        if self.run_thread is not None:
            with self.thread_lock:
                self.is_running = False
            self.run_thread.join()
            self.run_thread = None

    def update_pattern(self, new_pattern):
        if new_pattern is None:
            raise Exception('New pattern cannot be None')
        elif len(new_pattern) != 8:
            raise Exception('Pattern must contain 8 lists')
        else:
            for row in new_pattern:
                is_valid = all(isinstance(col, int) and 1 <= col <=8 for col in row)
                if is_valid == False:
                    raise Exception('Invalid column number detected')

            with self.thread_lock:
                self.pattern = new_pattern

    def cleanup(self):
        self.stop_lights()
        GPIO.cleanup()

    def __init__(self, row, column, model='1088AS', pin_mode=GPIO.BOARD):
        
        #Parameter Validation
        #Validate Row
        if len(row) != 8:
            raise Exception('Row length must be 8')

        #Validate Column
        if len(column) != 8:
            raise Exception('Column length must be 8')

        #Validate Model
        if model.upper() != '1088AS' and model.upper() != '1088BS':
            raise Exception('Model must either be 1088AS or 1088BS')

        #Validate pin mode
        if pin_mode != GPIO.BOARD and pin_mode != GPIO.BCM:
            raise Exception('pin_mode must either be GPIO.BOARD or GPIO.BCM')

        # Initialize properties
        self.pattern = None
        self.is_running = False
        self.model = model
        self.run_thread = None
        self.thread_lock = threading.Lock()

        # Assign pins to rows
        self.ROW_A = row[0]
        self.ROW_B = row[1]
        self.ROW_C = row[2]
        self.ROW_D = row[3]
        self.ROW_E = row[4]
        self.ROW_F = row[5]
        self.ROW_G = row[6]
        self.ROW_H = row[7]

        self.ALL_ROW = [self.ROW_A, self.ROW_B, self.ROW_C, self.ROW_D, self.ROW_E, self.ROW_F, self.ROW_G, self.ROW_H]

        # Assign pins to columns
        self.COL_1 = column[0]
        self.COL_2 = column[1]
        self.COL_3 = column[2]
        self.COL_4 = column[3]
        self.COL_5 = column[4]
        self.COL_6 = column[5]
        self.COL_7 = column[6]
        self.COL_8 = column[7]

        self.ALL_COL = [self.COL_1, self.COL_2, self.COL_3, self.COL_4, self.COL_5, self.COL_6, self.COL_7, self.COL_8]

        # Setup output pins

        GPIO.setmode(pin_mode)
        for row in self.ALL_ROW:
            GPIO.setup(row, GPIO.OUT)
            GPIO.output(row, GPIO.HIGH)
            
        for col in self.ALL_COL:
            GPIO.setup(col, GPIO.OUT)
            GPIO.output(col, GPIO.LOW)
