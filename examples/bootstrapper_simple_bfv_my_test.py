# archivo: bfv_bootstrapper_sim.py
import tenseal as ts

class SimulatedBFVBootstrapper:
    def __init__(self, context, max_ops=3):
        """
        Simula un bootstrapper para BFV.
        max_ops define cuántas operaciones se permiten antes de refrescar.
        """
        self.context = context
        self.max_ops = max_ops
        self.op_count = 0 

    def refresh_if_needed(self, ct):
        """
        Simula el bootstrapping si se supera el umbral de operaciones.
        """
        self.op_count += 1

        if self.op_count >= self.max_ops:
            print(f"Simulando bootstrapping (operaciones: {self.op_count})")

            # simulación de bootstrapping
            data = ct.decrypt()
            ct = ts.bfv_vector(self.context, data)

            self.op_count = 0  

        return ct
