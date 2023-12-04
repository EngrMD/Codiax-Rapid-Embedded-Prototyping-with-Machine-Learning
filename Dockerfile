# Stage 1: Build Stage
FROM python:3.10 AS builder

# Install build dependencies
RUN apt-get update && \
    apt-get install -y python3-pip libgl1-mesa-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /usr/src

# Copy only the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --user --no-cache-dir -r requirements.txt

# Stage 2: Final Stage
FROM python:3.10-slim

# Copy the installed dependencies from the builder stage
COPY --from=builder /root/.local /root/.local

ENV PATH=/root/.local/bin:$PATH
ENV LD_LIBRARY_PATH=/usr/lib:$LD_LIBRARY_PATH

# Set the working directory
WORKDIR /usr/src

# Copy the application code
COPY fingers/test ./fingers/test
COPY models/fingers_model_checkpoint.h5 ./models/fingers_model_checkpoint.h5
COPY *.py ./

