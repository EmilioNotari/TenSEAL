# archivo: bfv_bootstrapper_example.py
import tenseal as ts
from bootstrapper_simple_bfv_my_test import SimulatedBFVBootstrapper

def main():
    # Crear contexto BFV
    context = ts.context(
        ts.SCHEME_TYPE.BFV,
        poly_modulus_degree=8192,
        plain_modulus=1032193
    )

    # Crear bootstrapper
    bootstrapper = SimulatedBFVBootstrapper(context, max_ops=2)

    # Cifrar un número
    ciphertext = ts.bfv_vector(context, [5])
    print("Inicial:", ciphertext.decrypt())

    # Simulamos operaciones homomórficas
    for i in range(6):
        print(f"\nIteración {i+1}")
        ciphertext = ciphertext * 2
        ciphertext = bootstrapper.bootstrapp(ciphertext)
        print("Valor:", ciphertext.decrypt())

if __name__ == "__main__":
    main()
