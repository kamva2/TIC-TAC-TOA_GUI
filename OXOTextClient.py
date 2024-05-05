from GameClient import *

class OXOTextClient(GameClient):

    def __init__(self):
        GameClient.__init__(self)
        self.board = [' '] * BOARD_SIZE
        self.shape = None
        
    def clear_board(self):
        self.board = [' '] * BOARD_SIZE
        
    def input_server(self):
        return input('enter server:')
     
    def input_move(self):
        return input('enter move(0-8):')
     
    def input_play_again(self):
        return input('play again(y/n):')

    def display_board(self):
        # implement this method

        print(f" {self.board[0]} | {self.board[1]} | {self.board[2]} ")
        print("---+---+---")
        print(f" {self.board[3]} | {self.board[4]} | {self.board[5]} ")
        print("---+---+---")
        print(f" {self.board[6]} | {self.board[7]} | {self.board[8]} ")

        return 

    def handle_message(self,msg):
        # implement this method
        msg = msg.split(',')
        if msg[0] == 'new game':
            print(msg[0])
            
        elif msg[0] == 'your move':
            print(msg[0])
            self.display_board()
            move = self.input_move()
            self.send_message(move)

        elif msg[0] == 'opponents move':
            
            print(msg[0])

        elif msg[0] == 'valid move': 
            position = int(msg[2])
            shape = msg[1]
            self.board[position] = shape
            print(msg[0])

        elif msg[0] == 'invalid move':
            print(msg[0],'Enter a new move')
            move = self.input_move()
            self.send_message(move)

        elif msg[0] == 'game over':
            result = msg[1]
            print(msg[0],'\n',result,'Won the game')
            self.display_board()
            play_again = self.input_play_again().lower()

            if play_again == 'y':
                self.clear_board()
                self.display_board()
                self.send_message('y')
                if msg[0] == 'your move':
                    self.send_message(self.input_move())
            else:
                self.send_message('n')
                print("exit game")
    
                return
        pass
        
    
    def play_loop(self):
        while True:
            msg = self.receive_message()
            if len(msg): self.handle_message(msg)
            else: break
            
def main():
    otc = OXOTextClient()
    while True:
        try:
            otc.connect_to_server(otc.input_server())
            break
        except:
            print('Error connecting to server!')
    otc.play_loop()
    input('Press click to exit.')
        
main()