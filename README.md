# Support Chat Automation Framework

**The repo is 100% vibe coded and has 0% human interaction**

An end-to-end regression testing suite for the Support Chat platform, built using **Python** and **Playwright**.

## Features

- **Automated Login**: Secure authentication flow for Support Agents.
* **E2E Live Chat Interaction**: Simulates a complete customer journey, including:
  - Bypassing the AI Chatbot firewall.
  - Escalating to a real Support Agent.
  - Bidirectional, real-time message verification between two isolated browser contexts.
  - **Agent Ticket Creation**: Automated escalation from chat to official support ticket.
* **POM Architecture**: Organized using the Page Object Model for scalability.
* **Bug Documentation**: Integrated findings report (`bugs_report.md`).

## Prerequisites

- Python 3.8+
- [Playwright](https://playwright.dev/python/docs/intro)

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/viralart/SupportChat.git
   cd SupportChat
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

## Running Tests

To run the full regression suite:
```bash
pytest tests/ -v
```

To run the **Live Chat** bi-directional test specifically (Headed mode):
```bash
pytest tests/test_live_chat.py -vs
```

## Bug Findings
Detailed descriptions of functional issues identified during development can be found in [bugs_report.md](./bugs_report.md).
