baseurl = 'http://127.0.0.1:5000'
const score = $('#score');
const game_time = $('#time');
const ul_list = $('#list');
const guess_input = $('#guess');
const guess_btn = $('#guess_btn');
const start_btn = $('#start');
const reset_btn = $('#reset');

$('#guess_form').on('submit', async function (evt) {
    // handle users input/guess from the form.
    evt.preventDefault();
    const guess = guess_input.val().toLowerCase();
    guess_input.val('')
    if (!guess) return;
    try {
        await isValidGuess(guess)
    } catch (e) {
        console.log(e)
    }
})
start_btn.on('click', startGame)

function startGame() {
    // enable buttons and inputs start the timer
    guess_btn.toggleClass('disabled')
    guess_input.prop('disabled', false)
    start_btn.toggleClass('disabled');
    reset_btn.toggleClass('disabled');
    startTimer()
}
function stopGame() {
    // disable inputs
    guess_btn.toggleClass('disabled')
    guess_input.prop('disabled', true)
}

function updateScore() {
    // updates the score on the html page
    score.html(parseInt(score.html()) + 1)
}
function updateList(word) {
    // updates ul with valid words
    ul_list.append(`<li>${word}</li>`)
}

function alertUser(result, guess) {
    // temporary way to alert the user if word is not valid.
    if (result == 'ok') {
        updateScore()
        updateList(guess)
    } else if (result == 'not-word') {
        alert('not-word')
    } else if (result == 'not-on-board') {
        alert('not-on-board')
    } else if (result == 'already used') {
        alert('already used')
    }
}

async function isValidGuess(guess) {
    // sends word to server to check if its valid
    try {
        const res = await axios({
            url: `${baseurl}/guess`,
            method: 'POST',
            data: { 'guess': guess }
        });
        const { result } = res.data;
        alertUser(result, guess)
    } catch (e) {
        console.log(e)
    }
}


let timeoutID;
let sec = 60
function startTimer() {

    timeoutID = setInterval(updateTimer, 1000);
}

function updateTimer() {
    // update timer on html page also checks if timer reached 0
    sec = (sec - 1);
    game_time.html(sec);
    if (sec == 0) {
        stopGame();
        clearTimeout(timeoutID);
        recordScore()
    }
}

async function recordScore() {
    // send post request to update session score if new high score. 
    try {
        const res = await axios({
            url: `${baseurl}/record_score`,
            method: 'POST',
        });
        const { high_score } = res.data;
        if (high_score) {
            alert('new high score!')
        } else if (high_score == 0) {
            alert('keep trying')
        }
    } catch (e) {
        alert('something when wrong while recording your score')
        console.log(e)
    }
}