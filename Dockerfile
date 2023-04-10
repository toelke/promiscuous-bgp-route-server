FROM python:3.11.3

RUN pip --no-cache-dir install ryu
COPY promiscuous-rs.py /
ENTRYPOINT ["python", "/promiscuous-rs.py"]
