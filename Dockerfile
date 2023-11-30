FROM python:3.8

WORKDIR /src

COPY ./backend /src

RUN pip install -r requirements.txt

# EXPOSE 5000

CMD ["gunicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]


# Quando o docker estiver instalado (versão pra windows), você executar o seguinte:
# docker build -t backend .
# docker run -p 5000:5000 backend

