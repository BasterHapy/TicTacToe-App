from PySide6.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QWidget, 
    QPushButton,
    QVBoxLayout,
    QGridLayout,
    QMessageBox
)
from PySide6.QtGui import QPainter, QFont
from PySide6.QtCore import Qt
import sys


class TicTacToeboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(300, 300)
        self.layouty = QVBoxLayout()
        self.gridy = QGridLayout()
        self.layouty.addLayout(self.gridy)
        self.buttons = []
        self.board = [''] * 9
        self.current_player = 'X'
        self.game_over = False
        self.make_buttons()
        self.make_reset_button()
        self.setLayout(self.layouty)

    def make_buttons(self):
        for i in range(9):
            btn = QPushButton("")
            btn.setFixedSize(80, 80)
            btn.setFont(QFont("Arial", 24))
            btn.setProperty('index', i)
            btn.clicked.connect(self.when_button_is_clicked)
            self.buttons.append(btn)
            row = i // 3
            col = i % 3
            self.gridy.addWidget(btn, row, col)

    def make_reset_button(self):
        self.reset_button = QPushButton("Restart")
        self.reset_button.clicked.connect(self.clear_everything)
        self.layouty.addWidget(self.reset_button)

    def when_button_is_clicked(self):
        if self.game_over:
            return
        btn = self.sender()
        index = btn.property('index')
        if self.is_spot_taken(index):
            return
        self.put_mark_on_button(btn)
        self.board[index] = self.current_player
        if self.did_someone_win():
            self.game_over = True
            self.show_winner_message()
            return
        if self.is_board_full():
            self.game_over = True
            self.show_tie_message()
            return
        self.switch_player()

    def is_spot_taken(self, idx):
        return self.board[idx] != ''

    def put_mark_on_button(self, btn):
        btn.setText(self.current_player)
        btn.setEnabled(False)

    def did_someone_win(self):
        b = self.board

       
        grid = [
            [b[0], b[1], b[2]],
            [b[3], b[4], b[5]],
            [b[6], b[7], b[8]]
        ]

      
        for row in grid:
            if row[0] != "" and row[0] == row[1] == row[2]:
                self.winner = row[0]
                return True

       
        for c in range(3):
            if grid[0][c] != "" and grid[0][c] == grid[1][c] == grid[2][c]:
                self.winner = grid[0][c]
                return True

        
        if grid[1][1] != "" and (
            grid[0][0] == grid[1][1] == grid[2][2] or
            grid[0][2] == grid[1][1] == grid[2][0]
        ):
            self.winner = grid[1][1]
            return True

        return False


    def show_winner_message(self):
        QMessageBox.information(self, "Game Over", f"{self.winner} wins!")

    def is_board_full(self):
        return all(cell != '' for cell in self.board)

    def show_tie_message(self):
        QMessageBox.information(self, "Game Over", "It's a tie!")

    def switch_player(self):
        if self.current_player == 'X':
            self.current_player = 'O'
        else:
            self.current_player = 'X'

    def clear_everything(self):
        self.board = [''] * 9
        self.current_player = 'X'
        self.game_over = False
        for btn in self.buttons:
            btn.setText('')
            btn.setEnabled(True)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tic Tac Toe")
        self.setMaximumSize(400, 400)
        self.setMinimumSize(400, 400)

        container = QWidget()
        self.vlayout = QVBoxLayout()
        container.setLayout(self.vlayout)
        self.setCentralWidget(container)

       
        self.button = QPushButton("Start Game")
        self.button.clicked.connect(self.start_game) 
        self.vlayout.addWidget(self.button)

        self.board = None

    def start_game(self):  
        if not self.board:
            self.board = TicTacToeboard()
            self.vlayout.addWidget(self.board)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()