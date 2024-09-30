# Fever challenge

## Requirements

- Make
- Docker
- Docker Compose
- Available ports 5000, 5432, 6379

## Decision making

- I've decided to use Flask for this challenge as it is a fast and easy to use framework to build a rest API.
- As a testing suite I decided to use pytest as I had some experience with it. I included only unit tests in this challenge as it was time consuming to prepare the environment also for functional tests.
- The chosen architecture is DDD to maintain clear separation of the framework with the business logic. I also apply the repository pattern to maintain separation of concerns and in case the future either the db, the cache or the provider changes the use cases don't need to be modified.
- To persist the events I've chosen PostgreSQL in prevision that this service could be expanded with relations, but as it is a MongoDB or DynamoDB would be also a valid approach.
- I created a Flask command that retrieves the events from the provider and stores them in the database in background.
- For the extra mile I included redis in the project working as an LRU. I create a hashed key based on the date range and store the results from the database there, so requests with already queried date ranges will be obtained without need to hit the database. I set the keys with a ttl of 60 seconds so results don't get inconsistent with the database in case of updates.
- The project is fully dockerized so it can run in any host.

The project is structured in 3 folders:
- **api**: Files related with the Flask application itself, bootstraps the services and initializes the endpoint
- **contexts**: Here are the different bounded contexts, in this case there's just an events bounded contexts. In each context there's a folder for each layer.
    - **Application**: Here's the use cases for the events context
    - **Domain**: Here's the aggregate root, value objects, and needed interfaces
    - **Infrastrucure**: Here's the implementation of the persistence repository, the cache repository, and the event provider 
    - **Presentation**: Here's the controllers in charge of transforming the data to adequate responses
- **shared**: In this folder I put all things that could be used in any contexts


## Real life considerations

### Better endpoint

In a real life scenario this endpoint should come also with pagination, being the design something like this:

- **Endpoint:** `GET /events/`
- **Query Parameters:**
  - `starts_at`: (string, required) The start datetime for filtering events (ISO 8601 format).
  - `ends_at`: (string, required) The end datetime for filtering events (ISO 8601 format).
  - `page`: (integer, optional) The page number for pagination.
  - `pageSize`: (integer, optional) The number of items per page.
  - `sortBy`: (string, optional) The field to sort the results by.
  - `sortDir`: (string, optional) The direction to sort the results (`asc` or `desc`).

- **Response:**
  - **200 OK:** page, pageSize, totalRows, totalPages, list of events
  - **404 Not Found:** If no events are found for the given date range.
  - **400 Bad Request:** If the query parameters are invalid.
  - **500 Internal Server Error:** In case of server error

With this design in mind and considering the possible extension of this endpoint with new parameters (category, city, etc), I would also implement for the repository the Criteria pattern (https://github.com/jperdior/user-service/blob/main/internal/user/domain/repository.go)

### Fetching from providers

Instead of a command running constantly in a container, a better approach would be to have a lambda on AWS that runs X times per day and publishes on any message broker (sqs, rabbitmq, etc) the fetched events so they can be consumed, processed and updated. Several consumers should be set up in order to process the amount of events in a realistic time. It could have been developed locally using localstack+terraform but I time-prioritized other things in this challenge.

### Scaling and rate limit

Aside of including an LRU cache between the database and the application, being a stateless service it should be scaled horizontally by using k8s, or aws ecs to ensure availability.

Also to prevent abuse and ensure stability a rate limiting system like an nginx reverse proxy or aws api gateway should be used.

## Observability

All relevant logging should be stored in some platform like Grafana, Datadog or Sentry. Alerts should be configured in case of errors and an integration with Slack/Teams would be advisable.

## CICD Pipelines

I like to work with githooks that ensure at least lint and static analysis has been run before pushing to the feature branch and of course a pipeline running also lint, analysis and tests should be set up.