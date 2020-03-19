import glob
import os
folder_path = os.getcwd() + '/EDFA_1STG' #Take the path to the folder
name_newfile = 'grouped-mask.txt' 

f_out = open(name_newfile, 'w')
big_string = ''

for filename in glob.glob(os.path.join(folder_path, '*.txt')): #Take every file in the folder and put into a big file.
  with open(filename, 'r') as f:
    text = f.read()
    big_string += text
f_out.write(big_string)    