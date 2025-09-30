from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import json
import os

# Initialize the FastAPI app
app = FastAPI(
    title="Insurance Sales Agent API",
    description="AI-powered insurance recommendation system for Inya.ai",
    version="1.0.0"
)

# Add CORS middleware to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Data Loading ---
# Load the entire insurance policy knowledge base from the JSON file into memory when the app starts.
policies_data = []

try:
    # Get the directory where this script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    policies_file = os.path.join(current_dir, 'policies.json')
    
    with open(policies_file, 'r') as f:
        policies_data = json.load(f)
    print(f"Successfully loaded {len(policies_data)} policies")
except FileNotFoundError:
    print("ERROR: policies.json not found. Please ensure the file is in the same directory.")
    policies_data = []
except Exception as e:
    print(f"ERROR loading policies: {e}")
    policies_data = []

# --- Pydantic Models ---
# These models define the structure of our API's inputs and outputs.
# FastAPI uses them to validate data automatically.

class UserProfile(BaseModel):
    """Defines the input data structure for the /quote endpoint."""
    age: int = Field(..., description="User's age in years")
    dependents_count: int = Field(..., description="Number of dependents")
    annual_income_band: int = Field(..., description="User's annual income in INR")
    risk_tolerance: str = Field(..., description="Low, Medium, or High risk tolerance")
    preferred_premium_band: int = Field(..., description="User's preferred yearly premium in INR")
    # Adding optional fields that might be useful for filtering specific policy types
    vehicle_type: Optional[str] = Field(None, description="e.g., Car, Bike")
    health_flags: Optional[List[str]] = Field(None, description="e.g., Smoker, Diabetic")

class Policy(BaseModel):
    """Defines the structure of a single policy for the API response."""
    policy_id: str
    name: str
    type: str
    description: str
    sum_insured: list
    premium_yearly: dict
    eligibility: dict
    exclusions: list
    riders: list

# --- API Endpoints ---

@app.get("/")
def read_root():
    """A simple root endpoint to confirm the API is running."""
    return {
        "status": "Insurance Sales Agent API is running.",
        "version": "1.0.0",
        "policies_loaded": len(policies_data),
        "endpoints": {
            "GET /policies": "Get all insurance policies",
            "POST /quote": "Get policy recommendations",
            "POST /handoff": "Schedule human agent callback",
            "GET /health": "Health check endpoint"
        }
    }

@app.get("/health")
def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "policies_count": len(policies_data),
        "timestamp": "2024-09-30"
    }

@app.get("/policies", response_model=List[Policy])
def get_policies():
    """
    Endpoint 1: Returns the entire catalog of insurance policies.
    Fulfills the GET /policies requirement.
    """
    return policies_data

@app.post("/quote")
def get_quote(profile: UserProfile):
    """
    Endpoint 2: The core recommendation engine.
    Accepts a user profile, filters policies, scores them, and returns the top 3.
    Fulfills the POST /quote requirement.
    """
    eligible_policies = []
    
    # 1. Filter policies based on strict eligibility criteria (age)
    for policy in policies_data:
        min_age = policy["eligibility"].get("min_age", 0)
        max_age = policy["eligibility"].get("max_age", 100)
        if min_age <= profile.age <= max_age:
            eligible_policies.append(policy)

    # 2. Score the eligible policies based on the user's preferences
    scored_policies = []
    for policy in eligible_policies:
        score = 0
        # For simplicity, we'll use the premium for the lowest sum_insured as a reference
        try:
            # Skip policies with empty sum_insured list (like motor insurance)
            if not policy["sum_insured"] or policy["sum_insured"] == [0]:
                # For motor insurance or policies without traditional sum insured
                reference_premium = list(policy["premium_yearly"].values())[0]
            else:
                # Find the lowest sum insured and its corresponding premium
                lowest_sum_insured = str(min(policy["sum_insured"]))
                reference_premium = policy["premium_yearly"].get(lowest_sum_insured, float('inf'))

            # Scoring based on premium preference (closer is better)
            premium_diff_percent = abs(reference_premium - profile.preferred_premium_band) / profile.preferred_premium_band
            if premium_diff_percent < 0.2: # Within 20% of preferred premium
                score += 3
            elif premium_diff_percent < 0.5: # Within 50%
                score += 1
            
            # Scoring based on risk tolerance
            if profile.risk_tolerance == "Low" and policy["type"] in ["life", "health"]:
                score += 2
            if profile.risk_tolerance == "High" and "ULIP" in policy["name"]:
                score += 3 # ULIPs are market-linked and higher risk
            
            scored_policies.append({"policy": policy, "score": score})

        except (ValueError, TypeError):
            # Skip policies with invalid or missing premium data
            continue

    # 3. Sort policies by score in descending order
    sorted_policies = sorted(scored_policies, key=lambda x: x["score"], reverse=True)
    
    # 4. Return the top 3 policies
    top_3_policies = [p["policy"] for p in sorted_policies[:3]]
    
    return {"recommendations": top_3_policies}


@app.post("/handoff")
def create_handoff():
    """
    Endpoint 3: Simulates creating a ticket for a human agent.
    Fulfills the POST /handoff requirement.
    """
    # In a real app, this would trigger a webhook or create a ticket in a CRM.
    # For the hackathon, a simple success message is sufficient.
    return {"status": "success", "message": "A callback has been scheduled with a human agent."}