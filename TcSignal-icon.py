
import matplotlib.pyplot as plt
from random import seed, random
from math import sin, pi

import numpy as np

# Set random seed for reproducibility
seed(42)

plt.figure(facecolor='#333333', figsize=(1, 1))

# Generate data
x = [i for i in range(1, 100)]
y = [sin(i/25*pi) + random()*1.5 for i in range(1, 100)]
y_smooth = [sum(y[i-5:i+6])/10 for i in range(5, 95)]

# Index for the point to fit
fit_point = 53

# Plot original data and smoothed line
plt.plot(x, y, color='#DCDCDC')  # Light gray signal
plt.plot(x[5:95], y_smooth, linewidth=3, color='#6895D2')  # Smoothed line

# Plot the fitted line
fit = np.poly1d(np.polyfit(x[fit_point-1:fit_point+1], y_smooth[fit_point-1-5:fit_point+1-5], 1))
plt.plot(x, fit(x), color="#F3B95F", linewidth=2)  # Fitted line

# Plot the fitted point
plt.scatter(x[fit_point], y_smooth[fit_point-5], s=50, color='#D04848', zorder=10)  # Fitted point

# Customize plot
plt.axis('off')  # Turn off the axis

plt.xlim(fit_point-20, fit_point+20)  # Zoom in on the fitted point
plt.ylim(-1, 2.5)  # Set y limits


plt.savefig("icon.svg")

# Show the plot
plt.show()
