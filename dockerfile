FROM python:3.7
EXPOSE 5000
WORKDIR /project
ADD . /project
RUN pip install -r requirements.txt
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "5000"]