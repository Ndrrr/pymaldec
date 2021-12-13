import os
import subprocess
import shutil
import pyinstxtractor
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

cmd=input("Choose \"Compile\" or \"Decompile\":\n")
a,b=input("Enter source and destination files paths:\n").split()
if cmd=="Compile":
  compile(a,b)
elif cmd=="Decompile":
  decompile(a,b)
else:
  print("Wrong command")