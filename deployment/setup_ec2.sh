#!/bin/bash
# ===============================================
# NeoVault EC2 Initialization Script
# Run this on a fresh Ubuntu EC2 Instance
# ===============================================

# 1. Update packages
echo "Updating packages..."
sudo apt-get update -y
sudo apt-get upgrade -y

# 2. Install Docker
echo "Installing Docker..."
sudo apt-get install -y ca-certificates curl gnupg lsb-release
sudo mkdir -m 0755 -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update -y
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 3. Enable Docker and start it
echo "Starting Docker service..."
sudo systemctl enable docker
sudo systemctl start docker

# 4. Add current user to Docker group to run without sudo (requires logout/login to take full effect)
echo "Adding user to docker group..."
sudo usermod -aG docker $USER

# 5. Install Git
echo "Installing Git..."
sudo apt-get install -y git

# 6. Install Docker Compose (V2 is installed via plugin above, aliasing docker-compose)
echo "Setting up docker-compose alias..."
echo 'alias docker-compose="docker compose"' >> ~/.bashrc
source ~/.bashrc

echo ""
echo "=========================================================================="
echo "✅ EC2 Setup Complete!"
echo "NOTE: Please log out and log back in for the Docker group changes to apply."
echo "You can now clone the repository and run: docker-compose -f docker-compose.prod.yml up -d"
echo "=========================================================================="
