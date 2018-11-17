# -*- coding: UTF-8 -*-
import win32clipboard
import win32con
import re
import threading
from Tkinter import *
from tkFileDialog import askopenfilename
root = Tk()
root.title("copy clipboard link in txt file")
root.geometry("800x400")
S = Scrollbar(root)
T = Text(root, height=30, width=100)
S.pack(side=RIGHT, fill=Y)
T.pack(side=LEFT, fill=Y)
S.config(command=T.yview)
T.config(yscrollcommand=S.set)
def check(urls,f):#بررسی تکراری نبود آدرس در فایل
        datafile = file(f)
        found = False 
        for line in datafile:
            if str(urls) in line: 
                return True
        return False

def printit(f):
	threading.Timer(0.2, printit,[f]).start()#تایمر برای بررسی کلیپ بورد
	if win32clipboard.IsClipboardFormatAvailable(win32con.CF_TEXT):
		win32clipboard.OpenClipboard()
		data = win32clipboard.GetClipboardData()
		win32clipboard.CloseClipboard()
		url = data
		if url:
			urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url)#استخراج آدرس از کلیپ بورد
			for a in urls:
				if check(a,f)==False:
					if a:
						quote = str(a)+'\n'
						T.insert(END, quote)
						file = open(f, 'a+b')
						file.writelines(str(a)+'\n')#ذخیره آدرس در فایل
						file.close()
def openfile():
	filename = askopenfilename(filetypes=(('text files', 'txt'),))#باز کردن بخش انتخاب فایل
	if filename:
		printit(filename)
menubar = Menu(root)#منو بالایی
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="باز کردن", command=openfile)
filemenu.add_separator()
filemenu.add_command(label="خروج", command=root.quit)
menubar.add_cascade(label="فایل", menu=filemenu)
root.config(menu=menubar)
root.mainloop()
