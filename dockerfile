FROM python

WORKDIR ./

copy . `/

RUN pip install -r requirement.txt

EXPOSE 80

CMD ["uvicorn", "app.main:app","--host","0.0.0.0"."--port" ]