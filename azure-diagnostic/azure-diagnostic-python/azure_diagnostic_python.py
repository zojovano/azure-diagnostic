from azure.servicebus import ServiceBusClient, ServiceBusMessage

from logging import INFO, getLogger

# Import the `configure_azure_monitor()` function from the
# `azure.monitor.opentelemetry` package.
from azure.monitor.opentelemetry import configure_azure_monitor

# Import the tracing api from the `opentelemetry` package.
from opentelemetry import trace

import time
import socket
import os

env_connstr = os.environ['SERVICE_BUS_CONNECTION_STRING']
env_queue_name = os.environ['SERVICE_BUS_QUEUE_NAME']
env_appinsights_connection_string = os.environ['APPINSIGHTS_CONNECTION_STRING']
env_conn = os.environ['SERVICE_BUS_ENDPOINT']

connstr = env_connstr
queue_name = env_queue_name

print(env_connstr)
print(env_queue_name)
print(env_appinsights_connection_string)

configure_azure_monitor(connection_string=env_appinsights_connection_string, disable_offline_storage=True)

# Get a tracer for the current module.
tracer = trace.get_tracer(__name__)
logger = getLogger(__name__)
logger.setLevel(INFO)

# Start a new span with the name "hello". This also sets this created span as the current span in this context. This span will be exported to Azure Monitor as part of the trace.
with tracer.start_as_current_span("azure-diagnostic--servicebus"):
    print("OTEL tracer started")
    logger.info("Logger: OTEL tracer started")


    # Create a Service Bus client
    with ServiceBusClient.from_connection_string(connstr) as client:
        while True:        
            with client.get_queue_sender(queue_name) as sender:
                
                addr1 = socket.gethostbyname_ex(env_conn)
    
                
                message = "nslookup: "+str(addr1[2])
                print(message)
                logger.info(message)

                # Sending a single message
                single_message = ServiceBusMessage("Single message")
                sender.send_messages(single_message)

                # Sending a list of messages
                messages = [ServiceBusMessage("First message"), ServiceBusMessage("Second message")]
                sender.send_messages(messages)
                print("Sent messages")
                logger.info("Sent messages")
                time.sleep(5)
