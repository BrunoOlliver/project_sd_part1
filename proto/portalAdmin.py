
from concurrent import futures
import logging
import grpc
import buffer_pb2
import buffer_pb2_grpc
import paho.mqtt.client as mqtt
import time

broker = "localhost"
client = mqtt.Client("admin")
print("connecting to broker")
client.connect(broker)

db = dict([])

class Greeter(buffer_pb2_grpc.GreeterServicer):

  def SayHello(self, request, context):
    return buffer_pb2.HelloReply(message='Hello, %s!' % request.name)

  def SayHelloAgain(self, request, context):
    return buffer_pb2.HelloReply(message='Hello again, %s!' % request.name)

  def insertNewClient(self, request, context):
    if request.id in db.keys():
      return buffer_pb2.HelloReply(message='Error! Already exists a client with ID = %s' % request.id)
    print("Inserting new Client "+request.name+" with ID = "+str(request.id))
    db[request.id] = request.name
    print(db)

    client.loop_start()
    print("\nPublishing message to topic","/data")
    client.publish("/data", payload="I,"+str(request.id)+","+str(db[request.id]))
    client.loop_stop()

    return buffer_pb2.HelloReply(message='Successfully created client with CID = %s!' % request.id)

  def updateClient(self,request,context):
    if request.id not in db.keys():
      return buffer_pb2.HelloReply(message='Error! Client with CID = %s not found.' % request.id)
    db[request.id] = request.name
    print(db)

    client.loop_start()
    print("\nPublishing message to topic","/data")
    client.publish("/data", payload="U,"+str(request.id)+","+str(db[request.id]))
    client.loop_stop()

    return buffer_pb2.HelloReply(message='Successfully updated client with CID = %s!' % request.id)

  def findClient(self, request, context):
    if request.id not in db.keys():
      return buffer_pb2.HelloReply(message='Error! Client with CID = %s not found.' % request.id)

    return buffer_pb2.HelloReply(message=db[request.id])

  def deleteClient(self, request, context):
    if request.id not in db.keys():
      return buffer_pb2.HelloReply(message='Error! Client with CID = %s not found.' % request.id)
    del db[request.id]

    client.loop_start()
    print("\nPublishing message to topic","/data")
    client.publish("/data", payload="D,"+str(request.id))
    client.loop_stop()

    return buffer_pb2.HelloReply(message='Successfully deleted client with CID = %s!' % request.id)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    buffer_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
