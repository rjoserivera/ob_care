from locust import HttpUser, task, between
import random


class SistemaObstetricoUser(HttpUser):
    # Tiempo de espera entre cada tarea (simula comportamiento humano)
    wait_time = between(1, 3)

    @task(4)
    def home(self):
        """Prueba de carga para la página principal"""
        with self.client.get("/", catch_response=True) as r:
            if r.elapsed.total_seconds() > 2.0:
                r.failure(f"Lento: {r.elapsed.total_seconds()}s")

    @task(3)
    def buscar_ajax(self):
        """Prueba de búsqueda de paciente vía AJAX"""
        rut = random.choice(['12345678', '18901234'])
        with self.client.get(
            f"/matrona/api/paciente/buscar/?rut={rut}",
            catch_response=True
        ) as r:
            if r.elapsed.total_seconds() > 0.5:
                r.failure(f"AJAX lento: {r.elapsed.total_seconds() * 1000:.2f}ms")


# Ejecución del test de carga:
# 
#
# Interfaz web:
# http://localhost:8089
