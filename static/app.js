const $msg = $('.msg');
const $score = $('.score');
const $timer = $('.timer');
const guessed = new Set();
const $restart = $('#restart');

function decrement_by_one(time) {
	while (time > 0) {
		const new_time = time - 1;
		return new_time;
	}
}

async function guess_word() {
	const word = $('.word').val();
	const data = {
		word : word
	};

	if (guessed.has(word)) {
		$msg.text('Already guessed this word!');
		$('.word').val('');
		return;
	}
	guessed.add(word);

	const res = await axios.get('/check-word', { params: data });
	const result = res.data.result;

	if (result === 'ok') {
		updateScore(word);
		$msg.text('Word found!!');
	} else if (result === 'not-on-board') {
		$msg.text('Word was not found on board');
	} else {
		$msg.text('That is an invalid word...please try again');
	}
	$('.word').val('');
}

$('#add-word-form').on('submit', async function(e) {
	e.preventDefault();
	await guess_word();
});

function updateScore(word) {
	let score = parseInt($('.score').text());
	const points = word.length;

	score += points;
	$('.score').text(score);
}

async function endGame() {
	$('#add-word-form').toggleClass('hidden');
	$msg.toggleClass('hidden');

	let game_score = parseInt($('.score').text());

	const res = await axios.post('/post-score', { score: game_score });
	$restart.toggleClass('hidden');
}

setInterval(() => {
	const new_time = decrement_by_one(parseInt($timer.text()));
	$timer.text(new_time);
}, 1000);
setTimeout(endGame, 60000);
