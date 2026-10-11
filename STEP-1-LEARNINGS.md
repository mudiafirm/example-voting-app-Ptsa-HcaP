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
