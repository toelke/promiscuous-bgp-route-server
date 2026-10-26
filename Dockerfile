FROM python:3.16.0a1

RUN pip --no-cache-dir install ryu
COPY promiscuous-rs.py /
ENTRYPOINT ["python", "/promiscuous-rs.py"]
