@echo off
setlocal enabledelayedexpansion

REM List your microservice folders here:
set SERVICES=climate safety vision user dashboard federated nlp-qa gateway

REM Minimal Dockerfile content
set dockerfile_1=FROM python:3.10-slim
set dockerfile_2=WORKDIR /app
set dockerfile_3=COPY . .
set dockerfile_4=RUN pip install --no-cache-dir -r requirements.txt
set dockerfile_5=EXPOSE 8000
set dockerfile_6=CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

REM Minimal requirements.txt content
set requirements_1=fastapi
set requirements_2=uvicorn
set requirements_3=requests

REM Loop through all service folders
for %%S in (%SERVICES%) do (
    if exist "%%S" (
        if not exist "%%S\Dockerfile" (
            echo %dockerfile_1%> "%%S\Dockerfile"
            echo %dockerfile_2%>> "%%S\Dockerfile"
            echo %dockerfile_3%>> "%%S\Dockerfile"
            echo %dockerfile_4%>> "%%S\Dockerfile"
            echo %dockerfile_5%>> "%%S\Dockerfile"
            echo %dockerfile_6%>> "%%S\Dockerfile"
            echo Created Dockerfile in %%S
        )
        if not exist "%%S\requirements.txt" (
            echo %requirements_1%> "%%S\requirements.txt"
            echo %requirements_2%>> "%%S\requirements.txt"
            echo %requirements_3%>> "%%S\requirements.txt"
            echo Created requirements.txt in %%S
        )
        if not exist "%%S\main.py" (
            echo WARNING: main.py not found in %%S
        )
    ) else (
        echo WARNING: Directory %%S does not exist!
    )
)

echo All done!
pause
