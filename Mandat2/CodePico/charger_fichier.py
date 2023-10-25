from scipy.io import loadmat
import matplotlib.pyplot as plt
import numpy as np
# import panda as pd
# from IPython.display import display
# Spécifiez le chemin du fichier MATLAB que vous souhaitez ouvrir
chemin_du_fichier = 'C:\\Users\\Ivan\\OneDrive\\Documents\\Mandat 2\\test7\\test7_01.mat'

# Utilisez loadmat pour charger le fichier
donnees = loadmat(chemin_du_fichier)
print(donnees)
tau = 0.05
t = np.linspace(0,tau,len(donnees['A']))
N = len(t)
samplingf = N/tau

input_signal = donnees['A'].ravel()
output_signal = donnees['B'].ravel()
Rxx = np.fft.fft(np.correlate(input_signal, input_signal, mode='full'))
Rxy = np.fft.fft(np.correlate(output_signal, input_signal, mode='full'))

frequencies2 = np.fft.fftfreq(len(Rxy),1/samplingf )

H_approx = Rxy/Rxx

TF_approx_norm = np.absolute(H_approx)
TF_approx_angle = np.angle(H_approx)


TF_approx_norm = np.absolute(H_approx)
TF_approx_angle = np.angle(H_approx)

# Calculation of Q and f_0
max_TF_approx= max(TF_approx_norm)
maxArg_TF_approx = np.argmax(TF_approx_norm[:int(N/2)]) #f0
f0_approx = frequencies2[maxArg_TF_approx]

threshold = 1/np.sqrt(2)
target_norm = threshold * max_TF_approx

# Lower frequency
lower_bandwidth_index = (np.abs(np.array(TF_approx_norm[:maxArg_TF_approx]) - target_norm)).argmin()
lower_bandwidth_freq = frequencies2[lower_bandwidth_index]

# Upper frequency
upper_bandwidth_index = (np.abs(np.array(TF_approx_norm[maxArg_TF_approx:int(N)]) - target_norm)).argmin() + maxArg_TF_approx
upper_bandwidth_freq = frequencies2[upper_bandwidth_index]

beta_approx = upper_bandwidth_freq - lower_bandwidth_freq

Q_approx = f0_approx/beta_approx

data = {
    'Variable': [r'f0', r'Q', r'beta'],
    'Approximate Value': [f0_approx, Q_approx, beta_approx]
}

print(data)
plt.figure()
plt.loglog(frequencies2, TF_approx_norm, label = 'Approximation')
plt.ylim(0.0001,2)
plt.title(f'Approximation of norm(H)')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.legend()

plt.figure()
plt.semilogx(frequencies2, TF_approx_angle, label = 'Approximation')
plt.title(f'Approximation of phase(H) with')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Phase (radians)')
plt.legend

plt.show()