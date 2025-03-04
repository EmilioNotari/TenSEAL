import tenseal as ts
import numpy as np
import time

def generate_bfv_context():
    """ Configura el contexto de TenSEAL para el esquema BFV. """
    context = ts.context(
        scheme=ts.SCHEME_TYPE.BFV,
        poly_modulus_degree=8192,
        plain_modulus = 65537,
        coeff_mod_bit_sizes=[60, 40, 40, 60]
    )
    context.generate_galois_keys() # Permite hacer rotaciones
    context.generate_relin_keys() # Genera las claves de relinearización
    return context

def encrypt_matrix(matrix, context):
    return [[ts.bfv_vector(context, [int(cell)]) for cell in row] for row in matrix]

def decrypt_matrix(matrix, context):
    return [[vec.decrypt()[0] for vec in row] for row in matrix]

def bfv_matrix_multiplication(matrix1, matrix2, context):
    rows1, cols1 = len(matrix1), len(matrix1[0])
    rows2, cols2 = len(matrix2), len(matrix2[0])
    
    if cols1 != rows2:
        raise ValueError("Dimensiones incompatibles para la multiplicación de matrices.")
    
    result = [[None for _ in range(cols2)] for _ in range(rows1)]
    
    for i in range(rows1):
        for j in range(cols2):
            sum_enc = matrix1[i][0] * matrix2[0][j]
            for k in range(1, cols1):
                sum_enc += matrix1[i][k] * matrix2[k][j]
            result[i][j] = sum_enc
    
    return result

def main():
    context = generate_bfv_context()
    
    matrix1 = np.random.randint(0, 10, (64, 64)).tolist()
    matrix2 = np.random.randint(0, 10, (64, 64)).tolist()
    
    # Medición del tiempo de ejecución
    start_time = time.time()
    
    encrypted_matrix1 = encrypt_matrix(matrix1, context)
    encrypted_matrix2 = encrypt_matrix(matrix2, context)
    
    encrypted_result = bfv_matrix_multiplication(encrypted_matrix1, encrypted_matrix2, context)
    
    end_time = time.time()
    
    decrypted_result = decrypt_matrix(encrypted_result, context)
    
    #print("Matriz 1:", matrix1)
    #print("Matriz 2:", matrix2)
    #print("Resultado homomórfico descifrado:", decrypted_result)
    
    # Impresión del tiempo de ejecución
    print(f"Tiempo de ejecución: {end_time - start_time} segundos")

if __name__ == "__main__":
    main()
