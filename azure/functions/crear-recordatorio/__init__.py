import logging
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Procesando recordatorio...')
    return func.HttpResponse("Recordatorio creado", status_code=200)
