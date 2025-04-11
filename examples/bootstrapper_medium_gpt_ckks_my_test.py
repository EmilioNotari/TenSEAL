import tenseal as ts
import numpy as np

class MediumCKKSGptBootstrapper:
    def __init__(self, context, target_scale=None):
        self.context = context
        self.default_scale = context.global_scale
        self.target_scale = target_scale or self.default_scale

    def interpolate_hermite(self, x, y, dydx):
        """Interpolación de Hermite simplificada."""
        n = len(x)
        H = np.zeros((2 * n, 2 * n))
        for i in range(n):
            H[2 * i][0] = y[i]
            H[2 * i + 1][0] = y[i]
            if i < n - 1:
                H[2 * i + 1][1] = dydx[i]

        # Rellenar resto de matriz (simplificado)
        for j in range(2, 2 * n):
            for i in range(2 * n - j):
                if x[i//2] != x[(i + j)//2]:
                    H[i][j] = (H[i + 1][j - 1] - H[i][j - 1]) / (x[(i + j)//2] - x[i//2])
                else:
                    H[i][j] = dydx[i//2]

        return H

    def fast_fourier_transformation(self, ciphertext):
        """
        Simula el proceso de FFT para polinomios en el ciphertext.
        Aquí solo vamos a aplicar una transformación FFT a los datos del ciphertext.
        """        
        data = ciphertext.decrypt()
        print(f"[FFT] Datos antes de FFT: {data}")
        
        # Aplicamos FFT real sobre los valores cifrados (simulado)
        fft_result = np.fft.fft(data)
        
        print(f"[FFT] Datos después de FFT: {fft_result}")
        
        # Convertimos de nuevo el resultado de FFT a un vector cifrado
        result_ciphertext = ts.ckks_vector(self.context, np.real(fft_result)) 
        return result_ciphertext

    def bootstrap(self, ciphertext):
        """Simula el bootstrapping usando Hermite + FFT (reversible) + reescalado.""" 
        print("[Bootstrap] Simulación de bootstrapping con interpolación y FFT")

        try:
            # Paso 1: Interpolación de Hermite
            y = ciphertext.decrypt()
            x = np.linspace(0, 1, len(y))
            print(f"[Bootstrap] x: {x}")
            dydx = np.gradient(y)
            print(f"[Bootstrap] dydx: {dydx}")

            H = self.interpolate_hermite(x, y, dydx)
            print(f"[Hermite] Interpolación de Hermite: \n{H}")

            # Extraer valores aproximados desde la diagonal
            hermite_result = [H[i][i] for i in range(len(y))]
            print(f"[Hermite] Resultado aproximado: {hermite_result}")

            # Paso 2: FFT reversible (FFT + IFFT)
            fft_encrypted = self.fast_fourier_transformation(ciphertext)
            fft_smoothed_data = np.fft.ifft(fft_encrypted.decrypt())
            
            ciphertext = ts.ckks_vector(self.context, np.real(fft_smoothed_data))

            return ciphertext

        except Exception as e:
            print(f"[Bootstrap] Error: {e}")
            return ciphertext
