FROM python:3.11.2

# Set the working directory
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# Copy the model file into a specific directory within the container
COPY prophet_model.pkl /usr/src/app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]



# # Etapa 1: Construcción del frontend de Angular
# FROM node:18 AS build-frontend

# # Establecer el directorio de trabajo para el frontend
# WORKDIR /usr/src/app/frontend

# # Copiar los archivos de Angular
# COPY frontend/package.json ./

# # Instalar dependencias de Angular
# RUN npm install

# # Copiar el código de Angular
# COPY . .

# # Construir la aplicación de Angular
# RUN npm run build --prod

# FROM nginx:1.21.3

# COPY --from=build-frontend /usr/src/app/frontend/dist/frontend /usr/share/nginx/html

# # Etapa 2: Construcción del backend (API)
# FROM python:3.11.2 AS build-backend

# # Establecer el directorio de trabajo para el backend
# WORKDIR /usr/src/app

# # Copiar los archivos de requerimientos
# COPY requirements.txt ./

# # Instalar dependencias de Python
# RUN pip install --no-cache-dir -r requirements.txt

# # Copiar el código del backend
# COPY . .

# # Copiar los archivos construidos de Angular (etapa 1) al backend
# COPY --from=build-frontend /usr/src/app/frontend/dist /usr/src/app/frontend/dist


# # Comando para arrancar la API y nginx
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]