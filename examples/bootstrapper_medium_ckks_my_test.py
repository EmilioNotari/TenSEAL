import tenseal as ts
import numpy as np

class MediumCKKSBootstrapper:
    def __init__(self, context, target_scale=None):
        self.context = context
        self.default_scale = context.global_scale
        self.target_scale = target_scale or self.default_scale

    def normalize(self, ciphertext):
        """
        Simula el reescalado homomórfico: reduce la escala del ciphertext.
        """
        current_scale = ciphertext.scale
        print(f"[Normalize] Escala actual: {current_scale:.2e}")

        if current_scale > self.target_scale:
            factor = current_scale / self.target_scale
            ciphertext /= factor            
            print(f"[Normalize] Aplicado divisor de reescalado: {factor:.2e}")
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
        data = ciphertext.decrypt()
        print(f"[FFT] Datos antes de FFT: {data}")
        
        # Aplicamos FFT real sobre los valores cifrados (simulado)
        fft_result = np.fft.fft(data)
        
        print(f"[FFT] Datos después de FFT: {fft_result}")
        
        # Convertimos de nuevo el resultado de FFT a un vector cifrado
        result_ciphertext = ts.ckks_vector(self.context, np.real(fft_result)) 
        return result_ciphertext

    def bootstrap(self, ciphertext):
        """
        Simula el bootstrapping:
        1. Interpolación de Hermite
        2. FFT para el polinomio encriptado
        3. Normalización (reescalado)
        """
        print("[Bootstrap] Simulación de bootstrapping con interpolación y FFT")

        try:
            # Paso 1: Aplicar interpolación de Hermite (simulada)
            # Tomamos datos de la encriptación para usarlo como puntos x, y y derivadas (dydx)
            x = np.linspace(0, 1, len(ciphertext.decrypt()))  # Puntos de interpolación
            y = ciphertext.decrypt()  # Valores de ciphertext
            dydx = np.gradient(y)  # Derivada aproximada (en este ejemplo simplificado)
            
            # Interpolación de Hermite
            H = self.interpolate_hermite(x, y, dydx)
            print(f"[Bootstrap] Interpolación de Hermite: \n{H}")
            
            # Duplicamos los valores de y y dydx para que coincidan con H
            y_ext = np.repeat(y, 2)
            dydx_ext = np.repeat(dydx, 2)
            
            # Simulamos un "reconstrucción" con el polinomio interpolado de Hermite
            # Aquí simplemente tomamos el primer término para simplificar la simulación
            result = np.dot(H, y_ext)  # Esto sería un ejemplo simple de reconstrucción
            
            # Reconstrucción del ciphertext (de manera simplificada, en un caso real usaríamos otros métodos)
            reconstructed_ciphertext = ts.ckks_vector(self.context, result)            

            # Paso 2: Aplicar FFT al ciphertext (simulación)
            reconstructed_ciphertext = self.fast_fourier_transformation(reconstructed_ciphertext)

            # Paso 3: Normalización / reescalado
            reconstructed_ciphertext = self.normalize(reconstructed_ciphertext)

            return reconstructed_ciphertext
        except Exception as e:
            print(f"[Bootstrap] Error: {e}")
            return ciphertext
