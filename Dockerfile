FROM python:3.11.3-slim
WORKDIR /code

# Only requirements.txt file, so we can leverage cache later and save big time.
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Then the app.
COPY ./app /code/app
ENV PYTHONPATH=/code/app

# Entrypoint.
CMD ["uvicorn", "app.backend:app", "--host", "0.0.0.0", "--port", "80"]