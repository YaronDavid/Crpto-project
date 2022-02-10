import base64
import codecs
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from os import name

def generate_key(id):
    qwerty = RSA.generate(1024)

    keypublic = qwerty.publickey()
    keypublicPEM = keypublic.exportKey()
    f = open('Public_Key_RSA_'+id+'.pem','wb')
    f.write(keypublicPEM)
    f.close()

    keyprivatePEM = qwerty.exportKey()
    f = open('Private_Key_RSA_'+id+'.pem','wb')
    f.write(keyprivatePEM)
    f.close()

x=0
while x==0:
    print("\nBuenas profesor, ¿Qué desea hacer")
    print("1.- Generar llaves\n2.- Firmar \n3.- Exit")
    menu = int(input('Elige una opcion: '))

    if menu !=3:
        if menu==1:
            id = input('Escriba un identificador para el par de llaves: ')
            generate_key(id)
        elif menu==2:
            #leemos el texto 
            filename = input('Escriba el nombre del archivo de calificaciones: ')
            f = open(filename+'.txt', 'rb')
            text = f.read()
            f.close()

            #convertir a b
            #text = text.encode("utf-8")
            #text = base64.b64decode(text)

            #leemos llave privada2
            filename = input('Escriba el nombre del archivo de su clave privada RSA: ')
            private_key = RSA.import_key(open(filename+".pem").read())

            #firmamos 
            h = SHA256.new(text)
            signature = pkcs1_15.new(private_key).sign(h)

            #guardamos firma
            name = input('Escriba el nombre del archivo para guardar la firma digital: ')
            file = open(name+'.pem', 'w')
            signature = base64.b64encode(signature)
            signature = signature.decode("utf-8")
            file.write(signature)
            file.close()
    else:
        x=3
print("Adios")

