import tenseal as ts
import numpy as np
import time
import ctypes.util


# ---- DEMO ----
def main(n_items):
    # Crear contexto CKKS
    context = ts.context(
        scheme=ts.SCHEME_TYPE.CKKS,
        poly_modulus_degree=32768,  # estaba a 8192 pero lo he subido para sumar vectores con más de 10000 elementos
        coeff_mod_bit_sizes=[60, 40, 40, 60]
    )
    context.global_scale = 2**40  # Escala global para precisión
    context.generate_galois_keys()

    # Generar vectores aleatorios DECIMALES entre 1 y 100
    vec1 = np.random.uniform(1, 100, n_items).tolist()
    vec2 = np.random.uniform(1, 100, n_items).tolist()

    print("Vector 1:", vec1)
    print("Vector 2:", vec2)
    
    # Medición del tiempo de ejecución
    start_time = time.time()

    # Cifrar los vectores
    encrypted_vec1 = ts.ckks_vector(context, vec1)
    encrypted_vec2 = ts.ckks_vector(context, vec2)

    # Sumar los vectores cifrados
    encrypted_result = encrypted_vec1 + encrypted_vec2
    
    end_time = time.time()

    # Descifrar el resultado
    decrypted_result = encrypted_result.decrypt()

    print("Resultado descifrado:", decrypted_result)
    
    # Impresión del tiempo de ejecución
    print(f"Tiempo de ejecución: {end_time - start_time} segundos")

if __name__ == "__main__":
    n_items = 3  
    main(n_items)
