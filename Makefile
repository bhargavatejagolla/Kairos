# KAIROS Enterprise Makefile

CLUSTER_NAME=kairos
NAMESPACE=kairos
IMAGE_TAG=$(shell git rev-parse --short HEAD 2>/dev/null || echo "latest")

.PHONY: help build deploy-local deploy-prod destroy logs restart port-forward

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Build frontend and backend Docker images
	@echo "Building Backend Image (Tag: $(IMAGE_TAG))..."
	cd backend && docker build -t kairos-api:$(IMAGE_TAG) .
	@echo "Building Frontend Image (Tag: $(IMAGE_TAG))..."
	cd frontend && docker build -t kairos-app:$(IMAGE_TAG) .

import-images: build ## Import built images into k3d cluster
	@echo "Importing images into k3d cluster $(CLUSTER_NAME)..."
	k3d image import kairos-api:$(IMAGE_TAG) -c $(CLUSTER_NAME)
	k3d image import kairos-app:$(IMAGE_TAG) -c $(CLUSTER_NAME)

deploy-local: import-images ## Deploy to local k3d cluster using Kustomize
	@echo "Deploying to Local Cluster..."
	./k8s/scripts/deploy.sh local $(IMAGE_TAG)

deploy-prod: ## Deploy to production cluster using Kustomize
	@echo "Deploying to Production Cluster..."
	./k8s/scripts/deploy.sh production $(IMAGE_TAG)

destroy: ## Tear down the Kubernetes deployment
	@echo "Destroying KAIROS deployment in namespace $(NAMESPACE)..."
	kubectl delete kustomization -k k8s/overlays/local --ignore-not-found=true
	kubectl delete namespace $(NAMESPACE) --ignore-not-found=true

logs: ## Tail logs for the backend API
	kubectl logs -n $(NAMESPACE) -l app=backend -f

restart: ## Perform a rolling restart of the backend deployment
	kubectl rollout restart deployment/backend -n $(NAMESPACE)
	kubectl rollout restart deployment/worker -n $(NAMESPACE)

port-forward: ## Port forward the ingress or services for local testing
	@echo "Forwarding API to http://localhost:8000 and App to http://localhost:3000"
	@echo "Run these in separate terminals if needed."
	kubectl port-forward -n $(NAMESPACE) svc/backend 8000:8000 &
	kubectl port-forward -n $(NAMESPACE) svc/frontend 3000:80 &
