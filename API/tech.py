f = open('./techCrunch.txt','r')
text = f.read()
initial = text.index("src")
temp = text[initial:text.index("alt",initial)]
print temp[temp.index("http"):len(temp)-2]
