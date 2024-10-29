# Project:
This project aim to help local community to monitor the different parameter of the water.

# It is composed of several element:

1) A raspeberry pi 1 - 'modulo tierra', which recieve data trough LoRa and register them localy.
It also create a local AP (acces point), that broadcast the value of the read data.
Everything is control through nodered interface install.
The post is: `10.3.141.1:1880`
To see the user interface : `10.3.141.1:1880/ui`

2) A raspeberry pi 1 - 'modulo huellin', which concatenate the data from all the sensors and send it to the 'modulo tierra' through LoRa.
<details open>
<summary>
Current implemented sensors are:
</summary> <br />
###
- Oxygen
- PH
- Water quality
- GPS 
</details open>



3) The documentation of the project
![Diagrama general](Doc/Diagrama general.drawio.svg)



### Shortly will be added the diagram of the project and the rest of the source code

version 3.1.9 de node red