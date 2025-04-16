import tenseal as ts
import numpy as np

class MediumCKKSBootstrapper:
    def __init__(self, context, target_scale=None):
        self.context = context
        self.default_scale = context.global_scale
        self.target_scale = target_scale or self.default_scale
        self.SMOOTHING_FACTOR = 0.01

    def normalize(self, ciphertext):
        seal_ciphertext = ciphertext.ciphertext()
        current_scale = seal_ciphertext[0].scale
        print(f"[Normalize] Escala actual: {current_scale}")

        if current_scale > self.target_scale:
            factor = current_scale / self.target_scale
            decrypted = ciphertext.decrypt()
            print(f"[Normalize] Decrypted: {decrypted}")
            
            # Ajustamos con un divisor más suave (factor raíz cuadrada)
            normalized_data = [elem / factor for elem in decrypted]
            print(f"[Normalize] Aplicado divisor de reescalado: {factor:.2e}")
            ciphertext = ts.ckks_vector(self.context, normalized_data)
        else:
            print("[Normalize] No se necesita normalización")

        return ciphertext



    def interpolate_hermite(self, x, y, dydx):
        """
        Simula la interpolación de Hermite (polinomio de Hermite).
        Recibe x, y y dydx (derivada en x) para construir el polinomio.
        """
        n = len(x)
        
        # Interpolación de Hermite (simplificada)
        H = np.zeros((2 * n, 2 * n))
        
        for i in range(n):
            H[2*i][0] = y[i]
            H[2*i + 1][0] = y[i]
            if i < n - 1:
                H[2*i + 1][1] = dydx[i]
        
        # Usamos la fórmula de interpolación para llenar la matriz
        for i in range(1, n):
            for j in range(i, n):
                H[i][j] = H[i][j - 1] + (x[j] - x[i]) * dydx[i]  # Simplificación

        # Devolvemos la interpolación de Hermite (puede adaptarse a un polinomio específico)
        return H

    def fast_fourier_transformation(self, ciphertext):
        """
        Simula el proceso de FFT para polinomios en el ciphertext.
        Aquí solo vamos a aplicar una transformación FFT a los datos del ciphertext.
        """        
        data = ciphertext #ciphertext.decrypt()
        print(f"[FFT] Datos antes de FFT: {data}")
        
        # Aplicamos FFT real sobre los valores cifrados (simulado)
        fft_result = np.fft.fft(data)
        
        print(f"[FFT] Datos después de FFT: {fft_result}")
        
        # Convertimos de nuevo el resultado de FFT a un vector cifrado
        #result_ciphertext = ts.ckks_vector(self.context, np.real(fft_result)) 
        return fft_result #result_ciphertext

    def bootstrap(self, ciphertext):
        print("[Bootstrap] Simulación de bootstrapping con interpolación y FFT (estabilizado)")

        try:
            # Paso 1: Desencriptamos y normalizamos
            y = ciphertext.decrypt() #test
            x = np.linspace(0, 1, len(y)) #
            print(f"[Bootstrap] x: {x}")
            print(f"[Bootstrap] y (original): {y}")

            # Escalamos para estabilizar Hermite
            scale_factor = max(abs(v) for v in y)
            y_scaled = [v / scale_factor for v in y]
            print(f"[Bootstrap] y escalado: {y_scaled}")

            # Derivadas aproximadas
            dydx = np.gradient(y_scaled)
            print(f"[Bootstrap] dydx: {dydx}") 

            # Interpolación Hermite (sin cambios)
            H = self.interpolate_hermite(x, y_scaled, dydx)
            y_ext = np.repeat(y_scaled, 2)

            hermite_result = np.dot(H, y_ext)
            print(f"[Bootstrap] Hermite result: {hermite_result}")

            # Solo aplicamos una corrección leve basada en Hermite
            result = y_scaled + self.SMOOTHING_FACTOR * hermite_result[:len(y_scaled)]
            result *= scale_factor  # Reescalamos de vuelta
            print(f"[Bootstrap] Resultado tras Hermite ajustado: {result}")

            # Recreamos el ciphertext
            #reconstructed_ciphertext = ts.ckks_vector(self.context, result)

            # Paso 2: FFT
            reconstructed_ciphertext = self.fast_fourier_transformation(result) #reconstructed_Ct

            # Paso 2.5: IFFT
            ifft_data = np.fft.ifft(reconstructed_ciphertext)  #reconstructed_ct.decrypt()
            recovered = np.real(ifft_data)
            print(f"[Bootstrap] Recuperado tras IFFT: {recovered}")

            # Paso 3: Reencriptar
            reconstructed_ciphertext = ts.ckks_vector(self.context, recovered)

            return reconstructed_ciphertext

        except Exception as e:
            print(f"[Bootstrap] Error: {e}")
            return ciphertext
