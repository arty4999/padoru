FROM python:3.6
EXPOSE 80/tcp
LABEL name="padorubot"
ADD padoru-bot /
ADD requirements.txt /
RUN pip install -r requirements.txt
VOLUME ["padoru-bot"]
CMD [ "python", "./padorubot.py" ]
