import tenseal as ts
import numpy as np
import time

# Parámetros globales
POLY_MODULUS_DEGREE = 8192
COEFF_MODULUS = [60, 40, 40, 60]

def EvalBootstrapKeyGen(context):
    """
    Genera claves de bootstrapping usando operaciones criptográficas sencillas.
    :param context: El contexto de TenSEAL.
    :return: Un diccionario con las claves de bootstrapping.
    """
    # Dimensión del anillo
    ring_dim = POLY_MODULUS_DEGREE 

    # Número de slots 
    num_slots = ring_dim // 2

    # Generar una máscara aleatoria
    mask = np.random.rand(num_slots)  
    mask = mask.tolist()

    noise = np.random.normal(0, 0.0001, num_slots) 
    noise = noise.tolist()

    # Cifrar la máscara y el ruido usando la clave pública
    mask_key = ts.ckks_vector(context, mask)
    noise_key = ts.ckks_vector(context, noise)

    context.bootstrap_keys = {
        "mask_key": mask_key,
        "noise_key": noise_key,
    }

    return context.bootstrap_keys

def EvalBootstrap(context, ciphertext):
    """
    Función de bootstrapping usando las claves generadas.
    :param context: El contexto de TenSEAL.
    :param ciphertext: El cifrado que se va a refrescar.
    :return: El cifrado refrescado.
    """
    # Obtener las claves de bootstrapping
    bootstrap_keys = context.bootstrap_keys

    # Aplicar la máscara y reducir el ruido
    masked_ciphertext = ciphertext * bootstrap_keys["mask_key"]  
    noised_ciphertext = masked_ciphertext + bootstrap_keys["noise_key"] 

    return noised_ciphertext

def main():
    # Configuración del contexto de TenSEAL
    context = ts.context(
        scheme=ts.SCHEME_TYPE.CKKS,
        poly_modulus_degree=POLY_MODULUS_DEGREE,   
        coeff_mod_bit_sizes=COEFF_MODULUS
    )
    context.global_scale = 2**40 
    context.generate_galois_keys()  
    context.generate_relin_keys()

    # Generar claves de bootstrapping
    bootstrap_keys = EvalBootstrapKeyGen(context)
    print("Claves de bootstrapping generadas:")
    print("Mask Key:", bootstrap_keys["mask_key"].decrypt()[:5], "...")  
    print("Noise Key:", bootstrap_keys["noise_key"].decrypt()[:5], "...") 

    ring_dim = POLY_MODULUS_DEGREE 
    num_slots = ring_dim // 2
    print("Dimensión del anillo (ringDim):", ring_dim)
    print("Número de slots (numSlots):", num_slots)

    # Datos de ejemplo
    data = np.random.uniform(low=1.0, high=5.0, size=num_slots) 
    print("Datos originales:", data[:5], "...")  

    # Medición del tiempo de ejecución
    start_time = time.time()

    # Codificar y cifrar los datos
    encrypted_data = ts.ckks_vector(context, data)
    print("Datos cifrados:", encrypted_data.decrypt()[:5], "...")  

    # Aplicar bootstrapping
    bootstrapped_data = EvalBootstrap(context, encrypted_data)
    print("Datos refrescados:", bootstrapped_data.decrypt()[:5], "...")  

    end_time = time.time()

    # Verificar la precisión
    original_data = np.array(data)
    bootstrapped_data_decrypted = np.array(bootstrapped_data.decrypt())  
    # Calcular el error absoluto medio (MAE)
    mae = np.mean(np.abs(original_data - bootstrapped_data_decrypted))
    print("Error absoluto medio después del bootstrapping:", mae)

    # Impresión del tiempo de ejecución
    print(f"\nTiempo de ejecución: {end_time - start_time} segundos")

if __name__ == "__main__":
    main()