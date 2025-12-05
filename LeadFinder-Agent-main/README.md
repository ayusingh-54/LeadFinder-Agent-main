# LeadFinder Agent

## Overview

LeadFinder is an AI-powered lead generation tool that helps businesses find potential leads on Quora by transforming user queries into targeted searches. Now powered by **OpenAI GPT-4** for superior query transformation and analysis.

![LeadFinder Dashboard](gifs/leadfinder.gif)

## Features

- 🤖 Query transformation using OpenAI GPT-4
- 🎯 Targeted Quora URL search
- 📊 User interaction extraction
- 💼 Comprehensive lead data formatting
- 🎨 Modern dark-themed dashboard UI
- 📥 CSV export functionality

## Prerequisites

- Python 3.9+
- Node.js 18+
- API Keys:
  - OpenAI API Key
  - Firecrawl API Key

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/charans2702/LeadFinder-Agent.git
cd LeadFinder-Agent
```

### 2. Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_openai_api_key
FIRECRAWL_API_KEY=your_firecrawl_api_key
```

## Running the Application

### Start the API Server

```bash
python main.py
```

### API Endpoint

- **POST** `/generate-leads`
- Request Body:
  ```json
  {
    "query": "Find leads for AI customer support",
    "num_links": 3
  }
  ```

## React Dashboard

### Setup

```bash
cd lead-generation-dashboard
npm install
npm run dev
```

The dashboard will be available at `http://localhost:5173`

## Configuration

Modify `config/settings.py` to adjust:

- API Host/Port
- Default Search Settings
- Debug Mode

## Technologies

- FastAPI
- OpenAI GPT-4
- Firecrawl
- Pydantic
- React + Vite
- Tailwind CSS
