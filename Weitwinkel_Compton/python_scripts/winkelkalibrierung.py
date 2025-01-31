import numpy as np
import matplotlib
matplotlib.use('QT5Agg')
import matplotlib.pyplot as plt
from scipy.stats import linregress

prefix = "../Daten/"
names = np.array(["Na22_(-33, 10, 7)_60min.txt", "Na22_(-33, 4, 15)_30min.txt", "Na22_(-33, 6, 20)_30min.txt", "Na22_(-33, 9, 24)_30min.txt", "Na22_(-33, 20, 27)_30min.txt"])
data = []
for name in names:
    data.append(np.transpose(np.loadtxt(prefix + name, delimiter=';', skiprows=2)[:, 2:]))

# 0 - HPGermanium, 1 - Szintillator

# %%
# Data manipulation

channel_max = 700

for i in range(0, len(data)):
    data[i] = data[i][:, data[i][0] <= channel_max]
    data[i] = data[i][:, data[i][1] <= channel_max]

# Filter the linear area

### FILTER SETTINGS
data_filter_m = -357.0/544.0 # delta y / delta x
data_filter_n_low = 310.0
data_filter_n_high = 410.0
### END FILTER SETTINGS

filtered_data = [None] * len(data)

for i in range(0, len(data)):
    line_part = data[i][1] - (data_filter_m * data[i][0]) # y - m*x = n
    filter = np.logical_and(line_part > data_filter_n_low, line_part < data_filter_n_high)
    filtered_data[i] = data[i][:, filter]


# linear regression
reg_results = [None] * len(data)

for i in range(0, len(data)):
    reg_results[i] = linregress(filtered_data[i])

# find error

### ERROR FILTER SETTINGS
margin = 0.8   # fraction of the data points inside error boundaries
initial_n_shift = 50.0
max_error = 10e-5 # max. allowed difference from margin
### END ERROR FILTER SETTINGS

# assuming error boundaries are parallel to regression line and same distance from it.

n_shift_array = []

for i in range(0, len(data)):
    n_shift = initial_n_shift
    n_shift_shift = initial_n_shift
    error = np.inf
    line_part_err = filtered_data[i][1] - (reg_results[i].slope * filtered_data[i][0])

    while True:
        filter_err = np.logical_and(line_part_err > reg_results[i].intercept-n_shift, line_part_err < reg_results[i].intercept+n_shift)
        error = margin - (np.sum(filter_err) / len(filtered_data[i][0]))
        if (np.abs(error) <= max_error):
            n_shift_array.append(n_shift)
            break
        else:
            if np.sign(error) != np.sign(n_shift_shift):
                n_shift_shift *= -0.5
            n_shift += n_shift_shift

# %%
# Plot

u = int(np.ceil(np.sqrt(len(data))))   # Find subplot x and y amount
w = int(np.floor(np.sqrt(len(data))))
print(u,w)

fig, axes = plt.subplots(w, u)

for i in range(0, len(data)):
    x_idx = int(np.floor(i / u))
    y_idx = int(i % u)
    axes[x_idx][y_idx].hist2d(data[i][0], data[i][1], bins=channel_max)

plt.show()

# filtered data
fig, axes = plt.subplots(w, u)

for i in range(0, len(data)):
    x_idx = int(np.floor(i / u))
    y_idx = int(i % u)
    axes[x_idx][y_idx].hist2d(filtered_data[i][0], filtered_data[i][1], bins=channel_max)
    axes[x_idx][y_idx].plot([0, -(data_filter_n_low/data_filter_m)], [data_filter_n_low, 0], color = "plum", label = "filter lower bound")
    axes[x_idx][y_idx].plot([0, -(data_filter_n_high/data_filter_m)], [data_filter_n_high, 0], color = "thistle", label = "filter upper bound")
    axes[x_idx][y_idx].plot([0, -(reg_results[i].intercept / reg_results[i].slope)], [reg_results[i].intercept, 0], color = "greenyellow", label="linear fit")
    axes[x_idx][y_idx].plot([0, -((reg_results[i].intercept+n_shift_array[i]) / reg_results[i].slope)], [(reg_results[i].intercept+n_shift_array[i]), 0], color = "lime", label="error range")
    axes[x_idx][y_idx].plot([0, -((reg_results[i].intercept-n_shift_array[i]) / reg_results[i].slope)], [(reg_results[i].intercept-n_shift_array[i]), 0], color = "lime")
    axes[x_idx][y_idx].title.set_text(r"$x = 0$ intercept: ${inter:.3f}$, error: ${err:.3f}$".format(inter = reg_results[i].intercept, err = 2.0*n_shift_array[i]))
    axes[x_idx][y_idx].legend(loc = "best")

plt.show()
