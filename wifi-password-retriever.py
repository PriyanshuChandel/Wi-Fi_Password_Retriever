from tkinter import Tk, Frame, Label, Entry, Button, StringVar, OptionMenu, filedialog # To create GUI
from tkinter.ttk import Combobox
from os.path import join, dirname  # TO manage the files and path
from subprocess import Popen, PIPE, STDOUT  # To execute the commands
from re import findall  # To manage the regular expression
from threading import Thread  # To use multiple process threads

Icon_File = join(dirname(__file__), 'wifi-icon.ico')

window = Tk()
window.config(bg='grey')
window.title('Wi-Fi Password Retriever')
window.minsize(width=230, height=165)
window.maxsize(width=230, height=165)
window.iconbitmap(Icon_File)
window.resizable(False, False)

def threading_main_btn_func():
    thread_btn = Thread(target=main_btn_func)
    thread_btn.start()

def main_btn_func():
    try:
        cmd = f'netsh wlan show profile {var.get()} key=clear'
        sp1 = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        key = findall('\s*Key Content\s*:\s*.*', sp1.stdout.read().decode())[0].strip().split(': ')[1]
        labl3.config(text=f'Password for select SSID is "{key}"')
    except Exception as E:
        labl3.config(text='No password available for this network')

labl1 = Label(window, text='Select SSID from saved wifi network', font=(None, 9, 'bold'), bg='grey').place(x=8, y=6)
btn1 = Button(window, text='Submit', font=(None, 10, 'bold'), command=threading_main_btn_func, bg='Green')
btn1.place(x=85, y=60)
frame2=Frame(window,bg = "white",bd=20,width=300,height=60,cursor = "target").place(x=2, y=95)
labl2 = Label(frame2, text='Status:', font=(None, 9, 'bold'), bg='white')
labl2.place(x=2, y=95)
labl3 = Label(window, font=(None, 8, 'bold'), bg='white', wraplength=220, justify='left')
labl3.place(x=2, y=110)
command = 'netsh wlan show profile'
sp = Popen(command, shell=True,stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
SSID_List = [item.split(":")[1].strip() for item in findall('\s*All User Profile\s*:\s*.*', sp.stdout.read().decode())]
var = StringVar()
box1 = Combobox(window, value=SSID_List,textvariable = var)
box1.place(x=38, y=30)
box1.bind()
window.mainloop()