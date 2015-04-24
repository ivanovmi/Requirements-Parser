file_ = open('req', 'r')

a=[]
for i in file_:
    a.append(i)
    if not i.strip():
        continue
    else:
        print i

print a