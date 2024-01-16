<h3 align="center">Django REST FrameWork Project on PostgreSQL database</h3>

## About The Project
I made this project to review its functionality, it allows you to run DRF project connected to PostgreSQL database, authorize new users, follow/unfollow their profiles and create, update, delete simple posts. To make it happen you need to create new user and authorize with access token or fill the forms


### Built With

This project utilize python packages, django and also has an option of saving data on external database

## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

Before you could you need to install Docker on your OS

<a href="https://docs.docker.com/desktop/install/linux-install/">Install Docker Desktop on Linux</a>

<a href="https://docs.docker.com/desktop/install/mac-install/">Install Docker Desktop on Mac</a>

<a href="https://docs.docker.com/desktop/install/linux-install/">Install Docker Desktop on Linux</a>

### Installation

1. Download archived file of source code

2. Unzip folder to wherever you need

3. Open terminal(or cmd on Windows) with path to unzipped files

4. Enter comands bellow into the terminal
   ```sh
   docker-compose up -d db
   ```
   ```sh
   docker compose build
   ```
   ```sh
   docker compose up
   ```
   This comands also download additional software automatically so it may take a while

 5. Open browser and proceed to 'localhost:8000/doc/' to swagger or 'localhost:8000/api/posta/' to proceed to home page  
