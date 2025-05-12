# main.py

from gemini.runtime import Runtime
from auth_agent import agent as auth_agent
from payment_agent import agent as payment_agent
from claims_agent import agent as claims_agent
from monitoring_agent import agent as monitoring_agent
from agents import (
    user_vetting_agent,
    flight_verification_agent,
    coverage_agent,
    payment_agent,
    claims_agent
)
from tools import (
    UserVettingTools,
    FlightVerificationTools,
    CoverageTools,
    PaymentTools,
    ClaimsTools
)
from typing import Dict, Any

class TravelInsuranceSystem:
    def __init__(self):
        self.user_data = {}
        self.flight_data = {}
        self.insurance_data = {}
        self.payment_data = {}
        self.claims_data = {}

    def register_user(self, email: str, mac_address: str) -> Dict[str, Any]:
        """Register a new user with MAC address verification and 2FA setup."""
        # Verify MAC address
        if not UserVettingTools.verify_mac_address(mac_address):
            return {"status": "error", "message": "Invalid MAC address"}

        # Register user
        user_info = UserVettingTools.register_user(email, mac_address)
        self.user_data[user_info["user_id"]] = user_info

        # Setup 2FA
        two_fa_info = UserVettingTools.setup_2fa(email)
        self.user_data[user_info["user_id"]]["2fa"] = two_fa_info

        return {
            "status": "success",
            "user_id": user_info["user_id"],
            "2fa_setup": True
        }

    def process_flight_purchase(self, ticket_number: str, user_id: str) -> Dict[str, Any]:
        """Process flight purchase and offer insurance options."""
        # Verify flight purchase
        flight_info = FlightVerificationTools.verify_flight_purchase(ticket_number, user_id)
        self.flight_data[ticket_number] = flight_info

        # Extract ticket details
        ticket_details = FlightVerificationTools.extract_ticket_details(ticket_number)
        self.flight_data[ticket_number]["details"] = ticket_details

        # Calculate coverage options
        coverage_options = CoverageTools.recommend_coverage(ticket_details["price"])

        return {
            "status": "success",
            "ticket_number": ticket_number,
            "coverage_options": coverage_options
        }

    def purchase_insurance(self, user_id: str, ticket_number: str, coverage_level: int, 
                         payment_method: str) -> Dict[str, Any]:
        """Process insurance purchase."""
        # Get ticket details
        ticket_details = self.flight_data[ticket_number]["details"]
        
        # Calculate premium
        coverage_info = CoverageTools.calculate_premium(
            ticket_details["price"], 
            coverage_level
        )

        # Process payment
        payment_info = PaymentTools.process_payment(
            coverage_info["premium_amount"],
            payment_method,
            user_id
        )
        self.payment_data[payment_info["transaction_id"]] = payment_info

        # Store insurance details
        self.insurance_data[ticket_number] = {
            "user_id": user_id,
            "coverage_level": coverage_level,
            "coverage_amount": coverage_info["coverage_amount"],
            "premium_amount": coverage_info["premium_amount"],
            "payment_info": payment_info
        }

        return {
            "status": "success",
            "transaction_id": payment_info["transaction_id"],
            "coverage_details": coverage_info
        }

    def process_claim(self, ticket_number: str, user_id: str) -> Dict[str, Any]:
        """Process insurance claim for flight cancellation."""
        # Verify claim
        claim_id = f"claim_{ticket_number}_{user_id}"
        claim_verification = ClaimsTools.verify_claim(claim_id, user_id)
        
        if claim_verification["verification_status"] != "verified":
            return {"status": "error", "message": "Claim verification failed"}

        # Get insurance details
        insurance_details = self.insurance_data[ticket_number]
        
        # Process payout
        payout_info = ClaimsTools.process_payout(
            claim_id,
            insurance_details["coverage_amount"]
        )
        self.claims_data[claim_id] = payout_info

        # Notify user
        user_email = self.user_data[user_id]["email"]
        notification = ClaimsTools.notify_user(
            user_email,
            f"Your claim has been processed. Payout amount: {insurance_details['coverage_amount']}"
        )

        return {
            "status": "success",
            "claim_id": claim_id,
            "payout_amount": insurance_details["coverage_amount"],
            "notification": notification
        }

    def process_refund(self, transaction_id: str) -> Dict[str, Any]:
        """Process refund for unused insurance plan."""
        payment_info = self.payment_data.get(transaction_id)
        if not payment_info:
            return {"status": "error", "message": "Transaction not found"}

        refund_info = PaymentTools.process_refund(transaction_id)
        return {
            "status": "success",
            "refund_info": refund_info
        }

# Example usage
if __name__ == "__main__":
    system = TravelInsuranceSystem()
    
    # Register user
    user_registration = system.register_user(
        email="user@example.com",
        mac_address="00:1A:2B:3C:4D:5E"
    )
    
    # Process flight purchase
    flight_purchase = system.process_flight_purchase(
        ticket_number="ABC123",
        user_id=user_registration["user_id"]
    )
    
    # Purchase insurance
    insurance_purchase = system.purchase_insurance(
        user_id=user_registration["user_id"],
        ticket_number="ABC123",
        coverage_level=2,
        payment_method="VISA"
    )
    
    # Process claim
    claim = system.process_claim(
        ticket_number="ABC123",
        user_id=user_registration["user_id"]
    )
