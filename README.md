 Work in progress...
# Anime Tracker
App allows you to track your progress while watching anime in the number of episodes watched and ratings for it.

Inspired by [shikimori.one](https://shikimori.one/)

## Requirements

-   [Docker](https://www.docker.com/get-started)
-   [Docker Compose](https://docs.docker.com/compose/install/)
-   [GNU Make](https://www.gnu.org/software/make/)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/kreengg/anime-tracker.git
   cd anime-tracker
   ```
2. Create and configure `.env` file from `.env.example`(test section can be skipped)
3. Install all required packages in `Requirements` section.

## Running the Application

1. Start application in Docker Compose using Makefile

   ```bash
   make app
   ```
2. Apply database migrations
    ```bash
    make migrations
    ```
3. Access the API documentation:

   Open your browser and navigate to `http://127.0.0.1:8000/api/docs` to see the interactive API documentation provided by Swagger UI.
