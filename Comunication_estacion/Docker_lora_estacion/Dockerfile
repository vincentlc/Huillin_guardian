# We use the official `python` image as base.
FROM python:3.11

# Copy the python script into the image
# Syntax: `COPY [SOURCE] [DESTINATION]`
COPY read_string_send_mqtt.py /app/read_string_send_mqtt.py

# We need to run commands while building the image
# This will install the `requests` package so we can use it in script.py
COPY requirements.txt /usr/share/requirements.txt
RUN pip3 install -r /usr/share/requirements.txt

RUN mkdir /usr/Downloads/
COPY RPi.GPIO-0.7.1.tar.gz /usr/Downloads/RPi.GPIO-0.7.1.tar.gz

#install the package to install rpi
#RUN yum update -y
#RUN yum groupinstall 'Development Tools' -y

#RUN dpkg -i /usr/Downloads/RPi.GPIO-0.7.1.tar.gz
RUN pip3 install  /usr/Downloads/RPi.GPIO-0.7.1.tar.gz

# The command is executed when the container starts
CMD ["python3", "-u", "/app/read_string_send_mqtt.py"]
