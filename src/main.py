from wrapper import *

import tkinter as tk
from tkinter import ttk
import sv_ttk

import threading

def SetConfig(uregion,ushard):
        uconfig = f"""
        region: {uregion}
        shard: {ushard}
        """

        if not os.path.exists(os.getenv("LOCALAPPDATA")+"\PreGame"):
            os.makedirs(os.getenv("LOCALAPPDATA")+"\PreGame")
        else:
            with open(os.getenv("LOCALAPPDATA")+"\PreGame\config.yaml", "w") as f:
                f.write(uconfig)

if not os.path.exists(os.getenv("LOCALAPPDATA")+"\PreGame\config.yaml"):
    SetConfig("ap","ap")

# Create Tk Window
window = tk.Tk()
window.geometry("200x250")
window.title("")

notebook = ttk.Notebook(window)
notebook.pack(fill="both", expand=True)

tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="Home")

l5 = ttk.Label(tab1,font=('Helvetica', 12, 'bold'), text="PreGame")
l5.pack(pady=10)

# Game Dodge
b2 = ttk.Button(tab1, text="Dodge", command=lambda: threading.Thread(target=Match.Dodge(Get.PreMatchID()),daemon=True).start(), width=15)
b2.pack(pady=10, padx=10, ipadx=10)

# Instalock
l3 = ttk.Label(tab1,font=('Helvetica', 12, 'bold'), text="Instalock")
l3.pack(pady=10)

dv1 = tk.StringVar()
dagents = Get.AgentLUT()
d1 = ttk.OptionMenu(tab1, dv1, "Select Agent", *dagents,)
d1.config(width=15)
d1.pack()

def Instalock(AgentID):
    Match.AgentLock(Get.PreMatchID(), AgentID)

b3 = ttk.Button(tab1, text="set", command=lambda: threading.Thread(target=Instalock(dagents[dv1.get()]),daemon=True).start(), width=15)
b3.pack(pady=10, padx=10, ipadx=10)

### SETTINGS ###

tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="Settings")

l5 = ttk.Label(tab2,font=('Helvetica', 12, 'bold'), text="Region")
l5.pack(pady=10)

dv2 = tk.StringVar()
Regions = ["ap","ap","na","kr","br","eu","latam"]
d2 = ttk.OptionMenu(tab2, dv2, *Regions,)
d2.config(width=15)
d2.pack()

l6 = ttk.Label(tab2,font=('Helvetica', 12, 'bold'), text="Shard")
l6.pack(pady=10)

dv3 = tk.StringVar()
Shards = ["ap","ap","na","kr","pbe","eu"]
d3 = ttk.OptionMenu(tab2, dv3, *Shards,)
d3.config(width=15)
d3.pack()

b7 = ttk.Button(tab2, text="Set Config", command=lambda: threading.Thread(target=SetConfig(dv2.get(),dv3.get()),daemon=True).start(), width=15)
b7.pack(pady=10, padx=10, ipadx=10)

sv_ttk.set_theme("dark")
window.mainloop()