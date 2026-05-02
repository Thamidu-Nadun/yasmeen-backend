from flask_sqlalchemy import SQLAlchemy
from playwright.sync_api import sync_playwright

db = SQLAlchemy()

playwright = None
browser = None

def init_browser():
    global playwright, browser
    if browser is None:
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch()