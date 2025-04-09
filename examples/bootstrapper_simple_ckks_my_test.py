import tenseal as ts

class SimulatedCKKSBootstrapper:
    def __init__(self, context, max_niveles=6, min_niveles=2):
        self.context = context
        self.max_niveles = max_niveles
        self.min_niveles = min_niveles
        self.niveles_restantes = max_niveles
        self.scale = context.global_scale

    def apply_operation(self, ciphertext):
        """Simula una operación homomórfica que consume un nivel."""
        self.niveles_restantes -= 1
        print(f"🔸 Operación: niveles restantes = {self.niveles_restantes}")
        return ciphertext * ciphertext

    def should_bootstrap(self):
        return self.niveles_restantes < self.min_niveles

    def bootstrap(self, ciphertext):
        """Bootstrapping simulado: reduce el ruido, pero no recupera niveles."""
        print(f"Bootstrapping aplicado (niveles restantes: {self.niveles_restantes})")
        try:
            # Simulamos reducción del ruido re-cifrando con escala original
            size = len(ciphertext.decrypt())
            result = ciphertext.polyval([0.0, 1.0])  # f(x) = x (identidad)
            new_ct = ts.ckks_vector(self.context, [0] * size)
            new_ct += result
            # NO se aumentan niveles
            return new_ct
        except Exception as e:
            print(f"Error durante el bootstrapping: {e}")
            return ciphertext

    def process(self, ciphertext):
        if self.should_bootstrap():
            ciphertext = self.bootstrap(ciphertext)
        return ciphertext
