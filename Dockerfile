# Download the latest image
FROM postgres

# Set the environment variables
ENV POSTGRES_PASSWORD 1234
ENV POSTGRES_DB postgres

# Define the port
EXPOSE 5432