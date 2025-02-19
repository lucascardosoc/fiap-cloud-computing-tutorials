import json
import boto3
from sqsHandler import SqsHandler
from datetime import datetime
from boto3.dynamodb.conditions import Key
from baseDAO import BaseDAO

def handlerS3(event, context):
    print (json.dumps(event))
    # Acessar a chave `key` do evento
    chave_key = event['Records'][0]['s3']['object']['key']
    
    # Dividir a chave em partes
    partes = chave_key.split('/')
    pedido = partes[1].split('-')[0]
    nome = partes[1].split('-')[1]
    
    # Gerar o JSON de resultado
    resultado = {
        "pedido": pedido,  # '394'
        "datetime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),  # Data e hora atual
        "cliente": nome,  # 'natalia'
        "status": partes[0]  # 'pronto'
    }
    
    if partes[0] == 'pronto':
        sqs = SqsHandler ("https://sqs.us-east-1.amazonaws.com/177870780625/pronto-pizzaria")
    else:
        sqs = SqsHandler ("https://sqs.us-east-1.amazonaws.com/177870780625/em-preparacao-pizzaria")
        
    sqs.send(str(resultado))
        
    return event
    
def handlerPreparacao(event, context):
    print (json.dumps(event))
    body = event["Records"][0]["body"].replace("'", "\"")
    print(body)
    event_json = json.loads(body)
    dao = BaseDAO('pedidos-pizzaria')
    dao.put_item(event_json)
    
    return event
    
def handlerPronto(event, context):
    print (json.dumps(event))
    body = event["Records"][0]["body"].replace("'", "\"")
    print(body)
    event_json = json.loads(body)
    dao = BaseDAO('pedidos-pizzaria')
    dao.put_item(event_json)
    
    return event