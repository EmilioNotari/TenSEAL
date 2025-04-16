import tenseal as ts
from bootstrapper_medium_ckks_my_test import MediumCKKSBootstrapper

def main():
    context = ts.context(
        ts.SCHEME_TYPE.CKKS,
        poly_modulus_degree=8192,
        coeff_mod_bit_sizes=[60, 40, 40, 60]
    )
    context.global_scale = 2**40
    context.generate_galois_keys()
    context.generate_relin_keys()
    context.auto_rescale = True

    data = [1.0, 2.0, 3.0]
    ciphertext = ts.ckks_vector(context, data)

    print("\n\tINICIAL:", ciphertext.decrypt())

    bootstrapper = MediumCKKSBootstrapper(context)

    for i in range(3):
        print(f"\n########## Iteración {i+1} ##########\n")
        ciphertext *= 10  # Aumenta la escala (2^40 * 2^40 = 2^80)
        ciphertext = bootstrapper.bootstrap(ciphertext)
        print("Resultado:", ciphertext.decrypt())

if __name__ == "__main__":
    main()
