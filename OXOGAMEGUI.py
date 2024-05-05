import sys
from GameClient import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from Play_thread import *

class OXOGameGui(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(250, 250, 400, 350)
        self.setWindowTitle('OXO GAME')
        self.setPalette(QPalette(QColor("green"))) 
        self.host = GameClient()
        
        # Create labels, buttons, and line edits
        title = QLabel('Welcome to the OXO-GAME')
        title.setStyleSheet("color: white;")
        label = QLabel('Connection To The Server:')
        label.setStyleSheet("color: white;")
        connect = QPushButton("Connect")
        connect.setStyleSheet("color: black;")
        disconnect = QPushButton("Disonnect")
        disconnect.setStyleSheet("color: black;")        
        Character = QLabel("Characters :")
        Character.setStyleSheet("color: white;")
        Character.setFont(QFont('Times', 12, 1000))
        Game = QLabel("Game :")
        Game.setStyleSheet("color: white;")
        Game.setFont(QFont('Times', 12, 1000))
        msg_from_server = QLabel("Messages from Server:")
        msg_from_server.setStyleSheet("color: white;")
        
        
        self.edit = QLineEdit(self)
        self.edit.setStyleSheet("color: black;")
        
        help = QPushButton("Help")
        help.setStyleSheet("color: black;")
        play = QPushButton("Play Again")
        play.setStyleSheet("color: black;")
        quit = QPushButton("Quit")
        quit.setStyleSheet("color: black;")
        
        
        title.setFont(QFont('Times', 12, 1000))
        label.setFont(QFont('Times',12,1000))
        msg_from_server.setFont(QFont('Times',12,1000))

        # Set up the main layout using a grid layout
        grid = QGridLayout()
        self.setLayout(grid)
        grid.addWidget(title, 0, 0)
        grid.addWidget(label, 1, 0)
        grid.addWidget(self.edit, 1, 1)
        grid.addWidget(connect, 1, 2)
        grid.addWidget(disconnect, 1, 3)
        grid.addWidget(Character,2,0)
        grid.addWidget(Game,2,1)
        grid.addWidget(help, 5, 0)
        grid.addWidget(quit, 5, 1)
        grid.addWidget(play, 5, 2)
        grid.addWidget(msg_from_server,2,3)
        
        # Create a layout for the character images (e.g., X and O)
        char_grid =  QGridLayout()
        grid.addLayout(char_grid, 3, 0, 2, 2) 
        
        x_image = QLabel()
        pixmap = QPixmap("cross.gif")
        x_image.setPixmap(pixmap)
        char_grid.addWidget(x_image,0,0)
        
        o_image = QLabel()
        pixmap = QPixmap("nought.gif")
        o_image.setPixmap(pixmap)
        char_grid.addWidget(o_image,1,0)        
        
        # Create an inner grid layout for image labels
        inner_grid = QGridLayout()
        grid.addLayout(inner_grid, 3, 1, 2, 2)  # Add inner grid layout to occupy the space of two columns
        
        # Create blank image buttons for the initial game board
        for i in range(3):
            for j in range(3):
                image_button = QPushButton()
                image_button.setStyleSheet("border: 0px")
                pixmap = QPixmap("blank.gif")
                image_button.setIcon(QIcon(pixmap))
                image_button.setIconSize(pixmap.rect().size())
                image_button.clicked.connect(lambda state, i=i, j=j: self.image_button_clicked(i, j))
                inner_grid.addWidget(image_button, i, j)      

        
        #Message from thr server grid
        self.message_grid = QTextEdit()
        grid.addWidget(self.message_grid,3,3,1,1)
        
        #creating a thread
        self.loop_thread = Play_thread(self.host)         

        # Handling buttons
        connect.clicked.connect(self.connect_clicked)
        disconnect.clicked.connect(self.disconnect_clicked)
        quit.clicked.connect(self.quit_clicked)
        play.clicked.connect(self.play_clicked)
        help.clicked.connect(self.help_clicked)
        
        self.loop_thread.updating_signal.connect(self.loop_slot)
        
        
    def connect_clicked(self):
        print("Connect has been clicked") 
        ip = self.edit.text().strip()
        self.host.connect_to_server(ip)
                
        self.loop_thread.start()
                
    def loop_slot(self,msg):
        self.message_grid.clear()
        
        messages = self.loop_thread.get_messages()
        for message in messages:
            self.message_grid.append(message)
            break
        
        

        
    def disconnect_clicked(self):
        print("Disconnect has been clicked") 
        self.edit.clear() 
        self.close()
           
    def quit_clicked(self):
        print("Quit has been clicked")
        
    def play_clicked(self):
        print("Play Again has been clicked")  
           
    def help_clicked(self):
        print("How to play?\nclicking on a clear box in the OXO game allows \na player to mark their position on the grid with \ntheir symbol, progressing towards the goal of getting \nthree symbols in a row.")
        
    def new_game(self):
        self.msg = ""
        print(self.msg)
    

def main():
    app = QApplication(sys.argv)
    widget = OXOGameGui()
    widget.show()
    sys.exit(app.exec_())    
    

main()
