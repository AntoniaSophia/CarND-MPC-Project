import matplotlib.pyplot as plt
import csv
import math

with open('../lake_track_waypoints.csv') as csvfile:
  linereader = csv.reader(csvfile, delimiter=',')
  i = 0
  for row in linereader:
    if i > 0:
      xValue = float(row[0])
      yValue = float(row[1].replace(';', ''))
      plt.plot(xValue, yValue, 'ro')

      psi = 4.12
      xValue_rotate = xValue * math.cos(psi) - yValue * math.sin(psi)
      yValue_rotate = xValue * math.sin(psi) + yValue * math.cos(psi)
      plt.plot(xValue_rotate, yValue_rotate, 'go')

    i += 1



plt.show()