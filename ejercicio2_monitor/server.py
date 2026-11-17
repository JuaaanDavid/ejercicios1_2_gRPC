from concurrent import futures
import time
import random
from datetime import datetime
import grpc
import monitor_pb2
import monitor_pb2_grpc

class MonitorCadenaFrioServicer(monitor_pb2_grpc.MonitorCadenaFrioServicer):
    def TransmitirTelemetria(self, request, context):
        print(f"[Servidor] Solicitud recibida para camión: {request.id_camion}")
        camiones_validos = ["CAM-001", "CAM-002", "CAM-003", "CAM-004", "CAM-005"]
        
        if request.id_camion not in camiones_validos:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Camión {request.id_camion} no encontrado en el sistema")
            return monitor_pb2.LecturaSensor()

        for i in range(5): 
            temp_actual = round(random.uniform(0.0, 10.0), 1)
            alerta = temp_actual < 2.0 or temp_actual > 8.0

            lectura = monitor_pb2.LecturaSensor(
                id_camion= request.id_camion,
                temperatura_celsius= temp_actual,
                latitud= -0.18,
                longitud= -78.46,
                timestamp= datetime.now().strftime("%H:%M:%S"),
                alerta_critica= alerta
            )
            yield lectura
            
            time.sleep(request.intervalo_segundos)

def serve():
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    monitor_pb2_grpc.add_MonitorCadenaFrioServicer_to_server(
        MonitorCadenaFrioServicer(), servidor
    )
    puerto = "50051"
    servidor.add_insecure_port(f'[::]:{puerto}')
    servidor.start()
    print(f"[Servidor] Servidor escuchando en el puerto {puerto}...")
    servidor.wait_for_termination()

if __name__ == '__main__':
    serve()