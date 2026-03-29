# AI Support Portal
A full-stack Python application that uses AI to categorize support tickets.
### Key Features:
**AI Analysis**: Automatically detects if a ticket is Hardware or Software.
**Sentiment Detection**: Flags frustrated customers with a "Red" Urgent tag.
**Database**: Saves all tickets permanently using SQLAlchemy and SQLite.
 **Modern UI**: Clean dashboard built with Tailwind CSS.

### How to Run:
1. Install requirements: `pip install -r requirements.txt`
2. Start the server: `uvicorn main:app --reload`
3. Open: http://127.0.0.1:8080/
