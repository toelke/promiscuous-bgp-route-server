FROM python:3.15.0a8

RUN pip --no-cache-dir install ryu
COPY promiscuous-rs.py /
ENTRYPOINT ["python", "/promiscuous-rs.py"]
