FROM python:3.12.2-slim

ENV USER=app
ENV APP_DIR=/home/subapi \
    # Set output directly to terminal
    PYTHONUNBUFFERED=1 \
    # Disable creating of .pyc files
    PYTHONDONTWRITEBYTECODE=1

# Set working directory to root directory
WORKDIR $APP_DIR

# Install packages
COPY ["requirements.txt",  "$APP_DIR/"]
RUN pip install -r requirements.txt && \
    addgroup --system $USER && adduser --system --group $USER

RUN chown -R "$USER":"$USER" $APP_DIR
USER $USER

CMD ["bash", "-c", "uvicorn app.main:app --reload --port 8000 --host 0.0.0.0"]