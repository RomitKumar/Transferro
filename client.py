import socket
from tkinter import Tk,filedialog

def main():
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        port = 54321
        host = input('Enter host IP: ')
##        CONNECTION
        while True:
                try:
                        s.connect((host,port))
                        break
                except:
                        print('IP not available')
                        print('1.Check sender\'s IP')
                        print('2.Check if sender & receiver are on same network')
                        host = input('Enter host IP ')
                
        print('Connected to Sender')

        tmp = Tk()
        tmp.withdraw()
        
##        FILENAME
        filename = s.recv(8192).decode()
        print('filename received')
        s.send('ok'.encode())
        
##        FILESIZE
        filesize = int(s.recv(1024).decode())
        filesizekb = filesize//1024
        s.send('ok'.encode())
        
##        LOCATION CHOOSER
        f = filedialog.asksaveasfile(initialfile = filename,title = 'Select location to save file',mode='wb')
        
        progress = 0
        data = s.recv(8192)
        print('Receiving file..............') 
        while data:
                f.write(data)
                data = s.recv(8192)
                temp = f.tell()*100//filesize
                if temp != progress:
                        progress = temp
                        print(str(progress),'% Downloaded',' {} KB/{} KB'.format(f.tell()//1024,filesizekb),sep='',end='\r')

        print(str(progress),'% Downloaded',' {} KB/{} KB'.format(f.tell()//1024,filesizekb),sep = '')
        print('file received successfully')
        f.close()
        s.close()


if __name__ == '__main__':

        main()
