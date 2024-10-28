FROM python:3.9-slim
RUN pip install psutil
COPY load_test.py /app/load_test.py
WORKDIR /app
CMD ["python", "load_test.py"]
