import matplotlib.pyplot as plt
import csv
import math

def func(x):
  a = 0.744287
  b = 0.00214534
  c = 0.00135139
  d = -9.85153e-07

  return a + b*x + c*x*x + d*x*x*x


with open('../lake_track_waypoints.csv') as csvfile:
  linereader = csv.reader(csvfile, delimiter=',')
  i = 0

  posx = -40.62
  posy = 108.74
  plt.plot(posx, posy, 'go')
  for row in linereader:
    if i > 0:
      xValue = float(row[0])
      yValue = float(row[1].replace(';', ''))
      plt.plot(xValue, yValue, 'ro')

      psi = -3.73

      xValue_rotate = (xValue-posx) * math.cos(psi) - (yValue-posy) * math.sin(psi) 
      yValue_rotate = (xValue-posx) * math.sin(psi) + (yValue-posy) * math.cos(psi)

      print(xValue_rotate, xValue_rotate)

      plt.plot(xValue_rotate, yValue_rotate, 'go')

      yValue_interpolated = func(xValue_rotate)
      
      if (yValue_interpolated < 500):
        plt.plot(xValue_rotate,yValue_interpolated , 'yo')

    i += 1

  
plt.show()