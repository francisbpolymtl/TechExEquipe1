import numpy as np
import matplotlib.pyplot as plt

# Define the transfer function in terms of the central frequency and quality factor
def transfer_function(f, f0, Q):
    w0 = 2 * np.pi * f0
    w = 2 * np.pi * f
    x= w/w0
    # return w / (w0**2 - w**2 + 1j * w * w0 / Q)
    return 1/(1+1.j*Q*(x-1/(x+1e-16)))
    # return 1/(1+x/Q+x**2)

# Generate an input signal
t = np.linspace(1, 2, 1000, endpoint=False)
input_signal = np.sin(2 * np.pi * 5 * t) + 0.5 * np.sin(2 * np.pi * 50 * t)

# Apply the Fourier transform to the input signal
input_signal_freq = np.fft.fft(input_signal)

# Define frequencies
frequencies = np.fft.fftfreq(len(t), d=t[1]-t[0])


# Parameters of transfer function
Q = 30
f0 = 30

# Calculate transfer function norm and phase
transNorm = np.absolute(transfer_function(frequencies, f0, Q))
transAngle = np.angle(transfer_function(frequencies, f0, Q))

# Apply the transfer function to the input signal in the frequency domain
output_signal_freq = input_signal_freq * transfer_function(frequencies, f0, Q)

# Convert the output signal back to the time domain
output_signal = np.fft.ifft(output_signal_freq)


# Plot the input and output signals
plt.figure()
plt.plot(t, input_signal, label='Input Signal')
plt.plot(t, np.real(output_signal), label='Output Signal')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.legend()

# Plot the Bode diagrams
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.loglog(frequencies, transNorm, s=10)
plt.xscale('log')
plt.yscale('log')
plt.title('Magnitude Response of RLC Band-pass Filter')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.grid(which='both', axis='both')

plt.subplot(2, 1, 2)
plt.semilogx(frequencies, transAngle)
plt.xscale('log')
plt.title('Phase Response of RLC Band-pass Filter' )
plt.xlabel('Frequency (Hz)')
plt.ylabel('Phase (radians)')
plt.grid(which='both', axis='both')
plt.tight_layout()

# Plot the signals in freq space
plt.figure()
plt.plot(frequencies, np.absolute(input_signal_freq), label='Input Signal')
plt.plot(frequencies, np.absolute(output_signal_freq),label='Output Signal')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.legend()

plt.show()
