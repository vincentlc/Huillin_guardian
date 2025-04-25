# Proyecto: Huillin Guardian

Este proyecto tiene como objetivo ayudar a la comunidad local a monitorear diferentes parámetros del agua.

---

## Componentes

### 1. Raspberry Pi 1 - 'Estación'

- Recibe datos a través de LoRa y los registra localmente.
- Crea un Punto de Acceso (AP) local para transmitir los valores de los datos leídos.
- Controlado a través de una interfaz Node-RED.
  - Panel de Node-RED: [http://10.3.141.1:1880/ui](http://10.3.141.1:1880/ui)
  - Editor de Node-RED: [http://10.3.141.1:1880](http://10.3.141.1:1880)

### 2. Raspberry Pi 1 - 'Huillin'

- Agrega datos de todos los sensores y los envía a la 'Estación' a través de LoRa.

#### Sensores actualmente implementados:

<details open>
<summary>Haz clic para expandir</summary>

- Oxígeno
- pH
- Calidad del agua
- GPS

</details>

---

## Estructura de Carpetas

### `Communication_huillin/`

- Contiene el proceso de instalación para la Raspberry Pi 'Huillin'.
- Incluye los paquetes de Python necesarios y las librerías para los sensores.
- Contiene el código para interactuar con los diferentes sensores.
- Incluye código de prueba para validar la funcionalidad de los sensores.
- Consulta el archivo interno [`README.md`](Communication_huillin/README.md) en esta carpeta para más detalles.

### `Communication_estacion/`

- Contiene el proceso de instalación para la Raspberry Pi 'Estación'.
- Incluye scripts para configurar la comunicación LoRa y la interfaz Node-RED.
- Contiene archivos de configuración para el Punto de Acceso (AP) local.
- Consulta el archivo interno [`README.md`](Communication_estacion/README.md) en esta carpeta para más detalles.

### `Doc/`

- Contiene la documentación del proyecto, incluidos diagramas y la arquitectura del sistema.
- Ejemplo: `Diagrama general.drawio.svg` proporciona una visión general del sistema.

---

## Mejoras Futuras

- Posibilidad de agregar sensores adicionales.
- Reportes automatizados a plataformas de datos.

---

## Requisitos

- Versión de Node-RED: `3.1.9`

---

## Contacto

Para cualquier pregunta o soporte, por favor contacta a los mantenedores del proyecto.  
O a través de Instagram: [https://www.instagram.com/huillin.guardian/](https://www.instagram.com/huillin.guardian/)
