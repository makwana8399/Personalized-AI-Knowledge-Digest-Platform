### Personalized-AI-Knowledge-Digest-Platform

Personalized-AI-Knowledge-Digest-Platform is an AI-powered platform that aggregates, processes, ranks, and delivers personalized knowledge content from multiple sources. It leverages web scraping, AI ranking, and scheduling to provide users with a tailored digest of information.

Table of Contents
#project-overview

Project Overview

Architecture & Project Flow

Folder Structure

Setup & Installation

Usage

Modules Description

Docker Setup

Logging & Monitoring

Scripts

Project Overview

This platform is designed to collect information from blogs, newsletters, and YouTube channels, process it using AI, rank it based on relevance, and provide a personalized digest. The project aims to save time and enhance knowledge acquisition by delivering curated content tailored to user interests.

Architecture & Project Flow

Data Ingestion (ingestion/):

Scrapes content from various sources: blogs, newsletters, and YouTube.

Persists the raw data into the database.

Processing (ai/processor.py & opennrout_client.py):

Preprocesses scraped content for AI processing.

Handles AI-based summarization and knowledge extraction.

Ranking (ranking/):

Ranks the processed content according to relevance and user preferences.

Scheduler (scheduler/cron.py):

Automates periodic content scraping, processing, and ranking tasks.

Database (database/):

Stores all raw and processed content, user data, and rankings.

Built with modular database access (db.py) and models (models.py).

Email Delivery (email/):

Sends the personalized digest to users via email.

Utilities (utils/):

Helper modules for handling topics, main processing workflows, and other recurring utilities.

Configuration & Logging (config/ & logs/):

Configures system parameters, logging settings, and app constants.

Folder Structure
Personalized-AI-Knowledge-Digest-Platform/
│
├─ app/
│   ├─ ai/                # AI processing and summarization
│   ├─ config/            # Configuration and settings
│   ├─ database/          # DB connection, models, and migrations
│   ├─ digest/            # Digest generation templates and logic
│   ├─ email/             # Email sending modules
│   ├─ ingestion/         # Scrapers for blogs, newsletters, YouTube
│   ├─ ranking/           # Content ranking logic
│   ├─ scheduler/         # Cron jobs for automation
│   ├─ utils/             # Utility functions and helpers
│   └─ main.py            # Entry point of the application
│
├─ docker/                # Docker setup files
├─ data/                  # Static or persisted data files
├─ logs/                  # Application logs
├─ scripts/               # Additional scripts for updating topics/users
├─ .env                   # Environment variables
├─ Dockerfile             # Docker image definition
├─ docker-compose.yml     # Docker compose setup
├─ requirements.txt       # Python dependencies
├─ alembic.ini            # Database migration tool configuration
└─ README.md              # This file

Setup & Installation

Clone the repository:

git clone https://github.com/yourusername/Personalized-AI-Knowledge-Digest-Platform.git
cd Personalized-AI-Knowledge-Digest-Platform


Create a virtual environment and activate it:

python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows


Install dependencies:

pip install -r requirements.txt


Configure environment variables in .env.

Usage

Run the application locally:

python app/main.py


Start the Dockerized version:

docker-compose up --build


Run periodic tasks using scheduler/cron.py.

Modules Description

ai/ – Handles content summarization, AI processing, and knowledge extraction.

database/ – Manages database connections, models, and migrations.

digest/ – Generates the final personalized digest content.

email/ – Sends digest emails to users.

ingestion/ – Scrapes content from blogs, newsletters, and YouTube.

ranking/ – Ranks content based on AI relevance and user interests.

scheduler/ – Automates scraping and digest sending.

utils/ – Common helper functions, topic handling, and main workflows.

Docker Setup

Dockerfile – Defines the image for running the app.

docker-compose.yml – Orchestrates services, including database and app container.

Build and run:

docker-compose up --build

Logging & Monitoring

Logs are stored in logs/.

Configure logging via config/logging.py.

Includes digest logs (digestlog) and script execution logs.

Scripts

scripts/backfill_topics.py – Backfills topics in the database.

scripts/update_user_interests.py – Updates user interests for better personalization.
