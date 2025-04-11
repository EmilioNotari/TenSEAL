import tenseal as ts
from bootstrapper_simple_ckks_my_test import SimpleCKKSBootstrapper

def main():
    # Cliente genera contexto completo
    client_context = ts.context(
        ts.SCHEME_TYPE.CKKS,
        poly_modulus_degree=8192,
        coeff_mod_bit_sizes=[60, 40, 40, 60]
    )
    client_context.global_scale = 2**20
    client_context.generate_galois_keys()
    client_context.generate_relin_keys()

    # Servidor solo recibe un contexto sin clave secreta
    public_context = ts.context_from(client_context.serialize(save_secret_key=False))

    # Cifrado inicial (por el cliente)
    data = [1.0, 2.0, 3.0]
    print("\nDATOS INICIALES: ", data)
    ciphertext = ts.ckks_vector(public_context, data)

    # Simulación de operaciones en el servidor
    for i in range(3):
        print(f"\n[Servidor] Operación homomórfica #{i+1}")
        ciphertext *= 5

        # Serializar resultado y enviar al cliente para bootstrapping
        serialized_ct = ciphertext.serialize()
        bootstrapper = SimpleCKKSBootstrapper(client_context, public_context)

        # Cliente realiza bootstrapping y devuelve nuevo cifrado
        ciphertext = bootstrapper.bootstrap(serialized_ct)

        # Desencriptar (lado cliente, para pruebas)
        test = ts.ckks_vector_from(client_context, ciphertext.serialize())
        print("Post-bootstrap:", test.decrypt())


if __name__ == "__main__":
    main()
