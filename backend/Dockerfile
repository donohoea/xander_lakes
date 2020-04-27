FROM python:3.7
WORKDIR /app
COPY backend /app/backend/
COPY frontend /app/frontend/
COPY manage.py requirements.txt /app/
RUN pip install -r requirements.txt
RUN npm install
RUN ./clean.sh
RUN ./build.sh
EXPOSE 8000
