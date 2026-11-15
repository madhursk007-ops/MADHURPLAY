# MADHURPLAY — Movie Discovery Platform

**Live application:** https://madhurplay-live.onrender.com  
**Backend API:** https://madhurplay-api-live.onrender.com  
**API health:** https://madhurplay-api-live.onrender.com/api/health

MADHURPLAY is a full-stack movie discovery application with a React/Vite frontend and Python/FastAPI backend. Movie metadata is provided by TMDB.

## Features
- Trending movie discovery
- Movie search and genre browsing
- Movie details, credits and YouTube trailer links
- User registration and login
- Personal watchlists

## Technology
- Frontend: React, Vite, JavaScript
- Backend: Python, FastAPI, SQLAlchemy
- Movie data: TMDB API
- Deployment: Render

## Deployment configuration
The frontend is deployed as a Render static site. The backend is deployed as a separate Render web service. Configure the backend environment variables in Render; do not commit secrets:
- `TMDB_API_READ_ACCESS_TOKEN`
- `JWT_SECRET`
- `FRONTEND_ORIGIN`

## Recovery note
The application source was reconstructed from the documented project specification because the original source archive was unavailable. This repository now contains the deployed source files; the reconstruction may not reproduce every feature or design from an earlier version.

## Links
- **Portfolio project entry:** https://madhursk007-ops.github.io/madhur-portfolio/
- **Portfolio repository:** https://github.com/madhursk007-ops/madhur-portfolio
- **GitHub profile:** https://github.com/madhursk007-ops
