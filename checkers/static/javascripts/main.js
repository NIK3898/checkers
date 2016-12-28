$(document).ready(function () {
  bind_events();
});

function bind_events() {
  var current_position = undefined;
  var destination = undefined;
  var $black_squares = $('tr:nth-child(odd) td:nth-child(even), tr:nth-child(even) td:nth-child(odd)');

  $black_squares.click(function () {
    if ($(this).find('.board__piece').length) {
      current_position = {
        x: $(this).data('x'),
        y: $(this).data('y')
      }
    } else {
      destination = {
        x: $(this).data('x'),
        y: $(this).data('y')
      }

      if (current_position === undefined) {
        alert('Choose a piece!')
      } else {
        var pieces = pieces_on_board();
        $.post('/move',
          {
            cur_x: current_position.x,
            cur_y: current_position.y,
            dst_x: destination.x,
            dst_y: destination.y,
            pieces: pieces,
            pieces_count: pieces.length,
            board_size: $('tr').length
          },
          function (data, status) {
            $('body').html(data);
            bind_events();
          }
        )
      }
    }
  });
}

function pieces_on_board() {
  var board_state = [];

  $('.board__piece').each(function () {
    var color;
    if ($(this).hasClass('board__piece--dark')) {
      color = 'DarkPiece';
    }

    if ($(this).hasClass('board__piece--light')) {
      color = 'LightPiece';
    }

    board_state.push({
      x: $(this).parent().data('x'),
      y: $(this).parent().data('y'),
      color: color,
      king: $(this).hasClass('board__piece--king')
    });
  });

  return board_state;
}
