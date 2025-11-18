from PySide6.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QWidget, 
    QPushButton,
    QVBoxLayout,
    QGridLayout,
    QMessageBox
)
from PySide6.QtGui import QFont
import sys


class TicTacToeboard(QWidget):
    """井字棋棋盘

    :param QWidget: PySide6 基础窗口
    """
    def __init__(self):
        """构造函数"""
        
        super().__init__()

        # 设置 最小窗口为 300x300
        self.setMinimumSize(300, 300)

        # 垂直布局
        self.layouty = QVBoxLayout()

        # 网格布局
        self.gridy = QGridLayout()

        # 垂直布局里添加 网格布局
        self.layouty.addLayout(self.gridy)

        # 初始化 按钮、面板、当前玩家、游戏状态
        self.buttons = []
        self.board = [''] * 9
        self.current_player = 'X'
        self.game_over = False

        # 创建按钮
        self.make_buttons()
        # 重置按钮
        self.make_reset_button()

        # 控件使用 垂直布局
        self.setLayout(self.layouty)

    def make_buttons(self):
        """创建按钮"""

        for i in range(9):
            # 创建 文本为空的 按钮 -> 9个空按钮
            btn = QPushButton("")

            # 固定 按钮大小
            btn.setFixedSize(80, 80)

            # 设置按钮字体
            btn.setFont(QFont("Arial", 24))

            # 将名为index 的对象 值 设置为 i
            btn.setProperty('index', i)

            # 当按钮点击的时候 连接 对应的 槽函数
            btn.clicked.connect(self.when_button_is_clicked)

            # 将按钮添加到 处理化的按钮列表里
            self.buttons.append(btn)

            # 3 行 3列
            row = i // 3
            col = i % 3
            
            # 网格布局 添加 三个控件
            self.gridy.addWidget(btn, row, col)

    def make_reset_button(self):
        """重置按钮"""

        # 实例化 重置按钮
        self.reset_button = QPushButton("重置")

        # 重置按钮点击后 连接 清理槽函数
        self.reset_button.clicked.connect(self.clear_everything)

        # 在 垂直布局里 添加 重置按钮
        self.layouty.addWidget(self.reset_button)

    def when_button_is_clicked(self):
        """当点击按钮触发"""
        
        # 游戏结束 返回None
        if self.game_over:
            return
        
        # https://doc.qt.io/qtforpython-6/PySide6/QtCore/QObject.html#PySide6.QtCore.QObject.sender
        # 如果在被信号激活的槽中调用，返回发送信号对象的指针;否则返回 None。指针仅在执行从该对象线程上下文调用该函数的时隙时有效。

        # 返回按钮
        btn = self.sender()

        # 根据对象 的name 返回 对应的值 value
        index = btn.property('index')

        # 位置 被沾满 返回空
        if self.is_spot_taken(index):
            return
        
        # 在按钮上放入 标志 玩家
        self.put_mark_on_button(btn)

        # 传入 对应面板 的位置
        self.board[index] = self.current_player


        # 判断某人胜利
        if self.did_someone_win():

            # 游戏结束
            self.game_over = True

            # 显示赢家的信息 X/Y
            self.show_winner_message()

            return
        
        # 如果面板 满了 游戏结束 和局
        if self.is_board_full():
            self.game_over = True
            self.show_tie_message()
            return
        
        # 选择玩家 
        self.switch_player()

    def is_spot_taken(self, idx):
        """位置是否为空"""
        return self.board[idx] != ''

    def put_mark_on_button(self, btn:QPushButton):
        """放入标志

        :param btn: 面板中的 按钮
        """
        btn.setText(self.current_player)

        # 放入后不可用
        btn.setEnabled(False)


    def did_someone_win(self):
        """判断是否有人胜利"""

        # 全局 面板 设置为局部变量 B
        b = self.board


        # 9*9 二维列表       
        grid = [
            [b[0], b[1], b[2]],
            [b[3], b[4], b[5]],
            [b[6], b[7], b[8]]
        ]

        ## 行相等
        # 遍历行
        for row in grid:
            # 不为空 且相等
            if (row[0] != "" )and (row[0] == row[1] == row[2]):
                # 胜利者 就是 row0
                self.winner = row[0]
                return True

        ## 列相等
        # 便利列
        for c in range(3):
            # 不为空 且相等
            if grid[0][c] != "" and grid[0][c] == grid[1][c] == grid[2][c]:
                self.winner = grid[0][c]
                return True

        ## 斜线相等
        if grid[1][1] != "" and (
            grid[0][0] == grid[1][1] == grid[2][2] or
            grid[0][2] == grid[1][1] == grid[2][0]
        ):
            self.winner = grid[1][1]
            return True

        # 不满足则 对局还没有结束
        return False


    def show_winner_message(self):
        """显示胜利者信息"""
        QMessageBox.information(self, "游戏结束", f"{self.winner} 获胜!")

    def is_board_full(self):
        """面板是否占满"""
        
        # all 函数 判断 可迭代对象的 每个值 对应的布尔值 => 如果都为True 则返回True => 有为False 的则返回 False
        # 如果可迭代对象是空的 返回 True
        return all(cell for cell in self.board)  # 推倒式

    def show_tie_message(self):
        """显示和局信息"""
        QMessageBox.information(self, "游戏结束", "和局")

    def switch_player(self):
        """选择玩家"""
        # 其实是自动切换玩家
        if self.current_player == 'X':
            self.current_player = 'O'
        else:
            self.current_player = 'X'

    def clear_everything(self):
        """清空面板"""
        self.board = [''] * 9
        self.current_player = 'X'
        self.game_over = False
        for btn in self.buttons:
            btn.setText('')
            btn.setEnabled(True)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置窗口标题
        self.setWindowTitle("井字游戏")

        # 固定窗口大小
        self.setMaximumSize(400, 400)
        self.setMinimumSize(400, 400)

        # 中心控件
        container = QWidget()

        # 中心控件使用垂直布局 
        self.vlayout = QVBoxLayout()
        container.setLayout(self.vlayout)
        self.setCentralWidget(container)

        # 创建按钮 
        self.button = QPushButton("开始游戏")

        # 按钮点击 调用开始游戏
        self.button.clicked.connect(self.start_game) 

        # 添加按钮 到 控件
        self.vlayout.addWidget(self.button)

        # 清空面板
        self.board = None

    def start_game(self):
        """开始游戏"""  
        
        # 没有面板则创建面板
        if not self.board:

            # 实例化井字棋棋盘
            self.board = TicTacToeboard()

            # 添加面板到中心控件中
            self.vlayout.addWidget(self.board)


if __name__ == "__main__":
        
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # 设置按钮支持
    app.setStyleSheet('QMessageBox QPushButton[text="&OK"] {qproperty-text: "是";}')

    app.exec()