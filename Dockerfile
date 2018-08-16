FROM frolvlad/alpine-python3

RUN pip3 install \
    flask \
    bs4

COPY ./*.py /app/

WORKDIR /app

EXPOSE 8080

ENTRYPOINT ["python3"]
CMD ["local_webhook.py"]

