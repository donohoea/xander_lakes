FROM python:3.7
RUN apt-get update && apt-get install -qy binutils libproj-dev gdal-bin nodejs npm redis-server
RUN apt-get update
WORKDIR /app
COPY ./backend /app/backend
COPY ./frontend /app/frontend
COPY  ./requirements.txt ./clean.sh ./build.sh /app/
RUN pip install -r requirements.txt
RUN npm install ./frontend
RUN bash ./clean.sh
RUN bash ./build.sh
ENTRYPOINT python3 -u backend/manage.py runserver 0.0.0.0:80
EXPOSE 80
