import base64
import codecs
from Crypto import Signature
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

def generateKeys():
    key = get_random_bytes(16)
    return key

def EncriptRSA(data,Public_Key_RSA):
    #print(f"llave {data}")
    key = RSA.importKey(open(Public_Key_RSA+'.pem').read())
    cipher = PKCS1_OAEP.new(key)
    ciphertext = cipher.encrypt(data)
    #print(f"llave cifrada {ciphertext}")
    #ciphertext = cipher.encrypt(data.encode("utf-8"))

    c_name = input('Escriba un nombre para la llave cifrada: ')
    f = open(c_name+'.txt','w')
    ciphertext = base64.b64encode(ciphertext)
    #print(f"llave cifrada b64 {ciphertext}")
    ciphertext = ciphertext.decode("utf-8")
    #print(f"llave utf-8 {ciphertext}")
    f.write(ciphertext)
    f.close()

def EncriptCFB(plain:str, key):
    iv = get_random_bytes(16)
    plain = plain.encode("utf-8")
    aes = AES.new(key, AES.MODE_CFB, iv)
    cipher = aes.encrypt(plain)
    cipher = base64.b64encode(cipher)
    cipher = cipher.decode("utf-8")
    iv = base64.b64encode(iv)
    iv = iv.decode("utf-8")
    cipher = iv+cipher
    name = input("Escribe el nombre del archivo para las calificaciones: ")
    ci = open(name+'.txt','w')
    ci.write(cipher)
    ci.close()

def DecryptRSA(data,Private_Key_RSA):
    key = RSA.importKey(open(Private_Key_RSA+'.PEM').read())
    cipher = PKCS1_OAEP.new(key)
    text = cipher.decrypt(data)
    return text

def DecryptCFB(cipher:str, key:str):
    iv = cipher[:24]
    cipher = cipher[24:]
    cipher = cipher.encode("utf-8")
    cipher = base64.b64decode(cipher)
    iv = iv.encode("utf-8")
    iv = base64.b64decode(iv)
    other = AES.new(key, AES.MODE_CFB, iv)
    decoded = other.decrypt(cipher)
    decoded = decoded.decode("utf-8")
    nombre = input("Escriba nombre para alojar las calificaciones del profesor: ")
    decipher = open(nombre+'.txt','w')
    decipher.write(decoded)
    decipher.close()


x=0
verificacion=0
while x==0:
    print("\nBuen día Jefe, ¿Qué desea hace?")
    print("1.- Generar llaves\n2.- Verificar firma de Gestion\n3.- Leer calificaciones\n4.- Exit")
    menu = int(input('Elige una opcion: '))

    if menu !=5:
        if menu==1:
            id = input('Escriba un identificador para el par de llaves: ')
            generate_key(id)
            print("Claves generadas exitosamente")
        elif menu==2:
            #leemos firma
            filename = input('Escriba el nombre de la firma digital: ')
            with open(filename+'.pem', 'r') as file:
                signature = file.read()

            signature = signature.encode("utf-8")
            signature = base64.b64decode(signature)

            #leemos la llave publica RSA
            Public_Key_RSA = input('Escriba el nombre de la llave publica RSA de gestion: ')
            Public_Key = RSA.import_key(open(Public_Key_RSA+".pem").read())

            #leemos el archivo con las calificaciones
            filename = input('Escriba el nombre del archivo de calificaciones: ')
            with open(filename+'.txt', 'rb') as file:
                text = file.read()
            #convertir a b
            #text = text.encode("utf-8")
            #text = base64.b64decode(text)
           
            #hasheamos el texto jsjs
            h = SHA256.new(text)
            #verificamos firma
            try:
                pkcs1_15.new(Public_Key).verify(h, signature)
                print ("The signature is valid.")
                verificacion=1
            except (ValueError, TypeError):
                print ("The signature is not valid.")
                verificacion=0
        elif menu==3: 
            if(verificacion==0):
                print("Para realizar esta operación verifique la firma")
            elif(verificacion==1): 
            #leemos la llave de aes
                name = input("Escriba el nombre del archivo de la llave cifrada: ")
                f = open("../nube/"+name+".txt", "r")
                AES_c = f.read()
                f.close()
                AES_c = AES_c.encode("utf-8")
                AES_c = base64.b64decode(AES_c)
                #leemos la llave privada
                Private_Key = input("Escriba el nombre de su llave privada RSA: ")
                AES_Key = DecryptRSA(AES_c, Private_Key)
            #leemos el archivo de calificaciones cifradas
                name = input("Escribe el nombre del archivo de calificaciones cifrada: " )
                file = open("../nube/"+name+".txt", "r")
                cipher = file.read()
                file.close()
                DecryptCFB(cipher, AES_Key)
                print("Calificaciones decifradas")
    else:
        x=5
print("Bye")