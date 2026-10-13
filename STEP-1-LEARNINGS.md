# Step 1: Docker Compose Learning Notes

## Project
Docker Example Voting App

## Services
- vote: accepts votes
- redis: queues submitted votes
- worker: processes votes
- db: stores processed voting data
- result: displays voting results

## Practical Exercises
- Started the application using Docker Compose.
- Opened the voting page on localhost:8080.
- Opened the results page on localhost:8081.
- Inspected container status and logs.
- Stopped and restarted an individual service.
- Practiced inspecting networks, ports and volumes.

## Important Commands
- docker compose ps - shows running services
- docker compose logs - for investigate errors
- docker compose config - Check the configured storage and networking
- docker compose stop - stops containers but retains them.
- docker compose start - shows resource consumption
- docker compose down - stops and removes the Compose containers and network

## Lessons Learned
Docker Compose manages multiple services from one configuration.
Containers communicate using Docker networks.
Persistent database data must be stored in volumes.
Logs and health checks helps in troubleshooting service problems.

---

# Step 2: Kubernetes Learning Notes

## Objective
Deploy the Example Voting App to Kubernetes and understand how its components communicate.

## Kubernetes Components
- **Pod:** Runs application containers.
- **Deployment:** Maintains the desired number of Pods.
- **Service:** Provides a stable network endpoint for accessing Pods.
- **ClusterIP:** Allows internal cluster communication.
- **NodePort:** Exposes a Service through a port on the Kubernetes nodes.
- **Namespace:** Separates Kubernetes resources logically.

## Application Architecture
- **vote:** Accepts votes.
- **redis:** Queues submitted votes.
- **worker:** Processes votes.
- **db:** Stores processed voting data in PostgreSQL.
- **result:** Displays voting results.

## Practical Exercises
- Deployed all five application components.
- Verified Pods, Deployments and Services.
- Opened the voting page successfully.
- Opened the results page successfully.
- Used the separate `voting-app1` namespace for the original deployment.
- Used the separate `voting-helm` namespace for the Helm deployment.

## Important Commands
- `kubectl get pods` — Lists Pods.
- `kubectl get deployments` — Lists Deployments.
- `kubectl get services` — Lists Services.
- `kubectl apply -f FILE.yaml` — Applies Kubernetes manifests.
- `kubectl logs POD_NAME` — Displays container logs.
- `kubectl describe pod POD_NAME` — Shows Pod details and events.

## Lessons Learned
Kubernetes maintains the desired state of an application.
Deployments can recreate Pods when necessary.
Services provide stable endpoints for communication.
Namespaces separate resources, but NodePorts are shared across the cluster.
The application was tested successfully in Kubernetes.



---

# Step 3: Helm Learning Notes

## Objective
Package, deploy, upgrade and roll back the Kubernetes application using Helm.

## Important Concepts
- **Helm:** A package manager for Kubernetes.
- **Chart:** A collection of templates and configuration for Kubernetes resources.
- **Chart.yaml:** Stores chart metadata and version information.
- **values.yaml:** Stores configurable deployment values.
- **templates/:** Contains Kubernetes resource templates.
- **Release:** An installed instance of a Helm chart.
- **Revision:** A recorded version of a Helm release.

## Chart Details
- Chart name: `voting-app`
- Chart version: `0.1.0`
- Namespace: `voting-helm`
- Initial revision: `1`

## Practical Exercises
- Created a chart using `helm create`.
- Customized `Chart.yaml` and `values.yaml`.
- Created templates for five Deployments and four Services.
- Validated the chart with `helm lint`.
- Rendered Kubernetes YAML using `helm template`.
- Validated the manifests with a client-side dry run.
- Installed the chart in a separate namespace.
- Verified all five Pods were running.
- Opened the voting and results pages.
- Upgraded the Vote Deployment from one replica to two.
- Rolled back to the original one-replica configuration.
- Inspected the release history.

## Important Commands
- `helm lint voting-app` — Checks the chart and its templates.
- `helm template voting-app ./voting-app` — Renders manifests without deploying.
- `helm install voting-app ./voting-app -n voting-helm --create-namespace` — Installs a release.
- `helm list -n voting-helm` — Lists Helm releases.
- `helm history voting-app -n voting-helm` — Displays release history.
- `helm rollback voting-app 1 -n voting-helm` — Rolls back to revision 1.

## Upgrade and Rollback Results
- Revision 1: Initial installation with one Vote replica.
- Revision 2: Upgrade to two Vote replicas.
- Revision 3: Rollback to revision 1; Vote returned to one replica.

## Lessons Learned
Helm templates make Kubernetes resources configurable and reusable.
Helm upgrades change the desired release configuration.
Helm rollback restores an earlier configuration and creates a new revision.
Helm history preserves the record of release operations.
A successful deployment should be verified by checking Pods, Deployments and application access.

## Security and Reliability Improvements
- Move database credentials into Kubernetes Secrets.
- Replace temporary `emptyDir` database storage with persistent storage.
- Review container security settings and health probes.
- Treat the current configuration as a learning environment, not production-ready.

---

# Capstone Progress

- Step 1: Run locally with Docker Compose — completed.
- Step 2: Deploy the application to Kubernetes — completed.
- Step 3: Deploy with Helm — completed.
- Step 4: Practise Helm upgrade and rollback — completed.
- Next: Improve Kubernetes security and storage.
- Later: Provision a k3s server with Terraform and automate deployments with GitHub Actions.
