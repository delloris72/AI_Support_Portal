# Project Title: AI-Augmented Support Portal: A Beginner’s Full-Stack Toolkit for FastAPI & Sentiment Analysis

## Project Objective
The goal of this toolkit is to provide a beginner-friendly roadmap for building an AI-powered web application using Python and FastAPI.
By using generative AI as a collaborative tutor, this project demonstrates how a novice can:
Build a Full-Stack Site: Connect a Python "brain" to a permanent database and a visual dashboard.
Integrate AI: Use natural language processing to automatically categorize support tickets and detect customer mood.
Bridge the Learning Gap: Show how to use AI prompts to solve real-world coding "bugs" and setup hurdles in real-time.
  
  ## Overview of Technology
This project uses FastAPI, a modern, high-performance web framework for building APIs with Python. It is designed to be easy to learn and fast to code. 
FastAPI
FastAPI
 +1
Database: SQLAlchemy handles data persistence using SQLite.
UI: Jinja2 is used for HTML templating.
AI: TextBlob provides simple natural language processing for sentiment analysis. 
TextBlob: Simplified Text Processing
TextBlob: Simplified Text Processing

## System requirements
Operating System: Windows 10/11, macOS, or Linux.
Python Runtime: Version 3.10 or higher (Required for the latest FastAPI features).
Hardware Essentials:
Memory: Minimum 4GB RAM (8GB recommended for multitasking).
Storage: ~500MB free space for Python and project libraries.
Software Tools:
Editor: Visual Studio Code (Recommended).
Browser: Any modern browser (Chrome, Edge, Firefox).
Key Dependencies (Installed via pip):
fastapi[standard]: The core web framework.
sqlalchemy: The database manager.
textblob: The AI analysis engine.
jinja2: The HTML dashboard renderer.
python-multipart: For handling the dashboard's "Submit" form. 

 ## Setup Instructions
Clone/Download the project folder.
Create a Virtual Environment:
python -m venv venv
Activate it:
Windows: .\venv\Scripts\activate
Mac/Linux: source venv/bin/activate
Install Requirements:
pip install fastapi[all] sqlalchemy textblob jinja2 python-multipart
Download AI Data:
python -m textblob.download_corpora 
 
 ## Minimal Working Example (Hello World)
python
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello World"}
Use code with caution.

   
## AI Prompts & Learning Reflections
Key Prompts Used:
"I have an Internal Server Error, how do I find the hidden message in the terminal?"
"How do I change the URL in the browser to see the /docs page?"
Reflection:
Using AI as a tutor allowed for immediate feedback on "invisible" errors (like folder hierarchy or port conflicts) that static tutorials often miss. It helped bridge the gap between "writing code" and "running a live server."


