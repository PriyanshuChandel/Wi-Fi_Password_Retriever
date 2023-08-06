from tkinter import Tk, Frame, Label, Entry, Button, StringVar, OptionMenu, filedialog, Toplevel 
from tkinter.ttk import Combobox
from os.path import join, dirname  
from subprocess import Popen, PIPE, STDOUT  
from re import findall 
from threading import Thread 

def hasMultipleSpaces(input_string):
    spaceCount = input_string.count(' ')
    return spaceCount >= 1

class WiFiApp:
    iconFile = join(dirname(__file__), 'wifi-icon.ico')
    aboutIcon = join(dirname(__file__), 'info.ico')

    def __init__(self):
        self.ssidList = ['Select SSID']
        self.window = Tk()
        self.window.config(bg='light grey')
        self.window.title('Wi-Fi Retriever v1.0')
        self.window.geometry('230x165')
        self.window.iconbitmap(self.iconFile)
        self.window.resizable(False, False)
        self.mainLabel = Label(self.window, text='WiFi Password Retriever', font=('Arial', 12, 'bold'),
                               fg='blue', bg='light grey')
        self.mainLabel.place(x=18, y=5)
        self.ssidVar = StringVar()
        self.ssidDropDown = Combobox(self.window, textvariable=self.ssidVar, state='readonly')
        self.ssidDropDown.place(x=38, y=30)

        self.submitBtn = Button(self.window, text='Submit', font=(None, 10, 'bold'),
                                command=self.wifiPasswordFinder, bg='light grey', state='disabled')
        self.submitBtn.place(x=85, y=60)
        self.aboutLabel = Label(self.window, text="About", bg='light grey', fg="blue", cursor="hand2")
        self.aboutLabel.place(x=190, y=73)
        self.aboutLabel.bind("<Button-1>", lambda event: self.aboutWindow())
        self.statusFrame = Frame(self.window, bg="white", bd=20, width=220, height=60, cursor="target").place(x=4, y=95)
        self.messageLabel = Label(self.statusFrame, text='Status:', font=(None, 9, 'bold'), bg='white')
        self.messageLabel.place(x=4, y=95)

        self.messageText = Label(self.window, font=(None, 8, 'bold'), bg='white', wraplength=220, justify='left')
        self.messageText.place(x=4, y=110)

    def wifiPasswordFinder(self):
        ssidContainsSpace = hasMultipleSpaces(self.ssidVar.get())
        if ssidContainsSpace:
            finderCommand = f'netsh wlan show profile "{self.ssidVar.get()}" key=clear'
        else:
            finderCommand = f'netsh wlan show profile {self.ssidVar.get()} key=clear'

        def inner():
            try:
                sp1 = Popen(finderCommand, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
                key = findall('\s*Key Content\s*:\s*.*', sp1.stdout.read().decode())[0].strip().split(': ')[1]
                self.messageText.config(text=f'Password for select SSID is "{key}"')
            except Exception as E:
                self.messageText.config(text='ERROR, try again!')
        threadKillProcess = Thread(target=inner)
        threadKillProcess.start()

    def aboutWindow(self):
        aboutWin = Toplevel(self.window)
        aboutWin.grab_set()
        aboutWin.geometry('285x90')
        aboutWin.resizable(False, False)
        aboutWin.title('About')
        aboutWin.iconbitmap(self.aboutIcon)
        aboutWinLabel = Label(aboutWin, text=f'Version - 1.1\nDeveloped by Priyanshu\nFor any improvement please '
                                             f'reach on below email\nEmail : priyanshu.kumar@alstomgroup.com\nMobile : '
                                             f'+91-8285775109', font=('Helvetica', 9)).place(x=1, y=6)

    def enableSubmitBtn(self, *args):
        self.messageText.config(text='')
        if self.ssidVar.get() in self.ssidList[1:]:
            self.submitBtn.config(state='normal', bg='green')
        else:
            self.submitBtn.config(state='disabled', bg='light grey')

    def runGUI(self):
        command = 'netsh wlan show profile'
        sp = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)

        for ssidText in findall('\s*All User Profile\s*:\s*.*', sp.stdout.read().decode()):
            ssid = ssidText.split(":")[1].strip()
            self.ssidList.append(ssid)
        self.ssidDropDown.config(values=self.ssidList)
        self.ssidDropDown.bind("<<ComboboxSelected>>", self.enableSubmitBtn)
        self.ssidDropDown.set(self.ssidList[0])
        self.window.mainloop()


if __name__ == '__main__':
    killApp = WiFiApp()
    killApp.runGUI()
