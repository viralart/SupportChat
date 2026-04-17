import pytest
from playwright.sync_api import sync_playwright, expect
import time
import random

CUSTOMER_URL = "https://superwork-chat-support.artoon.in/support?at=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY5ZDBiODMxZjU3YWEyYTZkZThlNDRhZiIsImNsaWVudFByb2ZpbGVJZCI6IjY5ZDBiODMxZjU3YWEyYTZkZThlNDRhZiIsInByb2R1Y3RJZCI6IjY5YzEyZTgwNGFlMDU3ZTY4ODdmZGI2MSIsImNvbXBhbnlJZCI6IjY4Mzk4ODMxM2FhZjhhMDU1OTBkY2RlOCIsInVzZXJOYW1lIjoiU3VwZXJXIiwiY29tcGFueU5hbWUiOiJTdXBlcndvcmtzIiwiZW1haWwiOiJzdXBlcndvcmtzQHlvcG1haWwuY29tIiwiY2F0ZWdvcnkiOiJBIiwic291cmNlIjoiY3VzdG9tZXIiLCJhY2Nlc3NUeXBlIjoiY2xpZW50X2FjY2VzcyIsImlhdCI6MTc3NjQxOTMzMywiZXhwIjoxNzc2ODUxMzMzLCJhdWQiOiJyb290IiwiaXNzIjoic3VwZXJ3b3Jrc0B5b3BtYWlsLmNvbSIsInN1YiI6InN1cGVyd29ya3NAeW9wbWFpbC5jb20ifQ.zDdGKeSoZCMV7DW6SkcBaPe6nrmb_bdFPZ3dt78LqsA&rt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY5ZDBiODMxZjU3YWEyYTZkZThlNDRhZiIsImNsaWVudFByb2ZpbGVJZCI6IjY5ZDBiODMxZjU3YWEyYTZkZThlNDRhZiIsInByb2R1Y3RJZCI6IjY5YzEyZTgwNGFlMDU3ZTY4ODdmZGI2MSIsImNvbXBhbnlJZCI6IjY4Mzk4ODMxM2FhZjhhMDU1OTBkY2RlOCIsInVzZXJOYW1lIjoiU3VwZXJXIiwiY29tcGFueU5hbWUiOiJTdXBlcndvcmtzIiwiZW1haWwiOiJzdXBlcndvcmtzQHlvcG1haWwuY29tIiwiY2F0ZWdvcnkiOiJBIiwic291cmNlIjoiY3VzdG9tZXIiLCJhY2Nlc3NUeXBlIjoiY2xpZW50X3JlZnJlc2giLCJpYXQiOjE3NzY0MTkzMzMsImV4cCI6MTc3NzcxNTMzMywiYXVkIjoicm9vdCIsImlzcyI6InN1cGVyd29ya3NAeW9wbWFpbC5jb20iLCJzdWIiOiJzdXBlcndvcmtzQHlvcG1haWwuY29tIn0.jSAGLi3-gVayV07NAE9MxqxEuY0Byphqm3yPALvgnU4"

