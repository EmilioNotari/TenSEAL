import tenseal as ts

class SimpleCKKSBootstrapper:
    def __init__(self, client_context, public_context):
        self.client_context = client_context  # con clave secreta
        self.public_context = public_context  # sin clave secreta
        self.scale = public_context.global_scale

    def bootstrap(self, ciphertext_serialized):
        # Crear ckks_vector desde serializado (sin secret_key en contexto público)
        ciphertext = ts.ckks_vector_from(self.client_context, ciphertext_serialized)

        # 1. Desencriptar
        plaintext = ciphertext.decrypt()
        print(f"[Bootstrapping] Desencriptado: {plaintext}")

        # 2. Reencriptar usando el contexto público
        reciphered = ts.ckks_vector(self.public_context, plaintext)
        print(f"[Bootstrapping] Reencriptado. Niveles restaurados.")

        return reciphered