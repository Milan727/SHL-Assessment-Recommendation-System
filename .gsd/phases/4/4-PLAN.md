---
phase: 4
plan: 1
wave: 1
---

# Plan 4.1: FastAPI Development

## Objective
Wrap the recommendation engine in a FastAPI application that implements the `/health` and `/recommend` endpoints according to the strict JSON schema.

## Context
- `.gsd/SPEC.md`
- `src/balancer.py`

## Tasks

<task type="auto">
  <name>Initialize FastAPI and Health Endpoint</name>
  <files>src/app.py</files>
  <action>
    - Create a new file `src/app.py`.
    - Initialize a FastAPI application.
    - Create a `GET /health` endpoint that returns `{"status": "ok"}` to verify the server is running.
  </action>
  <verify>Running uvicorn locally and hitting curl http://localhost:8000/health returns status ok.</verify>
  <done>Server starts without errors and `/health` responds correctly.</done>
</task>

<task type="auto">
  <name>Implement Recommend Endpoint</name>
  <files>src/app.py</files>
  <action>
    - Define a Pydantic `QueryRequest` model containing a `query` string.
    - Create a `POST /recommend` endpoint.
    - Import `get_balanced_recommendations` from `src.balancer`.
    - Execute the balancer against the incoming query and wrap the results in a precise JSON schema containing `query` and `recommendations` array.
  </action>
  <verify>Sending a POST request to `/recommend` with a JSON payload returns the exact array structure containing `Assessment_url` keys.</verify>
  <done>The `/recommend` endpoint successfully acts as an API gateway for the RAG engine.</done>
</task>

## Success Criteria
- [ ] `FastAPI` application starts successfully.
- [ ] `/health` returns `{ "status": "ok" }`.
- [ ] `/recommend` reliably ingests HTTP POST queries, passes them to the Chroma balancer, and emits valid response JSONs.
