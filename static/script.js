$submitButton = $("#submit")
$guessInput = $("#guess")
$words = $("#words")
$score = $("#score")
$newGameButton = $("#new")
$board = $("#board")
$results = $("#results")
$timer = $("#timer")
$highScore = $("#high_score")
$gamesPlayed = $("#games_played")

$submitButton.on("click", async function(evt){
    evt.preventDefault()
    guess = $guessInput[0].value
    $guessInput[0].value = ""

    let result = await axios.get("/check", {params: {guess: guess}})
    console.log(result)
    if (result.data["result"] == "ok"){
        $words.append(`<ul>${guess}</ul>`)
        $score.text(`Score: ${result.data["score"]}`)
    } else {
        alert(guess + " is " + result.data["result"])
    }
})

$(function() {
    setTimeout(function(){
        gameOver(intervalId)
    }, 60000)
    $guessInput.removeAttr("disabled")
    toggleNewGameButton()
    let time = 60
    $timer.text(time)
    let intervalId = setInterval(function(){
        time -= 1
        $timer.text(time)
    }, 1000)
})

function toggleNewGameButton() {
    $newGameButton.toggleClass("btn-primary")
    $newGameButton.toggleClass("btn-outline-primary")
}

function gameOver(intervalId) {
    clearInterval(intervalId)
    $guessInput.attr("disabled", 'disabled')
    $submitButton.toggleClass("btn-primary")
    $submitButton.toggleClass("btn-outline-primary")
    toggleNewGameButton()
    $timer.text("Time's Up!")
    updateLeaderboard()
}

async function updateLeaderboard() {
    newLeaderboard = await axios.get("/update_leaderboard")
    console.log(newLeaderboard)
    $gamesPlayed.text(newLeaderboard.data["games_played"])
    $highScore.text(newLeaderboard.data["high_score"])
}