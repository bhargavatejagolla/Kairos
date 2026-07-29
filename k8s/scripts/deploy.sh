#!/bin/bash
set -e

ENV=${1:-local}
IMAGE_TAG=${2:-latest}
NAMESPACE="kairos"
ENV_FILE=".env"

echo "==========================================="
echo " Deploying KAIROS to [$ENV] environment"
echo " Image Tag: $IMAGE_TAG"
echo "==========================================="

if [ ! -f "$ENV_FILE" ]; then
    echo "Error: $ENV_FILE not found! We need this to generate Kubernetes secrets."
    exit 1
fi

# Ensure namespace exists
kubectl get namespace $NAMESPACE >/dev/null 2>&1 || kubectl create namespace $NAMESPACE

# Create or update the secret dynamically from the .env file
echo "Generating kairos-secrets from $ENV_FILE..."
kubectl create secret generic kairos-secrets \
    --namespace $NAMESPACE \
    --from-env-file=$ENV_FILE \
    --dry-run=client -o yaml | kubectl apply -f -

# Update Kustomize image tags
echo "Setting image tags in Kustomize..."
cd k8s/base
kustomize edit set image kairos-api=kairos-api:$IMAGE_TAG
kustomize edit set image kairos-app=kairos-app:$IMAGE_TAG
cd ../..

# Apply the Kustomize overlay
echo "Applying Kustomize overlay for $ENV..."
kubectl apply -k k8s/overlays/$ENV

echo "==========================================="
echo " Deployment triggered successfully!"
echo " Monitor rollout status with:"
echo " kubectl get pods -n $NAMESPACE -w"
echo "==========================================="
