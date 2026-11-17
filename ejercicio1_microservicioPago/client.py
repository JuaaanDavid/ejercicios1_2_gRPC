import grpc
import pagos_pb2
import pagos_pb2_grpc


def enviar_pago(stub, nombre_prueba, solicitud):
    print(f"{nombre_prueba} (Tx: {solicitud.id_transaccion})")
    try:
        respuesta = stub.VerificarTransaccion(solicitud)
        if respuesta.aprobado:
            print(f"[Cliente] APROBADO: Código Auth: {respuesta.codigo_autorizacion}")
        else:
            print(f"[Cliente] RECHAZADO: Motivo: {respuesta.motivo_rechazo}")
    except grpc.RpcError as e:
        print(f"[Error gRPC] Código: {e.code()} | Detalle: {e.details()}")


def run():
    with grpc.insecure_channel('localhost:50051') as canal:
        stub = pagos_pb2_grpc.ValidadorPagosStub(canal)
        # Caso 1
        peticion1 = pagos_pb2.SolicitudPago(
            id_transaccion="TX-001",
            numero_tarjeta="4532123456789012",
            monto=100.0,
            codigo_moneda="USD",
            pais_origen="US"
        )
        enviar_pago(stub, "Prueba 1: Pago Exitoso", peticion1)

        # Caso 2
        peticion2 = pagos_pb2.SolicitudPago(
            id_transaccion="TX-002",
            numero_tarjeta="4532123456789012",
            monto=-50.0,
            codigo_moneda="MXN",
            pais_origen="MX"
        )
        enviar_pago(stub, "Prueba 2: Argumento Inválido", peticion2)

        # Caso 3
        peticion3 = pagos_pb2.SolicitudPago(
            id_transaccion="TX-003",
            numero_tarjeta="4000123456789012",
            monto=150.0,
            codigo_moneda="USD",
            pais_origen="US"
        )
        enviar_pago(stub, "Prueba 3: Tarjeta Bloqueada", peticion3)

        # Caso 4 
        peticion4 = pagos_pb2.SolicitudPago(
            id_transaccion="TX-004",
            numero_tarjeta="4532123456789012",
            monto=15000.0,
            codigo_moneda="USD",
            pais_origen="EC"
        )
        enviar_pago(stub, "Prueba 4: Política de Fraude (Monto Alto)", peticion4)


if __name__ == '__main__':
    run()