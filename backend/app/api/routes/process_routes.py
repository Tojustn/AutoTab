from flask import request

def register_process_routes(app):
    @app.route("/api/process", methods = ["POST"])
    def process():
        return {"message": "HI"}
