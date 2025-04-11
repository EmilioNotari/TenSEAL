import tenseal as ts

# Crear un contexto de TenSEAL
context = ts.context(ts.SCHEME_TYPE.CKKS, poly_modulus_degree=8192, coeff_mod_bit_sizes=[60, 40, 60])
context.generate_galois_keys()
context.global_scale=2**40

# Crear un vector cifrado utilizando TenSEAL
data = [1.0, 2.0, 3.0]
ciphertext = ts.ckks_vector(context, data)

# Método para obtener el scale de SEAL desde TenSEAL
def get_scale_from_seal(ciphertext):
    # Acceder al objeto Ciphertext de SEAL subyacente
    seal_ciphertext = ciphertext.ciphertext()
    print(f"SEAL_CT: {seal_ciphertext}")
    
    return seal_ciphertext[0].scale

# Obtener la escala desde SEAL
scale = get_scale_from_seal(ciphertext)
print(f"Escala del ciphertext: {scale}")
