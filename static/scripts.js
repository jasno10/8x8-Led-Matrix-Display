// var clickedButtons = [[], [], [], [], [], [], [], []];
var buttonsEnabled = true;

function toggleColor(button, row, col, pattern, event) {
    event.preventDefault();
    //console.log("button: " + button.id);
    //console.log("current pattern:");
    //console.log(pattern);

    // Toggle between led-off and led-on classes
    if (button.classList.contains('led-off')) {
        //console.log('turning on');
        button.classList.remove('led-off');
        button.classList.add('led-on');
    }
    else if (button.classList.contains('led-on')) {
        //console.log('turning off');
        button.classList.add('led-off');
        button.classList.remove('led-on');
    }

    if (button.classList.contains('led-on') == true) {
        //console.log('adding to row ' + row + ' and column ' + col);
        pattern[row].push(col+1);
    }
    else if (button.classList.contains('led-off')) {
        //console.log('removing ' + row + ' and column ' + col);
        let colIndex = pattern[row].indexOf(col + 1);
        colstr = col + 1
        //console.log('removing column ' + colstr + ' at index ' + colIndex);
        pattern[row].splice(colIndex, 1);
    }

    pattern[row].sort();
    displayClickedButtons(pattern);
    // console.log("new pattern:");
    // console.log(pattern);

    // Display the clicked buttons
}

function displayClickedButtons(pattern) {
    // Display the clicked buttons in the console
    // console.clear();
    // console.log('Clicked Buttons:', clickedButtons);
    document.getElementById('arraybox').value = JSON.stringify(pattern);
    // console.log('arraybox'.value)
}

function resetButtons(pattern, event) {
    event.preventDefault();
    //console.log('resetting buttons');
    //console.log('current pattern');
    //console.log(pattern);

    // Get all buttons
    var allButtons = document.querySelectorAll('.led');
    
    // Set all buttons off
    for (let button of allButtons) {
        button.classList.add('led-off');
        button.classList.remove('led-on');
    }

    // Reset pattern
    pattern = [[], [], [], [], [], [], [], []];

    //console.log('new pattern:');
    //console.log(pattern);
    displayClickedButtons(pattern);
    return pattern;
}

function applyClickedButtons(event) {
    event.preventDefault();
    for (var row = 0; row < clickedButtons.length; row++) {
        for (var colIndex = 0; colIndex < clickedButtons[row].length; colIndex++) {
            var col = clickedButtons[row][colIndex];

            // Find the corresponding button and toggle it on
            var button = document.querySelector(`.led[data-row="${row}"][data-col="${col}"]`);
            if (button) {
                button.classList.remove('led-off');
                button.classList.add('led-on');
            }
        }
    }
}

function loadButtons(pattern) {
    // console.log("Loading Buttons!");
    // console.log(pattern);
    rows = ["A", "B", "C", "D", "E", "F", "G", "H"];

    for (let i = 0; i < 8; i++) {
        for (let column of pattern[i]) {
            turnedOnBtn = "btn" + rows[i] + column;
            var element = document.getElementById(turnedOnBtn);
            element.classList.remove('led-off');
            element.classList.add('led-on');
        }
    }
}

function disableAllButtons() {
    // console.log("Disabling buttons");
    rows = ["A", "B", "C", "D", "E", "F", "G", "H"];
    columns = [1, 2, 3, 4, 5, 6, 7, 8];

    for (let i = 0; i < 8; i++) {
        for (let column of columns) {
            searchedButton = "btn" + rows[i] + column;
            // console.log(searchedButton)
            var element = document.getElementById(searchedButton);
            element.disabled = true;
        }
    }
}

function enableAllButtons() {
    // console.log("Enabling buttons");
    rows = ["A", "B", "C", "D", "E", "F", "G", "H"];
    columns = [1, 2, 3, 4, 5, 6, 7, 8];

    for (let i = 0; i < 8; i++) {
        for (let column of columns) {
            searchedButton = "btn" + rows[i] + column;
            // console.log(searchedButton)
            var element = document.getElementById(searchedButton);
            element.disabled = false;
        }
    }
}