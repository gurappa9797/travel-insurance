
"""Demonstration of Travel AI Conceirge using Agent Development Kit"""

from google.adk.agents import Agent
from google.adk.tools import Tool
from typing import List, Dict, Any

from travel_concierge import prompt

from travel_concierge.sub_agents.booking.agent import booking_agent
from travel_concierge.sub_agents.in_trip.agent import in_trip_agent
from travel_concierge.sub_agents.inspiration.agent import inspiration_agent
from travel_concierge.sub_agents.planning.agent import planning_agent
from travel_concierge.sub_agents.post_trip.agent import post_trip_agent
from travel_concierge.sub_agents.pre_trip.agent import pre_trip_agent

from travel_concierge.tools.memory import _load_precreated_itinerary


# === Agent Definition ===


# ===1. User Vetting Agent ===>>>>> (handles user registration and MAC address verification) 

user_vetting_agent = Agent(
    name="UserVettingAgent",
    model="gemini-2.5-pro-exp-03-25",
    description="Handles user registration, authentication, and MAC address verification",
    skills=[
        "verify_mac_address",
        "register_user",
        "setup_2fa",
        "validate_user_credentials",
        "log_user_activity"
    ],
    on_event=["user_registration", "authentication_request"]
)

# === Flight Purchase Verification Agent ===>>>>> (verifies flight purchases)
flight_verification_agent = Agent(
    name="FlightVerificationAgent",
    model="gemini-2.5-pro-exp-03-25",
    description="Verifies flight purchases and matches them with user credentials",
    skills=[
        "verify_flight_purchase",
        "match_purchase_to_user",
        "extract_ticket_details",
        "calculate_insurance_premium"
    ],
    on_event=["flight_purchase_detected", "ticket_verification_request"]
)

# === Insurance Coverage Agent ===>>>>> (manages insurance coverage options and calculations)
coverage_agent = Agent(
    name="CoverageAgent",
    model="gemini-2.5-pro-exp-03-25",
    description="Manages insurance coverage options and calculations",
    skills=[
        "calculate_coverage",
        "recommend_coverage_plan",
        "process_subscription",
        "handle_plan_updates"
    ],
    on_event=["coverage_calculation_request", "plan_subscription_request"]
)

# === Payment Processing Agent ===>>>>> (handles payment processing for insurance plans)
payment_agent = Agent(
    name="PaymentAgent",
    model="gemini-2.5-pro-exp-03-25",
    description="Handles payment processing for insurance plans",
    skills=[
        "process_payment",
        "handle_subscription",
        "manage_payment_methods",
        "process_refunds"
    ],
    on_event=["payment_request", "refund_request"]
)

# === Claims Processing Agent ===>>>>> (manages insurance claims and payouts)
claims_agent = Agent(
    name="ClaimsAgent",
    model="gemini-2.5-pro-exp-03-25",
    description="Manages insurance claims and payouts",
    skills=[
        "verify_claim",
        "process_claim",
        "handle_payout",
        "notify_user"
    ],
    on_event=["claim_submission", "claim_verification_request"]
)

# === Coverage Calculation Formula ===>>>>> (calculates insurance coverage based on ticket price and coverage level)
def calculate_coverage(ticket_price: float, coverage_level: int) -> Dict[str, float]:
    """
    Calculate insurance coverage based on ticket price and coverage level.
    
    Coverage levels:
    1: 50% coverage (1% of ticket price)
    2: 75% coverage (2% of ticket price)
    3: 100% coverage (3% of ticket price)
    """
    coverage_percentages = {
        1: 0.50,
        2: 0.75,
        3: 1.00
    }
    
    premium_percentages = {
        1: 0.01,
        2: 0.02,
        3: 0.03
    }
    
    coverage_amount = ticket_price * coverage_percentages[coverage_level]
    premium_amount = ticket_price * premium_percentages[coverage_level]
    
    return {
        "coverage_amount": coverage_amount,
        "premium_amount": premium_amount,
        "coverage_percentage": coverage_percentages[coverage_level] * 100
    }

# === Plan Types ===>>>>> (defines different types of insurance plans)
PLAN_TYPES = {
    "SINGLE": "Single purchase plan",
    "MONTHLY": "Yearly Plan (1 per month)",
    "FAMILY_TRIP": "One time family trip for 4",
    "ANNUAL_FAMILY": "Annual Trip Protection for 4 (1 per month)"
}

# === Payment Methods ===>>>>> (defines different payment methods)
PAYMENT_METHODS = [
    "VISA",
    "MASTERCARD",
    "AMEX",
    "PAYPAL"
]

# === Register User ===>>>>> (registers a new user)

system = TravelInsuranceSystem()
user_registration = system.register_user(
    email="user@example.com",
    mac_address="00:1A:2B:3C:4D:5E"
)

# === Process a flight purchase ===>>>>> (processes a flight purchase)

flight_purchase = system.process_flight_purchase(
    ticket_number="ABC123",
    user_id=user_registration["user_id"]
)

# === Purchase insurance ===>>>>> (purchases insurance for a flight)

insurance_purchase = system.purchase_insurance(
    user_id=user_registration["user_id"],
    ticket_number="ABC123",
    coverage_level=2,  # 75% coverage
    payment_method="VISA"
)

# === Process a claim ===>>>>> (processes a claim)

claim = system.process_claim(
    ticket_number="ABC123",
    user_id=user_registration["user_id"]
)