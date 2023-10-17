# gabarit_controlePico.py
# Samuel Desmarais, 2021-09-02
# prealables: 
# - pip install numpy matplotlib picoscope
# - https://www.picotech.com/download/software/sr/PicoScope6_6.14.44.5870.exe

import numpy as np
import matplotlib.pyplot as plt
from picoscope import ps2000a

# 1) definition des signaux
amplitude = 1
fsine = 200e3

# 2) definition de l'echantillonage
duration = 0.01
fsamp = 2.1*fsine
psamp = 1/fsamp

# 3) connection au picoscope
pico = ps2000a.PS2000a()

# 4) preparation du channel A en reception
psamp_quantized, n_samples, _ = pico.setSamplingInterval(
    psamp,          # periode d'echantillonnage [s]
    duration        # duree de l'echantillonnage [s]
)
pico.setChannel(channel='A', coupling='AC', VRange=1)

# 5) demarrage de la generation du signal sinusoidal
pico.setSigGenBuiltInSimple(
    frequency=fsine,        # frequence du signal emit [Hz]
    pkToPk=amplitude*2,     # amplitude peak-to-peak [V]
    waveType='Sine'         # forme du signal
)

# 6) execution de l'acquisition telle que definie en 4
pico.runBlock()
pico.waitReady()    # attente de la fin de l'acquisition

# 7) telecharger les donnees du picoscope vers l'ordinateur
chA = pico.getDataV(
    'A',                # channel
    n_samples           # nombre d'echantillons a telecharger
)

# 8) arret du picoscope
pico.stop()
pico.close()

# 9) affichage du signal
tvect = psamp_quantized * np.arange(n_samples)
plt.plot(tvect, chA)
plt.show()
