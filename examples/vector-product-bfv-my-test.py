import tenseal as ts
import numpy as np
import time

def main(n_items):
    context = ts.context(
        scheme=ts.SCHEME_TYPE.BFV,
        poly_modulus_degree = 8192,  # Tamaño del polinomio
        plain_modulus=65537        # Debe ser un número primo grande
    )
    context.generate_galois_keys()
    context.generate_relin_keys()

    vec1 = np.random.randint(1, 100, n_items).tolist()
    vec2 = np.random.randint(1, 100, n_items).tolist()

    # Medición del tiempo de ejecución
    start_time = time.time()

    # Cifrar los vectores
    encrypted_vec1 = ts.bfv_vector(context, vec1)
    encrypted_vec2 = ts.bfv_vector(context, vec2)

    # Multiplicar los vectores cifrados
    encrypted_result = encrypted_vec1 * encrypted_vec2  

    end_time = time.time()

    # Descifrar el resultado
    decrypted_result = encrypted_result.decrypt()

    # Mostrar tiempo de ejecución
    print(f"Tiempo de ejecución: {end_time - start_time} segundos")

if __name__ == "__main__":
    n_items = 1000 
    main(n_items)
