from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from textblob import TextBlob
import traceback

# 1. DATABASE SETUP
DATABASE_URL = "sqlite:///./support.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
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

