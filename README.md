# Inya Insurance Sales Agent API

## Overview
This is a FastAPI-based backend service that provides insurance policy recommendations for the Inya.ai conversational agent. The API serves as the knowledge base and recommendation engine for the "Aura" insurance advisor bot.

## Features
- **50 realistic insurance policies** covering Health, Life, Term, and Motor insurance
- **Intelligent recommendation engine** that filters and scores policies based on user profiles
- **RESTful API endpoints** designed for easy integration with Inya.ai platform
- **CORS enabled** for web-based integrations
- **Production-ready** with proper error handling and logging

## API Endpoints

### GET /
Root endpoint that returns API status and available endpoints.

### GET /health
Health check endpoint for monitoring and load balancers.

### GET /policies
Returns the complete catalog of all 50 insurance policies with detailed information including:
- Policy details (name, type, description)
- Sum insured options
- Premium structures
- Eligibility criteria
- Exclusions and riders

### POST /quote
The core recommendation engine. Accepts a user profile and returns the top 3 most suitable policies.

**Request Body:**
```json
{
  "age": 30,
  "dependents_count": 2,
  "annual_income_band": 800000,
  "risk_tolerance": "Medium",
  "preferred_premium_band": 15000,
  "vehicle_type": "Car",
  "health_flags": ["Smoker"]
}
```

**Response:**
```json
{
  "recommendations": [
    {
      "policy_id": "HLT_IND_002",
      "name": "Arogya Shield - Gold",
      "type": "health",
      "description": "A comprehensive health plan...",
      "sum_insured": [500000, 1000000, 1500000],
      "premium_yearly": {"500000": 12500, "1000000": 18000},
      "eligibility": {"min_age": 21, "max_age": 50},
      "exclusions": ["Cosmetic surgery"],
      "riders": [...]
    }
  ]
}
```

### POST /handoff
Simulates creating a ticket for human agent callback. Returns success confirmation.

## Deployment on Vercel

### Prerequisites
1. GitHub account
2. Vercel account (free tier available)
3. Git installed locally

### Step-by-step Deployment

1. **Create a GitHub Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Insurance Sales Agent API"
   git branch -M main
   git remote add origin https://github.com/your-username/inya-insurance-api.git
   git push -u origin main
   ```

2. **Deploy to Vercel**
   - Go to [vercel.com](https://vercel.com) and sign in
   - Click "New Project"
   - Import your GitHub repository
   - Vercel will automatically detect the Python project
   - Click "Deploy"

3. **Configuration**
   - Vercel will use the `vercel.json` configuration file
   - The `main.py` file contains the FastAPI application
   - Dependencies are specified in `requirements.txt`

4. **Testing Deployment**
   - Once deployed, Vercel will provide a URL (e.g., `https://your-project.vercel.app`)
   - Test the API using the provided test script:
   ```bash
   python test_api.py https://your-project.vercel.app
   ```

## Integration with Inya.ai

### Action Configuration
Create a new Action in Inya.ai with these settings:

- **Action Name:** Get Insurance Recommendations
- **HTTP Method:** POST
- **Endpoint URL:** `https://your-vercel-url.vercel.app/quote`
- **Content Type:** application/json
- **Request Body:** Map user profile data to the required JSON structure

### Sample Integration Flow
1. Aura collects user information (age, income, risk tolerance, etc.)
2. Aura triggers the "Get Insurance Recommendations" action
3. API returns top 3 policy recommendations
4. Aura presents recommendations in conversational format
5. If needed, Aura can trigger handoff to human agent

## Architecture

```
User → Inya.ai Platform (Aura Bot) → FastAPI on Vercel → Policy Database (JSON) → Response → User
```

## Project Structure
```
├── main.py              # FastAPI application
├── policies.json        # 50 insurance policies database
├── requirements.txt     # Python dependencies
├── vercel.json         # Vercel deployment configuration
├── test_api.py         # API testing script
├── vercel_app.py       # Vercel entry point
└── README.md           # This file
```

## Policy Database
The `policies.json` file contains 50 carefully crafted insurance policies:
- **15 Health Insurance policies** (individual, family, senior citizen, critical illness)
- **10 Term Insurance policies** (basic, with ROP, whole life, increasing cover)
- **15 Life Insurance policies** (endowment, ULIP, child plans, pension)
- **10 Motor Insurance policies** (car, bike, commercial, EV)

Each policy includes realistic Indian market data with proper premium structures, eligibility criteria, and policy features.

## Technical Stack
- **FastAPI** - Modern, fast web framework for building APIs
- **Pydantic** - Data validation using Python type annotations
- **Uvicorn** - ASGI server for production deployment
- **Vercel** - Serverless deployment platform

## Live API URL
Once deployed, your API will be available at: `https://your-project-name.vercel.app`

Replace `your-project-name` with your actual Vercel project name.

## Support
For technical issues or questions, please refer to the FastAPI documentation or create an issue in the project repository.