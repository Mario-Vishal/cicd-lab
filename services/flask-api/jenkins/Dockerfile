FROM jenkins/jenkins:lts-jdk17

USER root

# Install Docker CLI inside the Jenkins container
RUN apt-get update && apt-get install -y ca-certificates curl gnupg lsb-release \
  && mkdir -p /etc/apt/keyrings \
  && curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg \
  && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list \
  && apt-get update && apt-get install -y docker-ce-cli \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

# (Optional) Install basic tools you may want later
RUN apt-get update && apt-get install -y jq git make python3 python3-pip && rm -rf /var/lib/apt/lists/*

# Return to Jenkins user for safer operation
USER jenkins
