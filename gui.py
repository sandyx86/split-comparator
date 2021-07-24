import tkinter as tk
import xmlreader as xm


c1 = 0
c2 = 1
mid = xm.splCompare(c1, c2)


window = tk.Tk()
gridFrame = tk.Frame(master=window, relief=tk.SUNKEN, borderwidth=1)
nameFrame = tk.Frame(master=gridFrame)
leftFrame = tk.Frame(master=gridFrame)
midFrame = tk.Frame(master=gridFrame)
rightFrame = tk.Frame(master=gridFrame)

gridFrame.grid(row=1)

g = globals()
i=0
for i in range(len(xm._name)):
    g['lblName_{0}'.format(i)] = tk.Label(master=nameFrame, text=xm._name[i])
    g['lblLeft_{0}'.format(i)] = tk.Label(master=leftFrame, text=xm.splSeconds(xm._split[c1 + (i * len(xm._name))]))
    g['lblMid_{0}'.format(i)] = tk.Label(master=midFrame, text=mid[i])
    g['lblRight_{0}'.format(i)] = tk.Label(master=rightFrame, text=xm.splSeconds(xm._split[c2 + (i * len(xm._name))]))

i=0
for i in range(len(xm._name)):
    g['lblName_{0}'.format(i)].pack()
    g['lblLeft_{0}'.format(i)].pack()
    g['lblMid_{0}'.format(i)].pack()
    g['lblRight_{0}'.format(i)].pack()

nameFrame.pack(side='left')
leftFrame.pack(side='left')

rightFrame.pack(side='right')
midFrame.pack(side='right')

window.mainloop()