# Source Generated with Decompyle++
# File: agent_router_semantic.cpython-312.pyc (Python 3.12)

import os
import json
import re
import numpy as np
import faiss
from typing import Optional
AGENT_DESCRIPTIONS = {
    'architecture': 'system design, software architecture, component structure, module organization, technology selection, architectural patterns, system boundaries, service decomposition',
    'backend': 'APIs, REST endpoints, databases, server logic, authentication, authorization, data models, SQL, NoSQL, server-side, business logic, backend services, microservices, middleware',
    'frontend': 'UI, user interface, React, Vue, Angular, components, web pages, CSS, HTML, JavaScript, TypeScript, frontend, responsive design, client-side rendering, SPA',
    'ai_deeplearning': 'machine learning, deep learning, neural networks, training, RAG, retrieval augmented generation, NLP, computer vision, LLM, AI model, embeddings, vector search, data science',
    'devops': 'docker, containerization, CI/CD, deployment, infrastructure, cloud, kubernetes, monitoring, logging, configuration management, automation, pipelines, GitHub Actions',
    'qa': 'testing, validation, quality assurance, unit tests, integration tests, bugs, test coverage, pytest, assertions, debugging, verification, end-to-end testing, reliability' }
# WARNING: Decompyle incomplete
