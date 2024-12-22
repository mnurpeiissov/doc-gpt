# Use PostgreSQL 15 as the base image
FROM postgres:15

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    postgresql-server-dev-15 \
    && rm -rf /var/lib/apt/lists/*

# Clone and install pgvector
RUN git clone --branch v0.5.1 https://github.com/pgvector/pgvector.git \
    && cd pgvector \
    && make \
    && make install

# Add SQL script to enable the extension
# Add a custom init script to enable the extension
COPY init-pgvector.sql /docker-entrypoint-initdb.d/

# Ensure the script runs with the proper permissions
RUN chmod 755 /docker-entrypoint-initdb.d/init-pgvector.sql
# Set environment variables
ENV POSTGRES_DB=vectordb
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
USER postgres
# Expose PostgreSQL port
EXPOSE 5432
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["postgres"]