# Medical Wellness Assistant

A beautiful medical assistant chatbot with a warm pink/peach theme and rose-gold dark mode.

## Overview

This application provides a professional healthcare-themed chat interface that connects to an external Flask/FastAPI backend for AI-powered medical assistance.

## Architecture

### Frontend (React + Vite)
- **Framework**: React with TypeScript
- **Styling**: Tailwind CSS with Shadcn UI components
- **State Management**: React hooks (useState, useEffect)
- **Routing**: Wouter

### Backend (Express)
- **API Proxy**: Express server that forwards requests to Flask/FastAPI backend
- **Endpoints**:
  - `POST /api/chat` - Proxies chat messages to Flask backend
  - `POST /api/clear_memory` - Proxies clear session requests

### External Integration
- Connects to Flask/FastAPI backend at `http://127.0.0.1:8000` (configurable via `FLASK_API_URL` env var)
- Expected Flask endpoints:
  - `POST /chat` - Accepts `session_id`, `message`, `developer_mode`, `stream`
  - `POST /clear_memory` - Accepts `session_id`

## Key Components

- `ThemeProvider` - Dark/light mode context with localStorage persistence
- `ChatHeader` - Medical-themed header with heartbeat animation
- `ChatSidebar` - Session info, developer mode toggle, clear chat
- `ChatMessage` - User/AI message bubbles with metadata expansion
- `ChatInput` - Message input with send button
- `ThinkingIndicator` - Animated AI thinking state

## Design Theme

### Light Mode
- Background: Warm off-white (#FFF7F5)
- Primary: Rose/Coral (#FB7185)
- Cards: Soft pink with rose borders

### Dark Mode (Rose-Gold Night)
- Background: Deep burgundy (#1C0A12)
- Primary: Rose (#FB7185)
- Accents: Gold highlights (#D4AF37)

## Running the Application

1. Start this Replit application (runs on port 5000)
2. Start your Flask/FastAPI backend on port 8000 (or set `FLASK_API_URL` environment variable)
3. The chat interface will proxy all requests through Express to your Flask API

## Environment Variables

- `FLASK_API_URL` - URL of the Flask/FastAPI backend (default: `http://127.0.0.1:8000`)
