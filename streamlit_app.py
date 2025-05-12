# streamlit_app.py

import streamlit as st
from main import TravelInsuranceSystem
from agents import (
    user_vetting_agent,
    flight_verification_agent,
    coverage_agent,
    payment_agent,
    claims_agent,
    calculate_coverage,
    PLAN_TYPES,
    PAYMENT_METHODS
)

# Initialize system and session
if "insurance_system" not in st.session_state:
    st.session_state.insurance_system = TravelInsuranceSystem()

system = st.session_state.insurance_system

# Page configuration
st.set_page_config(
    page_title="AI Travel Insurance Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .agent-status {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("🤖 Agent Status")
    st.markdown("---")
    
    # Display agent statuses
    agents = {
        "User Vetting": user_vetting_agent,
        "Flight Verification": flight_verification_agent,
        "Coverage": coverage_agent,
        "Payment": payment_agent,
        "Claims": claims_agent
    }
    
    for name, agent in agents.items():
        st.markdown(f"""
            <div class="agent-status" style="background-color: #f0f2f6;">
                <h4>{name} Agent</h4>
                <p>Status: Active</p>
                <p>Model: {agent.model}</p>
            </div>
        """, unsafe_allow_html=True)

# Main content
st.title("✈️ AI-Powered Travel Insurance System")

# User Registration Section
st.header("1. User Registration")
col1, col2 = st.columns(2)

with col1:
    email = st.text_input("Email Address")
    mac_address = st.text_input("MAC Address")
    if st.button("Register User"):
        if email and mac_address:
            with st.spinner("Verifying user..."):
                result = system.register_user(email, mac_address)
                st.session_state.user_id = result.get("user_id", None)
                st.success(f"Registration successful! User ID: {st.session_state.user_id}")
        else:
            st.error("Please fill in all fields")

# Flight Ticket Section
st.header("2. Flight Ticket Verification")
col3, col4 = st.columns(2)

with col3:
    ticket_number = st.text_input("Ticket Number")
    if st.button("Verify Ticket"):
        if "user_id" not in st.session_state:
            st.error("Please register first")
        else:
            with st.spinner("Verifying ticket..."):
                result = system.process_flight_purchase(ticket_number, st.session_state.user_id)
                st.session_state.ticket_number = ticket_number
                st.json(result)

# Insurance Purchase Section
st.header("3. Insurance Coverage")
col5, col6 = st.columns(2)

with col5:
    coverage_level = st.selectbox(
        "Coverage Level",
        options=[1, 2, 3],
        format_func=lambda x: f"Level {x} ({'50%' if x==1 else '75%' if x==2 else '100%'} coverage)"
    )
    
    plan_type = st.selectbox("Plan Type", options=list(PLAN_TYPES.keys()))
    payment_method = st.selectbox("Payment Method", options=PAYMENT_METHODS)
    
    if st.button("Calculate Premium"):
        if "ticket_number" in st.session_state:
            with st.spinner("Calculating premium..."):
                # Get ticket price from the system
                ticket_info = system.get_ticket_info(st.session_state.ticket_number)
                if ticket_info:
                    coverage_details = calculate_coverage(ticket_info["price"], coverage_level)
                    st.session_state.coverage_details = coverage_details
                    st.success(f"""
                        Premium Amount: ${coverage_details['premium_amount']:.2f}
                        Coverage Amount: ${coverage_details['coverage_amount']:.2f}
                        Coverage Percentage: {coverage_details['coverage_percentage']}%
                    """)
        else:
            st.error("Please verify your ticket first")

# Claims Section
st.header("4. File a Claim")
col7, col8 = st.columns(2)

with col7:
    claim_type = st.selectbox(
        "Claim Type",
        options=["Flight Cancellation", "Medical Emergency", "Baggage Loss", "Trip Delay"]
    )
    claim_description = st.text_area("Claim Description")
    
    if st.button("Submit Claim"):
        if "user_id" in st.session_state and "ticket_number" in st.session_state:
            with st.spinner("Processing claim..."):
                result = system.process_claim(
                    st.session_state.ticket_number,
                    st.session_state.user_id,
                    claim_type=claim_type,
                    description=claim_description
                )
                st.json(result)
        else:
            st.error("Please complete registration and ticket verification first")

# Refund Section
st.header("5. Request Refund")
col9, col10 = st.columns(2)

with col9:
    transaction_id = st.text_input("Transaction ID")
    refund_reason = st.text_area("Refund Reason")
    
    if st.button("Request Refund"):
        if transaction_id:
            with st.spinner("Processing refund..."):
                result = system.process_refund(transaction_id, reason=refund_reason)
                st.json(result)
        else:
            st.error("Please provide a transaction ID")
