FROM python:3

RUN pip install ryu
ADD promiscuous-rs.py /
CMD ["python", "/promiscuous-rs.py"]
