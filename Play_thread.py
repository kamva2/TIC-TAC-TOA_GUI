# Playloop thread
# Kamva Poswa
# PSWKAM001
# 23 April 2024


from GameClient import *
from time import *
from PyQt5.QtCore import *


class Play_thread(QThread):
    
    updating_signal = pyqtSignal(str)
    
    def __init__(self,host= None):
        QThread.__init__(self)
        self.host = host
        self.messages = []
        
    def run(self):
        while True:
            sleep(0.25)
        
            msg = self.host.receive_message()
        
            if len(msg):
                self.messages.append(msg)
                self.updating_signal.emit(str(msg))
            else:
                break
            
    def get_messages(self):
        return self.messages
    
        