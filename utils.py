import json
from wikipedia_scraper import scrape_wikipedia
from court_analysis import analyze_court_data

def handle_question(question_text, attachments):
    question_text_lower = question_text.lower()

    if "highest grossing films" in question_text_lower:
        return scrape_wikipedia(question_text)

    elif "high court" in question_text_lower:
        return analyze_court_data(question_text, attachments)

    else:
        return {"error": "Unknown question type"}
