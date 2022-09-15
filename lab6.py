from tkinter import filedialog as fd
import pickle
import linecache

text = []
file_name = fd.askopenfilename()
file = open(file_name, 'r')
l=(sum(1 for _ in file))
print(l)
lines = file.readlines()
file.seek(0)
file_name2 = fd.askopenfilename()
file2 = open(file_name2,"w")
for i in range (l):
    s=file.readline()
    str(s)
    s=s[::-1]
    print(''.join(s).strip('\n'))
    file2.write(s+'\n')
file2.close
