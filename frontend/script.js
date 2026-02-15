const API_URL = "http://127.0.0.1:8000";

let players = [];
let questionsPerPlayer = 3;
let totalRounds = 0;
let currentRound = 0;
let currentPlayerIndex = 0;
let currentQuestionData = null;

function addPlayer() {
    const nameInput = document.getElementById("playerName");
    const name = nameInput.value.trim();

    if (!name) return;

    players.push({
        name: name,
        score: 0
    });

    updatePlayerList();
    nameInput.value = "";
}

function updatePlayerList() {
    const list = document.getElementById("playerList");
    list.innerHTML = "";

    players.forEach(p => {
        const li = document.createElement("li");
        li.innerText = p.name;
        list.appendChild(li);
    });
}

function startGame() {
    if (players.length < 1) {
        alert("Mindestens ein Spieler erforderlich!");
        return;
    }

    questionsPerPlayer = parseInt(document.getElementById("questionCount").value);

    totalRounds = questionsPerPlayer * players.length;
    currentRound = 0;
    currentPlayerIndex = 0;

    document.getElementById("setup").style.display = "none";
    document.getElementById("result").style.display = "none";
    document.getElementById("quiz").style.display = "block";

    loadQuestion();
}

async function loadQuestion() {
    if (currentRound >= totalRounds) {
        endGame();
        return;
    }

    document.getElementById("feedback").innerText = "";

    const response = await fetch(`${API_URL}/question`);
    const data = await response.json();
    currentQuestionData = data;

    const currentPlayer = players[currentPlayerIndex];

    document.getElementById("currentPlayer").innerText =
        `🎮 ${currentPlayer.name} ist dran`;

    document.getElementById("questionText").innerText =
        `Frage ${Math.floor(currentRound / players.length) + 1}: ${data.question}`;

    const answersDiv = document.getElementById("answers");
    answersDiv.innerHTML = "";

    data.options.forEach((option, index) => {
        const btn = document.createElement("button");
        btn.innerText = option;
        btn.onclick = () => submitAnswer(index);
        answersDiv.appendChild(btn);
    });
}

function nextTurn() {
    document.getElementById("continueBtn").style.display = "none";
    document.getElementById("explanation").style.display = "none";
    document.getElementById("feedback").innerText = "";

    currentRound++;
    currentPlayerIndex = (currentPlayerIndex + 1) % players.length;

    loadQuestion();
}

async function submitAnswer(selectedIndex) {
    const currentPlayer = players[currentPlayerIndex];

    // Buttons deaktivieren
    const buttons = document.querySelectorAll("#answers button");
    buttons.forEach(btn => btn.disabled = true);

    const response = await fetch(`${API_URL}/answer`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            question_id: currentQuestionData.id,
            selected_option: selectedIndex
        })
    });

    const result = await response.json();

    const feedback = document.getElementById("feedback");
    const explanation = document.getElementById("explanation");
    const continueBtn = document.getElementById("continueBtn");

    if (result.correct) {
        currentPlayer.score++;
        feedback.innerText = "✅ Richtig!";
        feedback.style.color = "green";

        explanation.style.display = "none";
    } else {
        feedback.innerText = `❌ Falsch!`;
        feedback.style.color = "red";

        explanation.innerText = result.explanation;
        explanation.style.display = "block";
    }

    continueBtn.style.display = "inline-block";
}

function endGame() {
    document.getElementById("quiz").style.display = "none";
    document.getElementById("result").style.display = "block";

    const scoreDiv = document.getElementById("finalScores");
    scoreDiv.innerHTML = "";

    // Sortieren nach Punkten
    players.sort((a, b) => b.score - a.score);

    players.forEach((p, index) => {
        const pElement = document.createElement("p");
        pElement.innerText = `${index + 1}. ${p.name}: ${p.score} Punkte`;
        scoreDiv.appendChild(pElement);
    });
}

function restart() {
    players.forEach(p => p.score = 0);
    document.getElementById("setup").style.display = "block";
    document.getElementById("result").style.display = "none";
}
