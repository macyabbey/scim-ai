FROM mcr.microsoft.com/devcontainers/java:17

# Install additional packages
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    curl \
    wget \
    jq \
    git \
    vim \
    unzip \
    htop \
    net-tools \
    httpie \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install GraalVM Native Image
RUN curl -L https://github.com/graalvm/graalvm-ce-builds/releases/download/jdk-17.0.8/graalvm-community-jdk-17.0.8_linux-x64_bin.tar.gz -o graalvm.tar.gz \
    && tar -xzf graalvm.tar.gz -C /opt \
    && rm graalvm.tar.gz

ENV GRAALVM_HOME=/opt/graalvm-community-openjdk-17.0.8+7.1
ENV PATH=$GRAALVM_HOME/bin:$PATH

# Install native-image
RUN gu install native-image && gu install python

# Install development tools
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g newman 