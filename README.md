# Subscription API

## What this project is

This project is a FastAPI-based subscription service that lets users sign up, authenticate, manage topics and subscriptions, and retrieve items collected from external sources.

The application also includes a periodic cleanup task to keep stored items limited per source, and it is set up to run locally with Docker Compose.

## Endpoints

POST /api/auth/signup - User registration
POST /api/auth/login - User login
POST /api/auth/refresh_token - Token refresh
DELETE /api/user/ - Delete current user

GET /api/topic/ - Get all topics
POST /api/topic/ - Create topic
DELETE /api/topic/{topic_name} - Delete topic

GET /api/subscription/ - Get user subscriptions
POST /api/subscription/ - Create subscription
DELETE /api/subscription/{topic_name} - Delete subscription

GET /api/item/ - Get items
GET /api/item/subscribed/ - Get items from subscribed topics

POST /api/webhook/{source} - Receive webhook payload for a source

## Startup with docker-compose:
### Environment variables:

- Find next files:
    - `.env.sample` - where you should define environment (local, dev, prod);
    - `.env.local.sample` - example of actual envs for local environment .
- Replace them with files without `.sample` suffix and populate with your credentials.
---
### Docker-compose:
To startup whole app run this command in root directory of repository:
```sh
docker compose up
```
Wait for everything to boot up.
- Application API documentation http://localhost:8000/docs/.
___
### Get started:

* Signup
* Login and obtain pair of access and refresh tokens
* Authorize in API documentation by clicking `Authorize`
* Use the API
