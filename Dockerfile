FROM python:3

RUN pip install ryu
ADD promiscuous-rs.py /
ENTRYPOINT ["python", "/promiscuous-rs.py"]
