import numpy as np
import matplotlib
matplotlib.use('QT5Agg')
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def gauss(x, H, A, x0, sigma):
    return H + A * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))

def gauss_fit(x, y):
    mean = sum(x * y) / sum(y)
    sigma = np.sqrt(sum(y * (x - mean) ** 2) / sum(y))
    popt, pcov = curve_fit(gauss, x, y, p0=[min(y), max(y), mean, sigma])
    return popt

def fwhm(sigma):
    return 2.3548 * sigma

#data = np.loadtxt("/Users/alexl/OneDrive/Documents/Uni/Master/Praktikum/WK/NA22_GE_kalibrierung_5min.txt", delimiter=';')
data = np.loadtxt("../Daten/Ba133_SZin_kalibirierung_3min.txt", delimiter=';')
#data = np.loadtxt("/Users/alexl/OneDrive/Documents/Uni/Master/Praktikum/WK/Ba133_Ge_kalibirierung_4min.txt", delimiter=';')
#data = np.loadtxt("/Users/alexl/OneDrive/Documents/Uni/Master/Praktikum/WK/Na22_(-33, 10, 7)_60min.txt", delimiter=';')

data = data[data[:,0] == 1.0]
binN = int(np.max(data[:,2]))

# %%
print(binN)
# %%

x = data[:,1]
y = data[:,2]

n, bins, patches = plt.hist(y, bins=binN, range=[13, 700])

"""
# First Peak
print("Peak 1")
y_fit = n[60:80]
x_fit = bins[60:80]
H1, A1, x0_1, sigma1 = gauss_fit(x_fit, y_fit)
print("mean =", int(round(x0_1)), "variance =", sigma1)
print("FWHM =", int(round(fwhm(sigma1))))

# Second Peak
print("Peak 2")
y_fit2 = n[290:307]
x_fit2 = bins[290:307]
H2, A2, x0_2, sigma2 = gauss_fit(x_fit2, y_fit2)
print("mean =", int(round(x0_2)), "variance =",sigma2)
print("FWHM =", int(round(fwhm(sigma2))))

# Third Peak
print("Peak 3")
y_fit3 = n[343:364]
x_fit3 = bins[343:364]
H3, A3, x0_3, sigma3 = gauss_fit(x_fit3, y_fit3)
print("mean =", int(round(x0_3)), "variance =",sigma3)
print("FWHM =", int(round(fwhm(sigma3))))

# Plots

plt.plot(x_fit, y_fit, color="r")
plt.plot(x_fit2, y_fit2, color="r")
plt.plot(x_fit3, y_fit3, color="r")
"""

plt.xlabel('Kanal', fontsize=14)
plt.ylabel('Ereignisse', fontsize=14)
#plt.yscale('log')
plt.grid(True)
plt.show()
