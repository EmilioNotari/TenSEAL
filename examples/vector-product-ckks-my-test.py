import tenseal as ts
import numpy as np
import time

def main(n_items):
    context = ts.context(
        scheme=ts.SCHEME_TYPE.CKKS,
        poly_modulus_degree=32768,  # Tamaño del polinomio
        coeff_mod_bit_sizes=[60, 40, 40, 60]  # Niveles de escala para la precisión
    )
    context.global_scale = 2**40  # Escala para operaciones de punto flotante
    context.generate_galois_keys()

    vec1 = np.random.uniform(1, 100, n_items).tolist()
    vec2 = np.random.uniform(1, 100, n_items).tolist()
    
    print("Vector 1:", vec1[:3])
    print("Vector 2:", vec2[:3])

    # Medición del tiempo de ejecución
    start_time = time.time()

    # Cifrar los vectores
    encrypted_vec1 = ts.ckks_vector(context, vec1)
    encrypted_vec2 = ts.ckks_vector(context, vec2)

    # Multiplicar los vectores cifrados (element-wise)
    encrypted_result = encrypted_vec1 * encrypted_vec2

    end_time = time.time()

    # Descifrar el resultado
    decrypted_result = encrypted_result.decrypt()
    
    print("Resultado descifrado:", decrypted_result[:3])
    
    # Mostrar tiempo de ejecución
    print(f"Tiempo de ejecución: {end_time - start_time} segundos")


if __name__ == "__main__":
    n_items = 10000000
    main(n_items)
