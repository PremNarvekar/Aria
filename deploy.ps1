# ARIA Deployment Script

param (
    [Parameter(Mandatory=$true)]
    [string]$RegistryUser
)

Write-Host "Building optimized images using docker-compose..."
docker-compose build

Write-Host "Tagging images for registry: $RegistryUser"
docker tag aria-api:optimized "$RegistryUser/aria-api:optimized"
docker tag aria-worker:optimized "$RegistryUser/aria-worker:optimized"
docker tag aria-frontend:optimized "$RegistryUser/aria-frontend:optimized"

Write-Host "Pushing images to Docker Hub..."
docker push "$RegistryUser/aria-api:optimized"
docker push "$RegistryUser/aria-worker:optimized"
docker push "$RegistryUser/aria-frontend:optimized"

Write-Host "Done! Update your k8s/deployment.yaml with $RegistryUser and run kubectl apply -f k8s/"
