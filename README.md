# AI-Powered Travel Insurance System

A modern travel insurance platform built with Streamlit and Google's Agent Development Kit (ADK), featuring specialized AI agents for different aspects of the insurance process.

## Features

- User Registration with MAC Address Verification
- Flight Ticket Verification
- Insurance Coverage Calculation
- Claims Processing
- Payment Processing
- Refund Management
- Real-time System Monitoring

## Tech Stack

- Python 3.8+
- Streamlit
- Google ADK
- Google Gemini AI
- Git

## Setup

1. Clone the repository:
```bash
git clone <your-repository-url>
cd travel-insurance
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your Google API key:
   - Create a `.env` file in the root directory
   - Add your Google API key: `GOOGLE_API_KEY=your_api_key_here`

5. Run the application:
```bash
streamlit run streamlit_app.py
```

## Project Structure

```
travel-insurance/
├── streamlit_app.py      # Main Streamlit application
├── main.py              # Core system implementation
├── agents.py            # ADK agent definitions
├── tools.py             # Utility functions
├── auth_agent.py        # Authentication agent
├── payment_agent.py     # Payment processing agent
├── claims_agent.py      # Claims processing agent
├── monitoring_agent.py  # System monitoring agent
├── requirements.txt     # Project dependencies
└── README.md           # Project documentation
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 