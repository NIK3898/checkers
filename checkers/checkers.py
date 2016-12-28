from flask import Flask
from flask import render_template
from flask import request
from .game import *

app = Flask(__name__)

@app.route('/')
@app.route('/board/<int:board_size>')
def index(board_size=8):
    gameboard = Gameboard.build(board_size)
    board = gameboard.board
    return render_template('index.html', board=board)

@app.route('/move', methods=['POST'])
def move():
    if request.method == 'POST':
        gameboard = Gameboard(__prepare_board(request))

        current_position = {
            'x': int(request.form['cur_x']),
            'y': int(request.form['cur_y'])
        }
        destination = {
            'x': int(request.form['dst_x']),
            'y': int(request.form['dst_y'])
        }
        gameboard.move(current_position, destination)

        board = gameboard.board
        return render_template('_gameboard.html', board=board)

def __prepare_board(request):
    board_size = int(request.form['board_size'])
    pieces_count = int(request.form['pieces_count'])
    prepared_board = __generate_empty_board(board_size)

    for i in range(pieces_count):
        x = int(request.form['pieces['+str(i)+'][x]'])
        y = int(request.form['pieces['+str(i)+'][y]'])
        color = request.form['pieces['+str(i)+'][color]']
        king = request.form['pieces['+str(i)+'][king]'] == 'true'

        if color == 'DarkPiece':
            prepared_piece = DarkPiece()
        if color == 'LightPiece':
            prepared_piece = LightPiece()
        if king:
            prepared_piece.become_king()

        prepared_board[y][x] = prepared_piece

    return prepared_board

def __generate_empty_board(size):
    board = []

    for i in range(size):
        board.append([None]*size)

    return board
