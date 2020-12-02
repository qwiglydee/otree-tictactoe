class Game {
    /** State of the game */
    constructor(player) {
        this.player = player;
        this.board = undefined;
        this.turn = undefined;
        this.over = false;
        this.winner = null;
    }
}


class View {
    /** rendering of the game */
    constructor(game, elem) {
        this.game = game;
        this.$root = elem;
        this.$cells = this.$root.find('td');

        this.$root.on('click', 'td', (ev) => {
            var idx = Number($(ev.target).data('i') - 1);
            this.$root.trigger('play', {idx: idx});
        })
    }

    render() {
        this.renderBoard();
        this.showStatus("");
        this.showTurn();
        if (this.game.over) {
            this.showWinner();
        }
    }

    renderBoard() {
        this.$cells.each((i, e) => {
            var e = $(e);
            var sym = this.game.board[e.data('i')-1];
            if (sym == '.') {
                e.text('');
            } else {
                e.text(sym);
            }
        });
    }

    showTurn() {
        if (!this.game.over) {
            $('#turn').text(`Current turn: ${this.game.turn}`);
        } else {
            $('#turn_sym').text("Game over!");
        }
    }

    showStatus(msg) {
        $("#status").text(msg);
    }

    showWinner() {
        if (this.game.winner === null) {
            this.showStatus("Tie!");
        } else {
            if (this.game.winner == this.game.player) {
                this.showStatus("You win!");
            } else {
                this.showStatus("You lose!");
            }
        }

    }

    showError(msg) {
        $("#error").text(msg).removeClass('hidden');
    }

    hideError() {
        $("#error").text("").addClass('hidden');
    }

    popError(msg) {
        this.showError(msg);
        window.setInterval(() => this.hideError, 3000);
    }

    highlightPattern(pattern) {
        for(var i of pattern) {
            this.$cells.eq(i).addClass('bg-info');
        }
    }
}


class Controller {
    /** communication with user and server */
    constructor(game, view, aiplays) {
        this.aiplays = aiplays;

        this.game = game;
        this.view = view;

        window.liveRecv = (msg) => {
            if(msg.type == 'game') {
                this.recvGame(msg);
            } else if(msg.type == 'gameover') {
                this.recvGameOver(msg);
            } else if(msg.type == 'error') {
                this.recvError(msg);
            } else {
                console.error("Unrecognized message:", msg);
            }
        }

        this.view.$root.on('play', (ev, params) => this.makeMove(params.idx));
    }

    sendWait() {
        window.liveSend({type: 'ai'});
    }

    sendStart() {
        window.liveSend({type: 'start'});
    }

    sendMove(i) {
        window.liveSend({type: 'move', place: i});
    }

    recvGame(msg) {
        this.game.board = msg.board;
        this.game.turn = msg.turn;
        this.view.render();

        if (this.game.turn == this.game.player) {
            this.view.showStatus("Make your move");
        } else {
            this.view.showStatus("Wait for opponent's move");
        }

        if (this.aiplays && this.aiplays == this.game.turn) {
            this.sendWait();
        }
    }

    recvError(msg) {
        this.view.popError(msg.error);
    }

    recvGameOver(msg) {
        this.game.board = msg.board;
        this.game.turn = msg.turn;
        this.game.over = true;
        this.game.winner = msg.winner;
        this.view.render();

        if (msg.pattern) {
            for (var p of msg.pattern) {
                this.view.highlightPattern(p);
            }
        }
    }

    start() {
        this.sendStart();
    }

    makeMove(place) {
        if (this.game.turn != this.game.player) {
            this.view.popError("Not your turn!");
        } else {
            this.view.hideError();
            this.sendMove(place);
        }
    }
}


var game, view, ctrl;

$(function() {
    game = new Game(js_vars['player_symbol']);
    view = new View(game, $('#game'));
    ctrl = new Controller(game, view, js_vars['ai_symbol']);
    ctrl.start();
})
