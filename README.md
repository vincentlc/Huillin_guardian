# Project: Huillin Guardian

This project aims to help the local community monitor different parameters of the water.

---

## Components

### 1. Raspberry Pi 1 - 'Estacion'

- Receives data through LoRa and registers it locally.
- Creates a local Access Point (AP) to broadcast the read data values.
- Controlled through a Node-RED interface.
  - Node-RED Dashboard: [http://10.3.141.1:1880/ui](http://10.3.141.1:1880/ui)
  - Node-RED Editor: [http://10.3.141.1:1880](http://10.3.141.1:1880)

### 2. Raspberry Pi 1 - 'Huillin'

- Aggregates data from all sensors and sends it to 'Estacion' via LoRa.

#### Current Implemented Sensors:

<details open>
<summary>Click to expand</summary>

- Oxygen
- pH
- Water Quality
- GPS

</details>

---

## Folder Structure

### `Communication_huillin/`

- Contains the installation process for the 'Huillin' Raspberry Pi.
- Includes required Python packages and wheels for the sensors.
- Contains the code for interfacing with the different sensors.
- Includes test code for validating sensor functionality.
- Refer to the internal [`README.md`](Communication_huillin/README.md) file in this folder for more details.

### `Communication_estacion/`

- Contains the installation process for the 'Estacion' Raspberry Pi.
- Includes scripts for setting up the LoRa communication and Node-RED interface.
- Contains configuration files for the local Access Point (AP).
- Refer to the internal [`README.md`](Communication_estacion/README.md) file in this folder for more details.

### `Doc/`

- Contains project documentation, including diagrams and system architecture.
- Example: `Diagrama general.drawio.svg` provides a high-level overview of the system.

---

## Future Enhancements

- Posibility to add extra sensor
- Automated report to data platforms

---

## Requirements

- Node-RED version: `3.1.9`

---

## Contact

For any questions or support, please contact the project maintainers.
Or this instagram : https://www.instagram.com/huillin.guardian/
