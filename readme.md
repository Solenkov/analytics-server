# BFH Analytics Server

A lightweight, privacy-first analytics backend for collecting standardized usage data from websites and storing it in PostgreSQL for further analysis.

This repository contains the **server-side part** of our Project 1 prototype:
- a central analytics collector backend
- a PostgreSQL database for raw event storage
- a minimal deployment setup using Docker Compose

The current prototype is designed as a **first technical step** toward a shared analytics infrastructure for public-sector websites in Switzerland.

---

## 1. Why this project was created

The broader project goal is to explore whether multiple public-sector websites (for example cantonal and municipal websites) can participate in a common analytics solution and make their usage data comparable.

The main idea is not just to count visits, but to create a shared and standardized data basis that can later support:
- comparison between websites
- identification of optimization opportunities
- understanding of user behavior on websites and portals
- discussion of usefulness and effectiveness of digital public services

This repository focuses only on the **backend/data collection layer**.

---

## 2. What this repository contains

This repository provides the central analytics backend that receives events from a client-side tracking snippet and stores them in PostgreSQL.

Main components:

- **FastAPI collector backend**
  - exposes an endpoint for incoming analytics events
  - validates incoming payloads
  - writes them into PostgreSQL

- **PostgreSQL database**
  - stores raw event data in a simple and transparent schema

- **Docker Compose setup**
  - starts both the backend and the database

This is intentionally a **minimal prototype**, not a full analytics platform like Matomo.

---

## 3. Example integration

To make the prototype testable, the analytics backend is currently connected to a simple demo website.

In our test setup:

- one AWS EC2 instance hosts a simple demo website
- a small analytics snippet is embedded into that website
- the snippet sends `page_view` events to this analytics backend
- this backend stores those events in PostgreSQL

This allows us to demonstrate the full technical flow:

browser on website  
→ analytics snippet  
→ HTTP POST to collector backend  
→ insert into PostgreSQL

---

## 4. Current architecture

The current prototype uses two servers:

### Demo website server
Hosts a simple example website with the embedded analytics snippet.

### Analytics server
Runs:
- the collector backend
- PostgreSQL
- Docker Compose deployment

This separation is useful for testing and demonstrates that the analytics collector can run independently from the websites it tracks.

---

## 5. Data currently collected

The current prototype stores a minimal baseline event model for `page_view` events.

Each event may contain:

- `event_timestamp` — UTC timestamp of the event
- `site_id` — currently derived from the website hostname
- `page_path` — requested page path (e.g. `/`)
- `language` — value of the HTML language attribute
- `device_type` — `desktop`, `mobile`, or `tablet`
- `referrer_type` — `direct`, `internal`, `external_search`, or `external_link`
- `referrer_domain` — source domain if available
- `extra` — JSON field reserved for future extensions

Important: the database stores **raw events**, not aggregated metrics.
One page load = one database row.

This means the analytics/visualization layer can later compute things like:
- page views per site
- page views per day
- device split
- language distribution
- referrer/source distribution
- top pages
- time-based usage patterns

---

## 6. Privacy-first approach

The collector is intentionally designed as a privacy-first prototype.

Current design principles:

- no persistent IP storage
- no user IDs
- no session tracking
- no personal data
- no cookies required for the current prototype
- raw event structure is limited to technical, comparable website usage information

The goal is to support comparable baseline analytics while avoiding person-related tracking.

---

## 7. Why not just use a ready-made analytics platform?

We are aware that tools such as Matomo already provide mature analytics functionality.

However, this prototype was intentionally built as a **minimal and transparent custom collector** because:

- it is easier to understand and explain in a project context
- it collects only a small, controlled set of fields
- it is lightweight
- it is easier to adapt to project-specific requirements
- it supports the idea of standardized cross-site comparison

A future production-oriented solution could still compare this custom approach with tools such as Matomo or combine both approaches.

---

## 8. Technology stack

Current prototype stack:

- **FastAPI** for the analytics backend
- **PostgreSQL** for event storage
- **Docker / Docker Compose** for deployment

This is a pragmatic prototype setup.
For larger future deployments, alternative storage options such as TimescaleDB or ClickHouse could be evaluated.

---

## 9. Project status

Current prototype status:

- analytics backend is running
- PostgreSQL is running
- events are successfully received and stored
- demo website is connected
- the event flow from browser to database works

At this stage, the system already proves:
- technical feasibility
- separation of website and collector backend
- standardized raw event collection
- readiness for downstream analysis by a visualization/dashboard team

---

## 10. Future development steps

The next logical steps are:

### 1. Configurable metric selection
Allow participating websites or organizations to decide which metrics they want to share.

### 2. Extend beyond page views
Add optional standardized event types such as:
- service start
- service completion
- process error
- custom interaction events

### 3. Multi-site pilot setup
Connect multiple demo or pilot websites to demonstrate comparison across participants.

### 4. Improved deployment model
Move toward a Swiss-hosted or production-ready infrastructure model if required by future project constraints.

### 5. Better handover to visualization
Provide a stable data contract and example SQL queries for the dashboard/frontend team.

### 6. Comparison with other analytics tools
Evaluate differences between this lightweight collector and existing tools such as Matomo.

---

## 11. Repository structure

Typical structure of this repository:

    .
    ├── app/
    │   ├── app.py
    │   ├── requirements.txt
    │   └── Dockerfile
    ├── docker-compose.yml
    ├── pgdata/                  # local database volume (not for public repo)
    └── README.md

In a cleaned-up public version, secrets and local runtime data should be excluded from version control.

---

## 12. Running the prototype

A typical local/server-side deployment uses Docker Compose.

Example:

    docker-compose up -d --build

The backend will expose:
- collector endpoint on port `8000`
- PostgreSQL on port `5432`

---

## 13. Example database table

Current main table:

    page_events

Typical columns:

- `id`
- `event_timestamp`
- `site_id`
- `page_path`
- `language`
- `device_type`
- `referrer_type`
- `referrer_domain`
- `extra`

This schema is intentionally simple so that downstream consumers can build their own analytics or visualizations on top of it.

---

## 14. Intended use in the project

This repository is intended to serve as:

- the backend prototype for Group 1 / backend
- the raw event source for Group 2 / visualization
- a technical proof of concept
- a reusable starting point for further experimentation

In other words:
this repository does **not** try to be the full final product.
It demonstrates that a lightweight analytics collector can be built, deployed, connected to a real website, and used as a foundation for later comparison and decision support.

---

## 15. Summary

BFH Analytics Server is a minimal backend for collecting standardized website usage events in a privacy-first way.

It was created to demonstrate that:
- websites can send comparable analytics events to a central server
- those events can be stored in a structured database
- and the resulting data can be used as a basis for further analysis and visualization

This is the backend foundation of our Project 1 prototype.