## Common Errors & Resolutions
404 Not Found: Usually means the URL is typed incorrectly or the route isn't defined in main.py.
Internal Server Error: Typically a "TemplateNotFound" error caused by index.html not being inside the templates folder.
Site Cannot Be Reached: The server is likely stopped. Restart using uvicorn main:app --reload.
  
  
## Reference Resources
**: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/) - Essential for API structure.
*   **SQLAlchemy Docs**: [https://docs.sqlalchemy.org/](https://docs.sqlalchemy.org/) - For database management.
*   **Real Python**: [https://realpython.com/](https://realpython.com/) - Best for practical tutorials.
*   **TextBlob Guide**: [https://textblob.readthedocs.io](https://textblob.readthedocs.io) - For AI sentiment analysis logic.

FastAPI Official Documentation: The primary guide for building the API and exploring the automatic /docs page.
SQLAlchemy Documentation: The definitive resource for managing database tables and queries.
Jinja2 Documentation: Explains how to use logic (like {% for %} loops) inside your HTML files.
TextBlob Official Docs: Details on how the AI analyzes sentiment and language
freecodecamp.org which offers masive, guidedpython courses.
AI learning and prompting resources AIDV-PT09 

## Learning Methodology & feedback
 Experimenting with Multiple Prompts
The Action: I started by asking for "next level projects," then narrowed it down to "web development," and finally asked for a "step-by-step" breakdown.

The Feedback: Instead of just getting a block of code, I used multiple prompts to 'zoom in' on the specific parts I didn't understand. This allowed me to learn the architecture (how the pieces fit) before writing the actual lines of code.

Refining Prompts Based on Errors (Dead-Ends)
The Action: When the "Internal Server Error" and "404 Not Found" appeared, I didn't give up. I prompted: "The website cannot be reached no matter how many times I try to reload" and "The folder is more of like [list of files]... is that correct?"

The Feedback: When I hit a dead-end with folder hierarchy, I refined my prompt by describing exactly what I saw on my screen. This allowed the AI to identify that my index.html was in the wrong spot. This taught me that clear communication with AI is just as important as the code itself.

 Improving Productivity and Clarity
The Action: I moved from a simple "Hello Name" script to an AI-powered database in a single session.

The Feedback: AI improved my productivity by acting as a Real-Time Debugger. Normally, a 'TypeError' or a 'Port Conflict' could stop a novice for days. With AI, I got an explanation of the error and a fix in seconds, which kept my momentum going and made complex topics like Asynchronous Servers feel simple.



## Working Codebase 
text
ai_support_portal/
├── main.py  
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from textblob import TextBlob
import traceback
import os

# 1. DATABASE SETUP
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./support.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    category = Column(String, default="General")

Base.metadata.create_all(bind=engine)

# 2. APP SETUP
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# 3. THE DASHBOARD (The Face)
@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    try:
        db = SessionLocal()
        # This fetches your tickets from the database
        all_tickets = db.query(Ticket).order_by(Ticket.id.desc()).all()
        db.close()
        # Convert to dicts
        tickets_dict = [{"id": t.id, "description": t.description, "category": t.category} for t in all_tickets]
        # Render manually
        template = templates.env.get_template("index.html")
        html = template.render(tickets=tickets_dict)
        return HTMLResponse(html)
    except Exception as e:
        return HTMLResponse(f"Error: {str(e)}\n{traceback.format_exc()}", status_code=500)

# 4. THE TICKET CREATOR (The Action)
from fastapi.responses import RedirectResponse

@app.post("/create-ticket/")
def create_ticket(problem: str = Form(...)): # <--- Tell it to look at the Form
    db = SessionLocal()
    blob = TextBlob(problem)

    # AI Analysis
    category = "Hardware" if "battery" in problem.lower() or "screen" in problem.lower() else "Software"
    mood = "Urgent" if blob.sentiment.polarity < -0.1 else "Neutral"

    new_ticket = Ticket(description=problem, category=f"{category} | {mood}")
    db.add(new_ticket)
    db.commit()
    db.close()

    # After saving, send the user back to the dashboard to see the new entry!
    return RedirectResponse(url="/", status_code=303)
@app.post("/clear-tickets/")
def clear_tickets():
    db = SessionLocal()
    db.query(Ticket).delete() # This wipes the table
    db.commit()
    db.close()
    return RedirectResponse(url="/", status_code=303)



Base.metadata.create_all(bind=engine)          
├── templates/         
│   └── index.html   
<!-- Ticket Table -->
        <table class="w-full text-left">
            <thead>
                <tr class="bg-gray-200 text-gray-700 uppercase text-sm">
                    <th class="p-4 border-b">ID</th>
                    <th class="p-4 border-b">Problem</th>
                    <th class="p-4 border-b">AI Analysis</th>
                </tr>
            </thead>
            <tbody>
               {% if not tickets %}
    <p class="text-center text-gray-500 py-10">No tickets yet. Type a problem above to start the AI analysis!</p>
{% endif %}
                {% for ticket in tickets %}
                <tr class="hover:bg-gray-50 border-b">
                    <td class="p-4 font-mono text-gray-400">{{ ticket.id }}</td>
                    <td class="p-4 text-gray-800">{{ ticket.description }}</td>
                    <td class="p-4">
                        {% if 'Urgent' in ticket.category %}
                        <span class="px-3 py-1 rounded-full text-xs font-bold bg-red-100 text-red-700 border border-red-200">
                            {{ ticket.category }}
                        </span>
                        {% else %}
                        <span class="px-3 py-1 rounded-full text-xs font-bold bg-blue-100 text-blue-700 border border-blue-200">
                            {{ ticket.category }}
                        </span>
                        {% endif %}
                    </td>
                </tr>
                {% endfor %}  
├── README.md          
└── TOOLKIT.md         




