import csv
import matplotlib.pyplot as plt
import sys

x = []
y = []
with open(str(sys.argv[1]),newline='\n')as csvfile:
	reader = csv.reader(csvfile,delimiter=';')
	for row in reader:
		x.append(float(row[0].replace(',','.')))
		y.append(float(row[1].replace(',','.')))

plt.plot(x,y,'o',markersize=2)
plt.xlim(0, 20)
plt.ylim(-5, 5)
plt.show()
