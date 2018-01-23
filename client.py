import socket
from tkinter import Tk,filedialog

temp_file,temp_socket = None, None

def receiver():
        global temp_file,temp_socket
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        temp_socket = s
        port = 54321
        host = input('Enter Sender IP: ')
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
        s.send('ok'.encode())
        
##        FILESIZE
        filesize = int(s.recv(1024).decode())
        filesizekb = filesize//1024
        s.send('ok'.encode())
        
##        LOCATION CHOOSER
        f = filedialog.asksaveasfile(initialfile = filename,title = 'Select location to save file',mode='wb')
        try:
                f.tell()
        except AttributeError:
                print('Download Cancelled')
                return
        
        temp_file = f
        data = s.recv(8192)
        print('Receiving file..............') 
        while data:
                f.write(data)
                data = s.recv(8192)
                progress = f.tell()*100//filesize
                print(str(progress),'% Downloaded',' {} KB/{} KB'.format(f.tell()//1024,filesizekb),sep='',end='\r')

        print(str(progress),'% Downloaded',' {} KB/{} KB'.format(f.tell()//1024,filesizekb),sep = '')
        if f.tell()!=filesize:
                print('Download failed')
        else:
                print('file received successfully')
        f.close()
        s.close()

def main():
        try:
                receiver()
        except KeyboardInterrupt:
                print('\nDownload Interrupted')
                temp_socket.close()
                try:
                        temp_file.close()
                except:
                        pass


if __name__ == '__main__':
        main()
