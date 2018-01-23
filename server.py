import socket,subprocess
from tkinter import Tk,filedialog
from os.path import getsize

temp_file,temp_socket = None,None

def print_ip():
        try:
                x=subprocess.getoutput('hostname -I').split()[0]
        except:
                x=''

        if not x:
                print('No network detected')
                choice = input('Do you want to run it on localhost[y/n]: ')
                if choice in ['y','Y']:
                        print('Your IP is -- localhost')
                else:
                        return True
        elif x[0].isnumeric():
                print('your IP is -- ',x)
        else:
                x=subprocess.getoutput('ipconfig | findstr /C:"IPv4 Address"').split(': ')[-1]
                print('Your IP is',x)
        return False


def sender():
        global temp_file,temp_socket
        myclient = ''
        port = 54321

        if print_ip():
                return
        
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        temp_socket = s
        s.bind((myclient,port))
        s.listen(1)
        print('Listening started')

        tmp=Tk()
        tmp.withdraw()
        
        filepath = filedialog.askopenfilename(title='Choose file to send')
        filename = filepath.split('/')[-1]

        f = open(filepath,'rb')
        temp_file = f
        
        filesize = getsize(filepath)
        filesizekb = filesize//1024
        print('File size: ',filesizekb,'KB')
        
        c,addr = s.accept()
        print('Connected to',addr)
        
        c.send(filename.encode())
        c.recv(2)
        
        c.send(str(filesize).encode())
        c.recv(2)
        
        print('Sending file..............')
        f.seek(0)
        data = f.read(8192)
        while data:
                c.send(data)
                data = f.read(8192)
                progress = f.tell()*100//filesize
                print(str(progress),'% Uploaded',' {} KB/{} KB'.format(f.tell()//1024,filesizekb),sep='',end='\r')
        
        print(str(progress),'% Uploaded',' {} KB/{} KB'.format(f.tell()//1024,filesizekb),sep='')        
        f.close()
        s.close()
        print('File sent successfully')

def main():
        try:
                sender()
        except KeyboardInterrupt:
                print('\nUpload Interrupted')
                temp_file.close()
        except (ConnectionResetError, BrokenPipeError):
                print('Upload Failed') 
                temp_file.close()
        except AttributeError:
                print('Upload Cancelled')
        finally:
                temp_socket.close()


if __name__ == '__main__':
        main()
