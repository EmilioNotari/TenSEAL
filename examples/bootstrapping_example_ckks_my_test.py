import tenseal as ts
from examples.bootstrapper_simple_ckks_my_test import SimulatedCKKSBootstrapper

def main():
    # Configuración del contexto
    context = ts.context(
        ts.SCHEME_TYPE.CKKS,
        poly_modulus_degree=8192,
        coeff_mod_bit_sizes=[60, 40, 40, 60]
    )
    context.global_scale = 2**30
    context.generate_galois_keys()

    data = [1.0, 2.0, 3.0]
    ct = ts.ckks_vector(context, data)

    print(f"🔹 Inicial: {ct.decrypt()}")
    bootstrapper = SimulatedCKKSBootstrapper(context)

    for i in range(2):
        print(f"\n🔹 Iteración {i+1}")
        ct = bootstrapper.apply_operation(ct)
        ct = bootstrapper.process(ct)
        print("Resultado:", ct.decrypt())

if __name__ == "__main__":
    main()
