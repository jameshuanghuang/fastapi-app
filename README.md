### fastapi, github CICD, dockerhub, render.com

MVP of option calculator using fastapi \
Visit [Option Calculator](https://fastapi-app-o4e5.onrender.com) hosted by Render \
Visit [Render](https://render.com/) for pricing. The free-tier option includes cold starts.

***
The CI/CD workflow is as follows:
1. GitHub tracks changes to the repository and triggers the workflow.
2. The workflow builds a Docker image and pushes it to Docker Hub using credentials stored in GitHub Repo Secrets.
3. Render pulls the updated Docker image from Docker Hub and deploys the application.
***

Commands
> uvicorn app.main:app --reload \
> docker build -t fastapi .  \
> docker build --no-cache -t fastapi . \
> docker run -p 8000:8000 fastapi \

endpoints [TBD]
- /docs - to see api docs
- /ml/prime - to guess if a number is prime

allow_origins=["*"] is not safe