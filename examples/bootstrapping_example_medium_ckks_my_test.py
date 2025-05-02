import tenseal as ts
import time
from bootstrapper_medium_ckks_my_test import MediumCKKSBootstrapper

def main():
    context = ts.context(
        ts.SCHEME_TYPE.CKKS,
        poly_modulus_degree=8192,
        coeff_mod_bit_sizes=[40, 40, 40, 40, 50]
    )
    context.global_scale = 2**40
    context.generate_galois_keys()
    context.generate_relin_keys()
    context.auto_rescale = True

    data = [1.0, 2.0, 3.0]
    ciphertext = ts.ckks_vector(context, data)

    print("\n\tINICIAL:", ciphertext.decrypt())

    bootstrapper = MediumCKKSBootstrapper(context)
    
    expected = []
    result = []
    error = []

    for i in range(45):
        print(f"\n########## Iteración {i+1} ##########\n")
        ciphertext *= 2
        data[0] *= 2

        start = time.time()
        ciphertext = bootstrapper.bootstrap(ciphertext)
        end = time.time()

        print(f"[Tiempo] Bootstrapping tardó: {end - start:.4f} segundos")

        expected.append(data[0])
        bootstrapped_result = ciphertext.decrypt()
        print("Resultado:", bootstrapped_result)
        result.append(bootstrapped_result[0])
        error.append(abs(result[-1]-expected[-1]))
        
    #print(f"EXPECTED: {expected}")
    #print(f"RESULT: {result}")
    print(f"ERROR")
    for i, elem in enumerate(error):
        print(f"#{i+1} -> {elem}")
    
if __name__ == "__main__":
    main()
