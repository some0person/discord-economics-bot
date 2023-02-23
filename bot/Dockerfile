FROM python:3-alpine
FROM gorialis/discord.py:minimal

RUN mkdir -p /usr/src/bot
WORKDIR /usr/src/bot

RUN pip3 install --upgrade pip
COPY . .
RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]