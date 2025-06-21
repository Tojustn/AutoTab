from flask import current_app as app
from app.api.GuitarTabs import Tab
def render_tabs():
    start_of_line =  "e-\nB-\nG-\nD-\nA-\nE-"
    block_of_lines = "-\n-\n-\n-\n-\n-"