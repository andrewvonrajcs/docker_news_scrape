FROM public.ecr.aws/lambda/python:3.8

COPY app.py   ./

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . . 

CMD ["app.handler"]