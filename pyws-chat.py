#!/usr/bin/env python

import asyncio
import websockets
import threading
#import tkinter as tk
#import select
from queue import *
from tkinter import *
import webbrowser
chat_messages=Queue() 
async def asrecvr(websocket):
    while True:
        await asyncio.sleep(1)
        print(await websocket.recv())
async def astrxmt(websocket):
    while True:
        await asyncio.sleep(1)
        if chat_messages.qsize():
                try:
                    await websocket.send(chat_messages.queue.pop())
                except: 
                    pass
async def asgui():
    thread=threading.Thread(target=GUI_pt)
    thread.start()
async def main(loop, name):
    uri = "ws://we6jbobbsdotorg.duckdns.org:16180"
    async with websockets.connect(uri) as websocket:
        await websocket.send('{\n"type": "auth",\n"name": "' + name + '"\n}')
        await websocket.send('{\n"type": "post-message",\n"message": "Good morning"\n}')
        await asyncio.gather(asrecvr(websocket), astrxmt(websocket))
        await asgui() 
#def Start_GUI_pt():
#    GUI_pt()
def GUI_pt():
    tk=Tk()
    tk.title('Hello')
    TextArea = Text()
    ScrollBar = Scrollbar(tk)
    ScrollBar.config(command=TextArea.yview)
    TextArea.config(yscrollcommand=ScrollBar.set)
    ScrollBar.pack(side=RIGHT, fill=Y)
    TextArea.pack(expand=YES, fill=BOTH)
    TextArea.insert('1.0', '{\n"type": "post-message",\n"message": "Good morning!"\n}')
    B = Button(tk,text='Submit',command= lambda: post_messagebtn(str(TextArea.get('1.0', 'end'))))
    B.pack()
    H = Button(tk,text='Help',command=helpcmd)
    H.pack()
    tk.mainloop()
def post_messagebtn(TextArea):
    chat_messages.put(str(TextArea))
def helpcmd():
    webbrowser.open("http://pyws-chat.wikidot.com")
def start_receive():
    GUI_pt()    
name = input("Enter your name: ")
th=threading.Thread(target=start_receive)
th.start()
loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop, name))
loop.close()
GUI_pt()

