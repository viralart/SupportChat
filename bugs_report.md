# Potential Bugs Found

1. **Logout Functionality Broken**
   - **Description**: Clicking the "Logout" button on the agent dashboard or profile page fails to terminate the user session. The user is not redirected to the login page, and the URL remains at `.../agent/dashboard` (or the last visited agent path), allowing the user to continue interacting with the platform unabated.
   - **Steps to Reproduce**: Log into the application -> Navigate to the dashboard -> Click "Logout".
   - **Expected Behavior**: The session should be securely terminated and the user routed back to the authentication screen.

2. **Absence of Clear Authentication Error Messages**
   - **Description**: When entering invalid credentials (such as an incorrect password), the application does not reliably provide a clear error message or toast notification indicating authentication failure. The user is instead silently kept on the login page without descriptive feedback.
