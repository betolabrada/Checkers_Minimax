#------------------------------------------------------------------------------------------------------------------
#	Decodificación de movimientos del móvil con técnicas de aprendizaje supervisado
#	Integrantes:
#		Alan González
#		Hyuntae Kim
#		Alberto Labrada
#------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------
from sklearn import datasets
from sklearn import svm
from sklearn.model_selection import KFold
from sklearn.metrics import confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
import matplotlib.pyplot as plt
import numpy as np
import sys
from scipy import stats
from scipy import signal

#------------------------------------------------------------------------------------------------------------------
#   Class Clasificador
#	* Entrenta todos los clasificadores y obtiene el precision, recall y accuracy para cada una de las 4 clases
#------------------------------------------------------------------------------------------------------------------
class Clasificador:
	def __init__(self, clf):
		self.clf = clf

	def train(self, kf, x, y):
		for train_index, test_index in kf.split(x):

            # Training phase
			x_train = x[train_index, :]
			y_train = y[train_index]

			self.clf.fit(x_train, y_train)

            # Test phase
			x_test = x[test_index, :]
			print('x_test', len(x_test[0]))
			y_test = y[test_index]

			y_pred = self.clf.predict(x_test)


	def predict(self, x):
		print(len(x[0]))
		return self.clf.predict(x)

	def results(self, kf_splits=5):
		pass

#------------------------------------------------------------------------------------------------------------------
#   Manejo de archivos
#------------------------------------------------------------------------------------------------------------------
def handle_files(pdata, pexp_data):
	# Archivo de señales
	data = np.loadtxt(pdata)
	# Archivo de ventanas
	exp_data = np.loadtxt(pexp_data, dtype='int')

	fs = 500														# Velocidad de muestreo
	window_size = int(fs * 0.1)										# 50 muestras
	nsignals = data.shape[1]										# Numero de señales

	trials = {}

	# Append windows per movement
	for step in exp_data:
		for index in range(step[1], step[2], window_size):
			# print(step[0], ' - ', index, ' - ', index + window_size - 1)

			if not step[0] in trials:
				trials[step[0]] = []

			trials[step[0]].append([index, index + window_size - 1])

	mean_values = {}
	std_values = {}
	kurtosis_values = {}
	skewness_values = {}
	psd_values = {}
	psd_freqs = []

	output = []

	for mov in trials:
		#print('Movimiento', mov)

		mean_values[mov] = []
		std_values[mov] = []
		kurtosis_values[mov] = []
		skewness_values[mov] = []
		psd_values[mov] = []

		for win in trials[mov]:
			# print('   Window', win)
			# Temporary values
			output_v = []
			output_v.append(mov)
			mean_v = []
			std_v = []
			kurtosis_v = []
			skewness_v = []
			psd_v = []
			for s in range(nsignals):
				# Foreach signal 
				sig = data[win[0] : win[1] + 1, s]
				mean = np.average(sig)
				std = np.std(sig)
				kur = stats.kurtosis(sig)
				skew = stats.skew(sig)

				mean_v.append(mean)
				std_v.append(std)
				kurtosis_v.append(kur)
				skewness_v.append(skew)

				freqs, psd = signal.periodogram(sig, fs, 'hamming', scaling='spectrum')            
				psd_v.extend(psd.tolist())
				# print(psd_freqs)

		
			mean_values[mov].append(mean_v)
			std_values[mov].append(std_v)
			kurtosis_values[mov].append(kurtosis_v)
			skewness_values[mov].append(skewness_v)
			psd_values[mov].append(psd_v)

			output_v.extend(mean_v)
			output_v.extend(std_v)
			output_v.extend(kurtosis_v)
			output_v.extend(skewness_v)
			output.append(output_v)

	return output


#------------------------------------------------------------------------------------------------------------------
#   Procesamiento de archivos para su posterior clasificación
#------------------------------------------------------------------------------------------------------------------
data_files = ['nueva_prueba/acc_data.txt']
trial_files = ['nueva_prueba/acc_trials.txt']

# K-NN Initialization
clf = Clasificador(KNeighborsClassifier(n_neighbors=3))
data_size = 12

print('preparing classifier...')
for file_i in range(len(data_files)):
	output = np.array(handle_files(data_files[file_i], trial_files[file_i]))
	# Sort array by first column
	output = output[np.argsort(output[:, 0])]
	# np.savetxt('moves_data.txt', output, fmt='%1.4g')
	x = []
	y = []
	for result in output:
		y.append(result[0])
		x.append([i for i in result[1:]])

	x = np.array(x)
	y = np.array(y)

	# 5-fold cross-validation
	kf = KFold(n_splits=5, shuffle = True)

	clf.train(kf, x, y)

print('classifier ready!')

#------------------------------------------------------------------------------------------------------------------
#   End of file
#------------------------------------------------------------------------------------------------------------------