
import tenseal as ts
import numpy as np
import time

def create_ckks_context(enable_bootstrapping=False):
    context = ts.context(
        scheme=ts.SCHEME_TYPE.CKKS,
        poly_modulus_degree=8192,
        coeff_mod_bit_sizes=[60, 40, 40, 60]
    )
    
    context.global_scale = 2**40  #Para trabajar con números reales.
    context.generate_galois_keys()

    if enable_bootstrapping:
        context.generate_relin_keys()

    return context


def encrypt_matrix(matrix, context):
    return [[ts.ckks_vector(context, [value]) for value in row] for row in matrix]


def decrypt_matrix(encrypted_matrix, context):
    return [[vec.decrypt()[0] for vec in row] for row in encrypted_matrix]


def matrix_multiplication_ckks(matrix1, matrix2, context):
    rows1, cols1 = len(matrix1), len(matrix1[0])
    rows2, cols2 = len(matrix2), len(matrix2[0])

    if cols1 != rows2:
        raise ValueError("Dimensiones incompatibles para multiplicación.")

    result = [[None for _ in range(cols2)] for _ in range(rows1)]

    for i in range(rows1):
        for j in range(cols2):
            sum_enc = matrix1[i][0] * matrix2[0][j]
            for k in range(1, cols1):
                sum_enc += matrix1[i][k] * matrix2[k][j]
            result[i][j] = sum_enc

    return result


def main(enable_bootstrapping=False):
    # Crear contexto
    context = create_ckks_context(enable_bootstrapping)

    # Generar matrices con valores decimales
    matrix1 = np.random.uniform(0.1, 5.0, (4, 4)).tolist()
    matrix2 = np.random.uniform(0.1, 5.0, (4, 4)).tolist()

    #print("\nMatriz 1 (original):", matrix1)
    #print("Matriz 2 (original):", matrix2)
    
    # Medición del tiempo de ejecución
    start_time = time.time()

    # Cifrar matrices
    enc_matrix1 = encrypt_matrix(matrix1, context)
    enc_matrix2 = encrypt_matrix(matrix2, context)

    # Multiplicación de matrices cifradas
    enc_result = matrix_multiplication_ckks(enc_matrix1, enc_matrix2, context)
    
    end_time = time.time()

    # Descifrar resultado
    decrypted_result = decrypt_matrix(enc_result, context)

    #print("\nMatriz resultado (descifrada):", decrypted_result)
    
    # Impresión del tiempo de ejecución
    print(f"Tiempo de ejecución: {end_time - start_time} segundos")


if __name__ == "__main__":
    print("Ejecución SIN bootstrapping:")
    main(enable_bootstrapping=False)

    print("\nEjecución CON bootstrapping:")
    main(enable_bootstrapping=True)