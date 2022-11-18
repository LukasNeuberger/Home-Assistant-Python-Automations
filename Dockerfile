FROM python:slim

ENV HOMEASSISTANT_DOMAIN=""
ENV HOMEASSISTANT_API_TOKEN=""
ENV DEBUG="False"

RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf && \
    pip install websockets

RUN useradd -c "ha-py-automations" \
    -d /home/ha-py-automations -m \
    -u 999 ha-py-automations
USER ha-py-automations:ha-py-automations
COPY . /home/ha-py-automations/
WORKDIR /home/ha-py-automations/

RUN mkdir Automations

VOLUME ["/home/ha-py-automations/Automations"]

CMD ["python", "Startup.py"]