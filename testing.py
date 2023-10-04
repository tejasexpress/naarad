with open('./ACCESS_TOKEN', 'r') as f:
    EMAIL = f.readline().split('"')[1]
    PASSWORD = f.readline().split('"')[1]
l=[]
l.append(EMAIL)
l.append(PASSWORD)
print(l)