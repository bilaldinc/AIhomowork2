import os
import shutil

files = [f for f in os.listdir('.') if os.path.isfile(f)]


files_with_values = []

for f in files:
    if '.csv' in f:
        f2 = open(f, 'r')
        first = f2.readlines()[0]
        f2.close()
        print(first)
        split = first.split(" ")[3]
        value = float(split)
        files_with_values.append((f,value))

sorted_by_second = sorted(files_with_values, key=lambda tup: tup[1],reverse=True)

if not os.path.exists("best10"):
    os.makedirs("best10")

for i in range(10):
    print(sorted_by_second[i][1])
    shutil.copy2(sorted_by_second[i][0], 'best10')

