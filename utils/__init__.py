from django.conf import settings

import pika, logging

rabbit_logger = logging.getLogger("rabbit")

def send_to_rabbitmq(routing_key, data):

    rabbit_logger.debug("[RABBITMQ SENDING '%s'] %s" % (routing_key, data))

    RABBITMQ_connection = pika.BlockingConnection(
        pika.ConnectionParameters(**settings.RABBITMQ)
    )
    RABBITMQ_channel = RABBITMQ_connection.channel()

    RABBITMQ_channel.basic_publish(
        exchange='application', routing_key=routing_key, body=data
    )
    RABBITMQ_connection.close()

    rabbit_logger.debug("[RABBITMQ SENT]")


# APPUNTI

# STUB PER LA PROVA DI MANTENERE PERMANENTE LA CONNESSIONE
# RABBITMQ_connection = pika.BlockingConnection(
#     pika.ConnectionParameters(**settings.RABBITMQ)
# )
# RABBITMQ_channel = RABBITMQ_connection.channel()
# routing_key = 'humen.update'
# data='ciao mondo'
# RABBITMQ_channel.exchange_declare(
#     exchange='application', type='direct'
# )
# RABBITMQ_channel.basic_publish(
#     exchange='application', routing_key=routing_key, body=data
# )
# RABBITMQ_connection.close()

