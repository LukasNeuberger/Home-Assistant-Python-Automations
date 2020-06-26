FROM python:slim

RUN useradd -c "ha-py-apps" \
    -d /home/ha-py-apps -m \
    -u 999 ha-py-apps
USER ha-py-apps:ha-py-apps
COPY . /home/ha-py-apps/
WORKDIR /home/ha-py-apps/

RUN pip install asyncws
RUN mkdir Apps

VOLUME ["/home/ha-py-apps/Apps"]

CMD ["python", "Startup.py"]