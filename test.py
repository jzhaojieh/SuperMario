s = 23
scores = ""
with open("/Users/joshuahuang/Desktop/112/TP/TP/score.txt", "r") as f:
    f.write(str(s) +"\n")

with open("/Users/joshuahuang/Desktop/112/TP/TP/score.txt", "r") as f:
  for line in f:
    scores+=(line)
print(scores)