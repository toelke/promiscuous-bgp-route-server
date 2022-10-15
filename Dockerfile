FROM python:3.10.7

RUN pip --no-cache-dir install ryu
COPY promiscuous-rs.py /
ENTRYPOINT ["python", "/promiscuous-rs.py"]
