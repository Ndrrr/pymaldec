import os
import subprocess
import shutil
import pyinstxtractor
from tkinter import *
import tkinter.font
import tkinter as tk




def compile(path_from, path_to):
    try:
      path_from=os.path.expanduser(path_from)
      path_to=os.path.expanduser(path_to)

      #removing file name from path in order to get path for folder
      path_from_folder='/'.join(path_from.split('/')[0:-1]) 
      dist,build = 0,0
      if os.path.exists(path_from_folder+"/build/"):
        build=1
      if os.path.exists(path_from_folder+"/dist/"):
        dist=1
      if os.path.exists(path_from)==False:
        print("File doesn't exist. Exiting app.")
        return
      print("The path of source code: ", path_from)
      result=subprocess.run(["python3","-m","PyInstaller","--onefile",path_from],stderr=subprocess.DEVNULL)
      if result.returncode!=0:
        print("Compilation failed. Exiting app.")
        return
      full_file=path_from.split('/')[-1]
      filename=full_file.split('.')[0]
      extension=''.join(full_file.split('.')[1:])
      shutil.copy2(path_from_folder+"/dist/"+filename,path_to)
      print("File compiled successfully.")
      print("The path of compiled file: ",path_to)
      if build==1:
        shutil.rmtree(path_from_folder+"/build/"+filename)
      else:
        shutil.rmtree(path_from_folder+"/build/")
      if dist==1:
        os.remove(path_from_folder+"/dist/"+filename)
      else:
        shutil.rmtree(path_from_folder+"/dist/")
      os.remove(path_from_folder+"/"+filename+".spec")
    except OSError as e:
       print("Error: %s - %s." % (e.filename, e.strerror))

def decompile(path_from, path_to):
    try:
      path_from=os.path.expanduser(path_from)
      path_to=os.path.expanduser(path_to)
      path_from_folder='/'.join(path_from.split('/')[0:-1]) 
      if os.path.exists(path_from)==False:
        print("File doesn't exist. Exiting app.")
        return
      print("The path of source code: ", path_from)
      pyinstxtractor.main(path_from)
      full_file=path_from.split('/')[-1]
      filename=full_file.split('.')[0]
      extension=''.join(full_file.split('.')[1:])
      result=subprocess.run(["uncompyle6","-o",path_to,path_from_folder+"/"+full_file+"_extracted/"+filename+".pyc"],stdout=subprocess.DEVNULL)
      if result.returncode!=0:
        print("Decompilation failed. Exiting app.")
        return
      with open(path_to, 'r') as fin:
        data = fin.read().splitlines(True)
      with open(path_to, 'w') as fout:
        fout.writelines(data[1:])
      fin.close()
      fout.close()
      print("File decompiled successfully.")
      print("The path of decompiled file: ",path_to)
      shutil.rmtree(path_from_folder+"/"+full_file+"_extracted/")
    
    except OSError as e:
       print("Error: %s - %s." % (e.filename, e.strerror))

#cmd=input("Choose \"Compile\" or \"Decompile\":\n")
#a,b=input("Enter source and destination files paths:\n").split()
#if cmd=="Compile":
#  compile(a,b)
#elif cmd=="Decompile":
#  decompile(a,b)
#else:
#  print("Wrong command")
  
class App:
    def __init__(self, root):
        global path, path2,tmp
        root.configure(background='#3f51b5')
        root.title("Comp/Decomp")
        width = 400
        height = 280
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        ft = tk.font.Font(family='Roboto',size=10)
        heading = Label(root, text="probably does something",bg='#3f51b5',fg='white',font=ft)
        path = Label(root, text="Path_from", background='#3f51b5', fg='white',font=ft)
        path2 = Label(root, text="Path_to", background='#3f51b5',fg='white',font=ft)
        heading.grid(row=0, column=1)
        path.grid(row=1, column=0)
        path2.grid(row=2, column=0)
        path = Entry(root)
        path2 = Entry(root)
        path.grid(row=1, column=1,ipadx="100")
        path2.grid(row=2, column=1,ipadx="100")
        path.bind("<Return>", path2.focus_set())
  
        GButton_510=tk.Button(root)
        GButton_510["bg"] = "#757de8"
        GButton_510["font"] = ft
        GButton_510["fg"] = "Black"
        GButton_510.grid(row=9, column=1)
        GButton_510["justify"] = "center"
        GButton_510["text"] = "Compile"
        GButton_510.place(x=110, y=80, width=80, height=40)
        GButton_510["command"] = self.GButton_510_command

        GButton_015= Button(root)
        GButton_015["bg"] = "#ff7961"  
        GButton_015["font"] = ft
        GButton_015["fg"] = "Black"
        GButton_015.grid(row=10, column=2)
        GButton_015["justify"] = "center"
        GButton_015["text"] = "Decompile"
        GButton_015.place(x=20, y=80, width=80,height=40)
        GButton_015["command"] = self.GButton_015_command


    def GButton_510_command(self):
        compile(path.get(),path2.get())
        #tmp= Label(root, text="message")
        #tmp.place(x=20,y=150)
    def GButton_015_command(self):
        decompile(path.get(),path2.get())
        
       
        
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
