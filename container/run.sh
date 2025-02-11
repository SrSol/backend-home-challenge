#!/bin/bash

# Agregar el directorio src al PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/opt/app"

# Ejecutar la aplicación desde el módulo correcto
uvicorn src.main:app --host 0.0.0.0 --port 8000
