FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    unixodbc \
    unixodbc-dev \
    odbc-postgresql \
    && rm -rf /var/lib/apt/lists/*

RUN echo "[PostgreSQL]\n\
Description=ODBC for PostgreSQL\n\
Driver=/usr/lib/x86_64-linux-gnu/odbc/psqlodbca.so\n\
Setup=/usr/lib/x86_64-linux-gnu/odbc/libodbcpsqlS.so\n\
FileUsage=1" > /etc/odbcinst.ini

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app:create_app
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--reload", "--debugger"]