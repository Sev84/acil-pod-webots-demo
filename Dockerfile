FROM cyberbotics/webots.cloud:R2025a-ubuntu22.04
ARG PROJECT_PATH=/webots-project
RUN mkdir -p "$PROJECT_PATH"
COPY . "$PROJECT_PATH"
