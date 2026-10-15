
# Voting App — DevOps Capstone Project

A multi-service voting application used to practise Docker, Kubernetes, Helm, Terraform, CI/CD, and observability.

## Table of Contents

- [Project Objectives](#project-objectives)
- [Application Architecture](#application-architecture)
- [Prerequisites](#prerequisites)
- [Run with Docker Compose](#run-with-docker-compose)
- [Deploy with Kubernetes](#deploy-with-kubernetes)
- [Deploy with Helm](#deploy-with-helm)
- [Upgrade and Roll Back](#upgrade-and-roll-back)
- [Terraform Infrastructure](#terraform-infrastructure)
- [GitHub Actions CI](#github-actions-ci)
- [Security and Reliability](#security-and-reliability)
- [Observability and SRE Roadmap](#observability-and-sre-roadmap)
- [Project Status](#project-status)

## Project Objectives

1. Run and understand a multi-service application.
2. Deploy application components to Kubernetes.
3. Package and manage deployments with Helm.
4. Define cloud infrastructure using Terraform.
5. Validate infrastructure and deployment configuration using GitHub Actions.
6. Extend the project with observability and Site Reliability Engineering (SRE).

## Application Architecture

![Voting application architecture](architecture.excalidraw.png)

The application consists of:

| Component | Purpose |
|---|---|
| Vote | Python web application that accepts votes |
| Redis | Queues submitted votes |
| Worker | Processes votes and stores results |
| PostgreSQL | Stores voting data |
| Result | Node.js application that displays results |

The delivery workflow uses Terraform for infrastructure configuration, Helm for Kubernetes deployments, and GitHub Actions for automated validation.

## Prerequisites

Install the tools required for your chosen workflow:

- Git
- Docker Engine and Docker Compose
- kubectl
- Minikube for local Kubernetes
- Helm
- Terraform
- AWS CLI and an appropriately configured AWS profile for future AWS provisioning

## Run with Docker Compose

From the repository root:

```bash
docker compose up -d
docker compose ps
```

Open:

- Voting application: http://localhost:8080
- Results application: http://localhost:8081

View logs:

```bash
docker compose logs --tail=100
```

Stop the application:

```bash
docker compose down
```

Use `docker compose down -v` only when you intentionally want to delete the associated volumes and their data.

## Deploy with Kubernetes

The original Kubernetes manifests are in `k8s-specifications/`.

```bash
kubectl apply -f k8s-specifications/
kubectl get deployments,services,pods
```

The original manifest setup uses NodePorts 31000 for voting and 31001 for results. Availability depends on the cluster and service configuration.

To remove the resources created by those manifests:

```bash
kubectl delete -f k8s-specifications/
```

## Deploy with Helm

The custom Helm chart is located in `voting-app/`.

Validate and render it:

```bash
helm lint ./voting-app
helm template voting-app ./voting-app --namespace voting-helm
```

Install or upgrade the release on the intended Kubernetes cluster:

```bash
helm upgrade --install voting-app ./voting-app \
  --namespace voting-helm \
  --create-namespace
```

Inspect the release:

```bash
helm status voting-app -n voting-helm
helm history voting-app -n voting-helm
kubectl get deployments,services,pods -n voting-helm
```

In the tested local Helm setup, the configured NodePort endpoints are:

- Voting application: http://localhost:31010
- Results application: http://localhost:31011

These endpoints depend on the local cluster and current chart configuration.

## Upgrade and Roll Back

After changing the chart or its values, validate and upgrade:

```bash
helm lint ./voting-app
helm upgrade voting-app ./voting-app -n voting-helm
helm history voting-app -n voting-helm
```

To roll back, first inspect the history:

```bash
helm history voting-app -n voting-helm
```

Replace `<REVISION>` with the revision you want to restore:

```bash
helm rollback voting-app <REVISION> -n voting-helm
```

Verify the release:

```bash
helm status voting-app -n voting-helm
kubectl get pods -n voting-helm
```

A Helm rollback restores a previous release configuration. It does not automatically reverse database changes or restore lost persistent data.

## Terraform Infrastructure

Terraform configuration is maintained in `terraform/`.

The current configuration defines an AWS infrastructure baseline that includes an Ubuntu AMI, default VPC/subnet discovery, security-group rules, and an EC2 instance.

Validate the configuration:

```bash
cd terraform
terraform fmt -check -recursive
terraform init -backend=false -input=false
terraform validate
cd ..
```

Terraform validation has passed locally. The AWS infrastructure has **not yet been provisioned**.

Before provisioning, review the target account, region, instance costs, access rules, key pair, credentials, and Terraform plan. Do not run `terraform apply` until the planned changes have been reviewed and explicitly approved.

Never commit Terraform state files or sensitive variable files.

## GitHub Actions CI

The workflow is:

`.github/workflows/validate-capstone.yml`

It runs on relevant pushes to `main`, pull requests targeting `main`, and manual workflow dispatches.

The workflow checks:

**Terraform**
- Formatting
- Provider initialization without a backend
- Configuration validation

**Helm**
- Chart linting
- Kubernetes manifest rendering

These jobs validate configuration; they do not deploy the application or create AWS resources.

View workflow runs:

https://github.com/mudiafirm/example-voting-app-Ptsa-HcaP/actions

A green check indicates a successful workflow run. Inspect individual job logs if a later run fails.

## Security and Reliability

This project is a learning environment and is not yet production-ready.

Before production use:

- Avoid storing real database passwords in plain-text values files.
- Use Kubernetes Secrets or an appropriate secrets manager.
- Restrict administrative access and publicly exposed ports.
- Use persistent storage where application data must survive pod replacement.
- Apply least-privilege access to AWS and Kubernetes.
- Add health checks, resource requests, and resource limits.
- Plan and test database backups and recovery.
- Review image versions and GitHub Actions dependencies.

## Observability and SRE Roadmap

Planned work includes:

- Metrics and dashboards.
- Centralized logs and useful error searches.
- Alerting for service failures.
- Service-level indicators (SLIs) and service-level objectives (SLOs).
- Error-budget policy and incident-response procedures.
- Incident drill, postmortem, and recovery testing.

These items should be marked complete only after implementation and testing.

## Project Status

| Deliverable | Status |
|---|---|
| Forked application repository | Completed |
| Docker Compose application | Tested |
| Kubernetes deployment on Minikube | Tested |
| Helm chart validation | Passed |
| Helm upgrade and rollback | Tested |
| Terraform configuration | Validated and committed |
| GitHub Actions validation workflow | Passing |
| AWS infrastructure provisioning | Not yet performed |
| Observability and SRE | Planned |

Update this table as new deliverables are implemented and verified.
