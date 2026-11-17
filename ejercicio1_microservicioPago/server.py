from concurrent import futures
import uuid
import grpc
import pagos_pb2
import pagos_pb2_grpc


class ValidadorPagosServicer(pagos_pb2_grpc.ValidadorPagosServicer):
    def VerificarTransaccion(self, request, context):
        print(f"[Servidor] Evaluando {request.id_transaccion}: {request.monto} {request.codigo_moneda} | País: {request.pais_origen}")

        if request.monto <= 0 or len(request.numero_tarjeta) != 16:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Monto o número de tarjeta inválido")
            return pagos_pb2.ResultadoPago()

        if request.numero_tarjeta.startswith("4000"):
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Tarjeta bloquada por fraude")
            return pagos_pb2.ResultadoPago()

        if request.monto > 10000 and request.pais_origen not in ["US", "MX"]:
            return pagos_pb2.ResultadoPago(
                aprobado=False,
                codigo_autorizacion="",
                motivo_rechazo="Rechazo monto alto desde país no autorizado"
            )

        codigo_auth = f"AUTH-{uuid.uuid4().hex[:8].upper()}"
        return pagos_pb2.ResultadoPago(
            aprobado=True,
            codigo_autorizacion=codigo_auth,
            motivo_rechazo=""
        )


def serve():
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pagos_pb2_grpc.add_ValidadorPagosServicer_to_server(
        ValidadorPagosServicer(), servidor
    )
    puerto = "50051"
    servidor.add_insecure_port(f'[::]:{puerto}')
    servidor.start()
    print(f"[Servidor] Servidor escuchando en el puerto {puerto}...")
    servidor.wait_for_termination()


if __name__ == '__main__':
    serve()