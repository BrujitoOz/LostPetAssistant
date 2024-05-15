# Lost Pet Assistant
## Un chatbot widget para sitios web que ayuda a registrar mascotas perdidas de manera rápida y sencilla.

### Notas:
* Esta es una prueba de concepto para demostrar el potencial de automatización con los modelos LLM y el uso de function calling.
* Dado que no está destinado para producción, se utilizó Ngrok para exponer públicamente los endpoints y permitir que la plataforma Voiceflow pueda consumirlos.
* Se requiere tener acceso al API de OpenAI para usar su modeo GPT-4o.
* Se requiere una cuenta en Airtable con al menos una tabla en su workspace, junto con un token de autorización de su API y la URL para crear registros.

### Test en VoiceFlow
* El chatbot maneja una conversación con lenguaje natural con el usuario
* Pide al usuario brindar la información requerida como detalles de la mascota, e información de contacto
* Se registra la mascota en la base de datos

![](https://github.com/BrujitoOz/LostPetAssistant/blob/main/assets/pet.gif)


### Integración en un sitio web usando javascript: 
El chatbot puede integrarse en cualquier sitio web utilizando JavaScript. Puedes personalizar el diseño para adaptarlo a tus necesidades, incluyendo el color, imagen del avatar y descripción.
![petfinder_integration](https://github.com/BrujitoOz/Petfinder-ChatBot-with-Actions/assets/54969025/d73b87ee-1688-4a35-9e60-b04bf1a09d57)
![petfinder_integration_2](https://github.com/BrujitoOz/Petfinder-ChatBot-with-Actions/assets/54969025/c584dc87-282f-4732-af7d-80745edfee23)
![petfinder_integration_3](https://github.com/BrujitoOz/Petfinder-ChatBot-with-Actions/assets/54969025/98ad2451-d399-43a4-acfb-ac93cc277f57)