def test_cross_browser_chat(playwright, base_url):
    """E2E Test simulating customer and agent interacting in two distinct browser instances."""
    
    unique_message_id = f"TestMessage-{random.randint(1000, 9999)}"
    customer_msg = f"Hello! Need help {unique_message_id}"
    agent_msg = f"I am reviewing your request {unique_message_id}"
    
    # We are running this HEADED with a slow_mo so the user can see it! 
    browser = playwright.chromium.launch(headless=False, slow_mo=1000)
    
    # Context 1: Customer (Smaller viewport on the left)
    customer_ctx = browser.new_context(viewport={"width": 640, "height": 1080})
    customer_page = customer_ctx.new_page()
    
    # Context 2: Agent (Larger viewport on the right)
    agent_ctx = browser.new_context(viewport={"width": 1280, "height": 1080})
    agent_page = agent_ctx.new_page()
    
    try:
        # --- AGENT LOGIN ---
        print("[Agent] Logging into backoffice...")
        agent_page.goto(base_url)
        agent_page.fill("#email", "viral.maurya@yopmail.com")
        agent_page.fill("#password", "Artoon1#")
        agent_page.click("button[type='submit']")
        agent_page.wait_for_url("**/agent/**", timeout=10000)
        
        # Go to Dashboard so agent can receive global alert
        agent_page.goto(f"{base_url}/agent/dashboard")
        agent_page.wait_for_load_state("networkidle")
        
        # --- CUSTOMER INITIALIZE CHAT ---
        print("[Customer] Loading Widget...")
        customer_page.goto(CUSTOMER_URL)
        customer_page.wait_for_load_state("networkidle")
        
        start_btn = customer_page.locator("button:has-text('Start Support Chat')")
        if start_btn.count() > 0:
            print("[Customer] Found 'Start Support Chat' button. Clicking...")
            start_btn.click()
            
        customer_page.wait_for_timeout(3000)
        
        # Check standard locators
        print("[Customer] Typing initial message to AI...")
        customer_input = customer_page.locator("textarea").first
        if customer_input.count() == 0:
             customer_input = customer_page.locator("input[type='text']").first
        
        if customer_input.count() > 0:
            customer_input.fill(customer_msg)
            # Find closest button
            customer_submit = customer_page.locator("button:has(svg), button[type='submit']")
            if customer_submit.count() > 0:
                customer_submit.last.click()
            else:
                customer_page.keyboard.press("Enter")
                
        print("[Customer] Sent message:", customer_msg)
        customer_page.wait_for_timeout(4000) # Wait for AI reply
        
        # --- CUSTOMER BYPASSES AI BOT ---
        print("[Customer] Indicating dissatisfaction with AI...")
        
        # 1. Click 'No'
        no_btn = customer_page.locator("button:has-text('No X'), button:has-text('No')").first
        print("[Customer] Waiting for 'No' button and clicking...")
        no_btn.click()
        customer_page.wait_for_timeout(2000)

        # 2. Click 'Or connect me to a support agent'
        print("[Customer] Clicking 'Or connect me to a support agent'...")
        connect_link = customer_page.locator("text='Or connect me to a support agent'").first
        connect_link.click()
        customer_page.wait_for_timeout(2000)

        # 3. Click 'Yes, connect me'
        print("[Customer] Clicking 'Yes, connect me'...")
        connect_btn = customer_page.locator("text='Yes, connect me'").first
        connect_btn.click()
             
        customer_page.wait_for_timeout(3000) # Give WS time to route to Agent's queue
             
        customer_page.wait_for_timeout(3000) # Give WS time to route to Agent's queue
        
        # --- AGENT RECEIVES ALERT & ACCEPTS ---
        print("[Agent] Waiting for Incoming Chat Alert...")
        
        # The gigantic popup "Incoming Support Request" with an "Accept" button
        accept_btn = agent_page.locator("button:has-text('Accept')").first
        try:
             # Wait for the accept button to appear natively
             accept_btn.wait_for(state="visible", timeout=15000)
             print("[Agent] Alert Received! Accepting chat...")
             accept_btn.click()
        except:
             print("[Agent Error] Auto-alert did not appear. Searching the global Queue natively...")
             agent_page.goto(f"{base_url}/agent/queue")
             agent_page.wait_for_load_state("networkidle")
             agent_page.wait_for_timeout(2000)
             fallback_accept = agent_page.locator("text='Accept'").first
             if fallback_accept.count() > 0:
                 fallback_accept.click()
                 print("[Agent] Accepted via generic queue table.")
                 
        agent_page.wait_for_timeout(4000) # Let workspace route to the assigned chat
        
        print("[Agent] Inspecting historical chat text sent to AI...")
        expect(agent_page.locator("body")).to_contain_text(unique_message_id, timeout=8000)
        
        print("[Agent] Sending manual reply to customer...")
        agent_input = agent_page.locator("textarea").first
        if agent_input.count() == 0:
             agent_input = agent_page.locator("input[type='text']").first
        agent_input.fill(agent_msg)
        agent_page.keyboard.press("Enter")
        
        # --- EXTENDED CHAT CONVERSATION (Talking with Human Agent) ---
        print("\n--- Starting Extended Conversation (Talking with Agent) ---")
        
        customer_phrases = [
            "I'm having trouble with the dashboard.",
            "Where can I find my previous tickets?",
            "Is there a way to export the chat log?",
            "How long is the typical wait time?",
            "Can I add another user to this account?",
        ]
        
        agent_phrases = [
            "I can certainly help you with the dashboard issues.",
            "You can find previous tickets in the 'Tickets' section on the sidebar.",
            "Yes, you can export the logs from the settings menu.",
            "Typical wait times are usually under 5 minutes.",
            "Yes, users can be added via the Superadmin panel.",
        ]
        
        for i in range(len(customer_phrases)):
            # CUSTOMER TURN
            c_msg = customer_phrases[i]
            print(f"[Customer] Sending: {c_msg}")
            c_input = customer_page.locator("textarea, [contenteditable='true']").first
            c_input.click()
            c_input.fill(c_msg)
            customer_page.keyboard.press("Enter")
            expect(agent_page.locator("body")).to_contain_text(c_msg, timeout=10000)
            
            # AGENT TURN
            a_msg = agent_phrases[i]
            print(f"[Agent] Sending: {a_msg}")
            a_input = agent_page.locator("textarea, [contenteditable='true']").last
            a_input.click()
            a_input.fill(a_msg)
            agent_page.keyboard.press("Enter")
            expect(customer_page.locator("body")).to_contain_text(a_msg, timeout=10000)

        # --- AGENT CREATES TICKET (Issue Not Resolved) ---
        print("\n--- Agent: Creating Ticket (Issue Not Resolved) ---")
        
        # Look for the "Create ticket" button in the right sidebar
        ticket_btn = agent_page.locator("button:has-text('Create ticket')").first
        print("[Agent] Waiting for 'Create ticket' button...")
        ticket_btn.wait_for(state="visible", timeout=10000)
        ticket_btn.click()
        
        # Fill the ticket form
        print("[Agent] Filling Ticket Form...")
        subject_input = agent_page.locator("input[name*='title'], input[placeholder*='Title'], input[type='text']:not([placeholder*='Search'])").first
        subject_input.fill(f"Support Request: {unique_message_id}")
        priority_select = agent_page.locator("select").first
        if priority_select.count() > 0:
            priority_select.select_option(label="High")
        desc_input = agent_page.locator("textarea[name*='description'], textarea[placeholder*='Description'], textarea").first
        desc_input.fill(f"This is an automated ticket for {unique_message_id}. Issue remains unresolved after chat.")
        
        # Click Create/Submit
        create_submit = agent_page.locator("button[type='submit'], button:has-text('Create')").last
        create_submit.click()
        print("[Agent] Ticket Submit clicked.")
        
        # Verify the chat is now disabled for the customer
        print("[Verification] Checking for 'Awaiting resolution' status...")
        agent_page.wait_for_timeout(3000)
        expect(customer_page.locator("textarea")).to_be_disabled()
        
        # Use regex to avoid brittle character/whitespace issues with the special dash and ellipsis
        import re
        expect(customer_page.locator("textarea")).to_have_attribute("placeholder", re.compile(r"A ticket has been raised"))
        
        print("\n[SUCCESS] Ticket created and chat correctly enters 'Awaiting Resolution' state!")
        time.sleep(10) # Pause so you can see the final state before closure!
        
    finally:
        browser.close()
