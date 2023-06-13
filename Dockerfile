# Download the latest image
FROM postgres

# Set the environment variables
ENV POSTGRES_USER ${DB_USER}
ENV POSTGRES_PASSWORD ${DB_PASSWORD}
ENV POSTGRES_DB ${DB_NAME}

# Define the port
EXPOSE 5432