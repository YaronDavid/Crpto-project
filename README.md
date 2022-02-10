# Crpto-project
A proyect for protect grades uploaded by teachers
La carpeta "Profesor1" tiene el codigo para producir las calificaciones cifradas y las llaves publicas y privadas así como la firma digital del profesor.
La carpeta "Gestion" tiene el codigo para producir las llaves publicas y privadas del jefe de gestion, tambien tiene las opciones para cifrar las calificaciones 
del profesor para enviarlas a la carpeta nube, para estos pasos previamente se tendra que haber validado la firma del profesor, tambien crea un archivo cifrado para que el
director sea el unico capaz de acceder a ese archivo y finalmente puede firmar las calificaciones para enviarlas a la carpeta "Director"
La carpeta direcctor unicamente puede validar la firma de Gestion y decifrar el archivo de la carpeta "nube"
La carpeta nube no tiene ningun codigo
Las carpetas buscan ser una simulación de los equipos que usarian los agentes que le dan nombre a la carpeta
Los algoritmos usados en este proyecto fueron AES con un modo de operación CFB y SHA256 como algoritmo Hash
