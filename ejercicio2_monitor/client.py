import grpc
import monitor_pb2
import monitor_pb2_grpc

def solicitar_telemetria(stub, id_camion):
    print(f"\nIniciando ingreso para: {id_camion}")
    peticion = monitor_pb2.SuscripcionCamion(
        id_camion= id_camion,
        intervalo_segundos= 1
    )
    try:
        respuestas = stub.TransmitirTelemetria(peticion)
        for lectura in respuestas:
            if lectura.alerta_critica:
                print(f"[ALERTA CRÍTICA] {lectura.timestamp} --- {lectura.id_camion} --- Temp: {lectura.temperatura_celsius} celsius")
            else:
                print(f"[Cliente] {lectura.timestamp} --- {lectura.id_camion} --- Temp: {lectura.temperatura_celsius} celsius (Normal)")
                
    except grpc.RpcError as e:
        print(f"[Error gRPC] Código: {e.code()} Detalle: {e.details()}")

def run():
    with grpc.insecure_channel('localhost:50051') as canal:
        stub = monitor_pb2_grpc.MonitorCadenaFrioStub(canal)
        solicitar_telemetria(stub, "CAM-999")
        solicitar_telemetria(stub, "CAM-001")
        solicitar_telemetria(stub, "CAM-002")
        solicitar_telemetria(stub, "CAM-003")

if __name__ == '__main__':
    run()