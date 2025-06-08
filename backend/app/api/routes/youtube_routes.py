from flask import request

def register_youtube_routes(app):
    @app.route("/api/youtube/download", methods = ["GET"])
    def download():
        return {"message": "complete"}