import numpy as np
import sys

from scipy import stats
from scipy import signal

import matplotlib.pyplot as plt

def axis(n):
	if n == 1:
		return 'x'
	if n == 2:
		return 'y'
	if n == 3:
		return 'z'

data = np.loadtxt('acc_data.txt')
exp_data = np.loadtxt('acc_trials.txt', dtype='int')

fs = 500														# Velocidad de muestreo
window_size = int(fs * 0.1)										# 50 muestras
nsignals = data.shape[1]										# Numero de señales

trials = {}

for step in exp_data:
	for index in range(step[1], step[2], window_size):
		print(step[0], ' - ', index, ' - ', index + window_size - 1)

		if not step[0] in trials:
			trials[step[0]] = []

		trials[step[0]].append([index, index + window_size - 1])

mean_values = {}
std_values = {}
kurtosis_values = {}
skewness_values = {}
psd_values = {}
psd_freqs = []

for mov in trials:
	#print('Movimiento', mov)

	
	mean_values[mov] = []
	std_values[mov] = []
	kurtosis_values[mov] = []
	skewness_values[mov] = []
	psd_values[mov] = []

	for win in trials[mov]:
		#print('   Window', win)

		mean_v = []
		std_v = []
		kurtosis_v = []
		skewness_v = []
		psd_v = []
		for s in range(nsignals):
			sig = data[win[0] : win[1] + 1, s]
			mean_v.append(np.average(sig))
			std_v.append(np.std(sig))
			kurtosis_v.append(stats.kurtosis(sig))
			skewness_v.append(stats.skew(sig))

			freqs, psd = signal.periodogram(sig, fs, 'hamming', scaling='spectrum')
			psd_v.append(psd)
			psd_freqs = freqs
			#print(psd_freqs)

		mean_values[mov].append(mean_v)
		std_values[mov].append(std_v)
		kurtosis_values[mov].append(kurtosis_v)
		skewness_values[mov].append(skewness_v)
		psd_values[mov].append(psd_v)

mean_mean_values = []
mean_std_values = []
mean_kurtosis_values = []
mean_skew_values = []
mean_psd_values = []
moves = []
for mov in mean_values:
	print('Movimiento: ', mov)
	moves.append(str(mov))
	values = np.array(mean_values[mov])
	mean_mean_values.append(values.mean(0))

moves = []
for mov in std_values:
	print('Movimiento: ', mov)
	moves.append(str(mov))
	values = np.array(std_values[mov])
	mean_std_values.append(values.mean(0))

moves = []
for mov in kurtosis_values:
	print('Movimiento: ', mov)
	moves.append(str(mov))
	values = np.array(kurtosis_values[mov])
	mean_kurtosis_values.append(values.mean(0))

moves = []
for mov in skewness_values:
	print('Movimiento: ', mov)
	moves.append(str(mov))
	values = np.array(skewness_values[mov])
	mean_skew_values.append(values.mean(0))

moves = []
for mov in psd_values:
	print('Movimiento: ', mov)
	moves.append(str(mov))
	values = np.array(psd_values[mov])
	mean_psd_v = []
	for i in range(len(psd_freqs)):
		mean_psd_v.append(values[:,i,:].mean(0))

	mean_psd_values.append(mean_psd_v)


fig, axs = plt.subplots(4, nsignals)

for s in range(nsignals):
	vals = [row[s] for row in mean_mean_values]
	axs[0, s].bar(moves, vals)
	axs[0, s].set_title('Mean ' + axis(s+1))

for s in range(nsignals):
	vals = [row[s] for row in mean_std_values]
	axs[1, s].bar(moves, vals)
	axs[1, s].set_title('Std ' + axis(s+1))

for s in range(nsignals):
	vals = [row[s] for row in mean_kurtosis_values]
	axs[2, s].bar(moves, vals)
	axs[2, s].set_title('Kurtosis ' + axis(s+1))

for s in range(nsignals):
	vals = [row[s] for row in mean_skew_values]
	axs[3, s].bar(moves, vals)
	axs[3, s].set_title('Skewness ' + axis(s+1))

fig.suptitle('Results')

plt.show()

fig, axs = plt.subplots(len(moves), nsignals)
vals = np.array(mean_psd_values)

for m in range(len(moves)):

	for s in range(nsignals):

		axs[m, s].plot(psd_freqs, vals[m, s])
		axs[m, s].set_title('PSD Signal ' + axis(s+1) + ' ' + str(moves[m]))

fig.suptitle('Results')

plt.show()

