// from https://codepen.io/_Billy_Brown/pen/dbJeh

class Stopwatch {
    constructor(display, results) {
        this.running = false;
        this.display = display;
        this.results = results;
        this.laps = [];
        this.reset();
        this.print(this.times);
    }

    reset() {
        this.times = [ 0, 0, 0 ];
    }

    start() {
        if (!this.time) this.time = performance.now();
        if (!this.running) {
            this.running = true;
            requestAnimationFrame(this.step.bind(this));
        }
    }

    lap() {
        let times = this.times;
		this.laps.push([times])
    }

    stop() {
        this.running = false;
        this.time = null;
    }

    restart() {
        if (!this.time) this.time = performance.now();
        if (!this.running) {
            this.running = true;
            requestAnimationFrame(this.step.bind(this));
        }
        this.reset();
    }

    clear() {
        clearChildren(this.results);
    }

    step(timestamp) {
        if (!this.running) return;
        this.calculate(timestamp);
        this.time = timestamp;
        this.print();
        requestAnimationFrame(this.step.bind(this));
    }

    calculate(timestamp) {
        var diff = timestamp - this.time;
        // Hundredths of a second are 100 ms
        this.times[2] += diff / 10;
        // Seconds are 100 hundredths of a second
        if (this.times[2] >= 100) {
            this.times[1] += 1;
            this.times[2] -= 100;
        }
        // Minutes are 60 seconds
        if (this.times[1] >= 60) {
            this.times[0] += 1;
            this.times[1] -= 60;
        }
    }

    print() {
        this.display.innerText = this.format(this.times);
    }

    format(times) {
        return `\
${pad0(times[0], 2)}:\
${pad0(times[1], 2)}:\
${pad0(Math.floor(times[2]), 2)}`;
    }
}

function pad0(value, count) {
    var result = value.toString();
    for (; result.length < count; --count)
        result = '0' + result;
    return result;
}

function clearChildren(node) {
    while (node.lastChild)
        node.removeChild(node.lastChild);
}

function nextClick() {
	stopwatch.lap();

	let next_panel = document.querySelector('.step-time.step-blank');

	next_panel.value = stopwatch.format(stopwatch.laps[stopwatch.laps.length - 1][0]);
	next_panel.classList.remove('step-blank');
	next_panel.classList.add('step-filled');

	// if there aren't any more empty steps stop the stopwatch and turn off the button
	if (!( document.querySelector('.step-time.step-blank') )) {
		stopwatch.stop();
		document.querySelector('#timer-button').onclick = null;
	};

}

function firstClick() {
	stopwatch.reset();
	stopwatch.start();
	document.querySelector('#timer-button').onclick = nextClick;
	document.querySelector('#timer-button').innerText = "Next";
}

let stopwatch = new Stopwatch(
    document.querySelector('#timer-display'),
    document.querySelector('.stopwatch'));
console.log(stopwatch);
