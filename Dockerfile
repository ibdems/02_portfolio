
FROM python:3.12-bookworm

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

RUN groupadd -r app && useradd -r -g app app

RUN apt update && apt install -y --no-install-recommends build-essential \
gcc libpq-dev libc-dev pkg-config

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
# Copy the source code into the container.
COPY . .
RUN chown -R app:app /app
# Expose the port that the application listens on.
EXPOSE 8080

# Run the application.
CMD ["uvicorn", "portfolio.asgi:application", "--host", "0.0.0.0", "--port", "8080"]
