const game = {
    symbol: js_vars['symbol'],
    field: js_vars['field'],
    turn: js_vars['turn']
}

function show_field() {
    $('td').each((i, e) => {
        var e = $(e);
        var sym = game.field[e.data('i')-1];
        if(sym == '_') {
            e.text('');
        } else {
            e.text(sym);
        }
    });

    $('#turn_sym').text(game.turn);
}

function make_move(i) {
    liveSend({'move': i});
}

function liveRecv(msg) {
    if( msg.type == 'error' ) {
        console.error(msg.error);
    }

    if( msg.type == 'game') {
        game.field = msg.field;
        game.turn = msg.turn;
        show_field();
    }

    if( msg.type == 'gameover' ) {
        game.field = msg.field;
        game.turn = msg.turn;
        show_field();

        $('#turn').addClass('hidden');
        $('#win').removeClass('hidden');
        if( msg.winner == game.symbol ) {
            $('#win').text("You won");
        } else {
            $('#win').text("You lost");
        }

        var cells = $('td');
        for(i of msg.pattern) {
            $(cells[i]).addClass('bg-info');
        }
    }
}

$(function() {
    $('table').on('click', (e) => {
        make_move($(e.target).data('i') - 1);
    });

    show_field();
});