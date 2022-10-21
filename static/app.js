baseurl = 'http://127.0.0.1:5000'
const score = $('#score')
const time = $('#time')
const ul_list = $('#list')
const guess_input = $('#guess')

$('#guess_form').on('submit', async function (evt) {
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

function updateScore() {
    score.html(parseInt(score.html()) + 1)
}
function updateList(word) {
    ul_list.append(`<li>${word}</li>`)
}

function handle(result, guess) {
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
    const res = await axios({
        url: `${baseurl}/guess`,
        method: 'POST',
        data: { 'guess': guess }
    });
    const { result } = res.data;
    handle(result, guess)
}