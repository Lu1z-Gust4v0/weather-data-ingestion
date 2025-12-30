# Use a slim python image
FROM python:3.12-slim

# Install system dependencies (cron + build tools if needed)
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# Install Poetry
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN pip install poetry

WORKDIR /app

# Copy configuration files
COPY pyproject.toml ./
# If you have a poetry.lock, copy it too
COPY poetry.lock ./

# Install dependencies without creating a virtualenv 
# (Easier for Cron to find the global python path)
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Copy the rest of the code
COPY src/ ./src/

# Create the cron job file
# '0 * * * *' = Every hour
# We export PATH so the job can find python, and redirect output to /proc/1/fd/1 
# This trick sends cron logs to the Docker container's STDOUT
# Change '0 * * * *' to '* * * * *' for once-per-minute execution
RUN echo "0 * * * * . /etc/environment; cd /app && /usr/local/bin/poetry run start >> /proc/1/fd/1 2>&1" \
    > /etc/cron.d/weather-cron && \
    chmod 0644 /etc/cron.d/weather-cron && \
    crontab /etc/cron.d/weather-cron

# Create an entrypoint script to keep the container alive
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Healthcheck: Verify that the cron process is running
HEALTHCHECK --interval=1m --timeout=3s --start-period=5s --retries=3 \
    CMD pgrep cron || exit 1

ENTRYPOINT ["/entrypoint.sh"]