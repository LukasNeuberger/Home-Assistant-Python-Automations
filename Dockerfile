FROM python:slim

RUN useradd -c "ha-py-automations" \
    -d /home/ha-py-automations -m \
    -u 999 ha-py-automations
USER ha-py-automations:ha-py-automations
COPY . /home/ha-py-automations/
WORKDIR /home/ha-py-automations/

RUN pip install asyncws
RUN mkdir Automations

VOLUME ["/home/ha-py-automations/Automations"]

CMD ["python", "Startup.py"]