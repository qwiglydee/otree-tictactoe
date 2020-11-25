const game = {
    symbol: js_vars['symbol'],
    ai: js_vars['ai'],
    field: js_vars['field'],
    turn: js_vars['turn'],
    over: false,
}

function show_field() {
    $('td').each((i, e) => {
        var e = $(e);
        var sym = game.field[e.data('i')-1];
        if(sym == '.') {
            e.text('');
        } else {
            e.text(sym);
        }
    });

    $('#turn_sym').text(game.turn);
}

function highlight(pattern) {
    var cells = $('td');
    for(i of pattern) {
        $(cells[i]).addClass('bg-info');
    }
}

function make_move(i) {
    liveSend({type: 'move', place: i});
}

function show_status(msg) {
    $("#status").text(msg);
}

function liveRecv(msg) {
    console.debug("recv", msg);

    if( msg.type == 'error' ) {
        console.error(msg.error);
    }

    if( msg.type == 'game' ) {
        game.field = msg.field;
        game.turn = msg.turn;
        show_field();

        if( game.turn == game.symbol ) {
            show_status("Make your move");
        } else {
            show_status("Wait for opponent's move");
        }

        if( game.ai && game.turn != game.symbol ) {
            liveSend({type: 'waitai'});
        }
    }

    if( msg.type == 'gameover' ) {
        game.field = msg.field;
        game.turn = msg.turn;
        game.over = true;
        show_field();

        $('#turn').addClass('hidden');
        $('#win').removeClass('hidden');

        if( msg.winner == null ) {
            show_status("Tie!");
        } else {
            if( msg.winner == game.symbol ) {
                show_status("You won!");
            } else {
                show_status("You lost!");
            }

            for(p of msg.pattern) {
                highlight(p);
            }
        }
    }
}

$(function() {
    $('table').on('click', (e) => {
        if( game.turn == game.symbol && !game.over ) {
            make_move($(e.target).data('i') - 1);
        }
    });

    liveSend({type: 'start'});
});