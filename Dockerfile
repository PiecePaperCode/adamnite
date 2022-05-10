FROM python:3.10-bullseye

WORKDIR adamnite

# DEPENDENCYS
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# ADAMNITE
COPY src src
WORKDIR ./src
RUN python main_tests.py

# MAIN
CMD python main.py
