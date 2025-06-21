from flask import session, has_request_context
import uuid
import os 
import shutil
def get_session_id():
    """Generate a new unique session ID"""
    return uuid.uuid4()

def init_session():
    session["session_id"] = get_session_id()


def get_user_paths(): 
    # If no request context, return None
    if not has_request_context():
        return None
    session_id = str(session.get("session_id"))
    if not session_id:
        return None
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
    # print(base_dir)

    upload_path = os.path.join(base_dir, 'user_data', session_id, 'static', 'raw_video')
    file_path = os.path.join(base_dir, 'user_data', session_id, 'static', 'frames')
    processed_path = os.path.join(base_dir, 'user_data', session_id, 'static', 'processed_frames')
    return {
        "upload_path": upload_path,
        "file_path": file_path,
        "processed_path": processed_path
    }
def cleanup_user_data(exception):
    user_paths = get_user_paths()
    if user_paths is not None:
        if os.path.exists(user_paths["upload_path"]):
            shutil.rmtree(user_paths["upload_path"])
        if os.path.exists(user_paths["file_path"]):
            shutil.rmtree(user_paths["file_path"])
        if os.path.exists(user_paths["processed_path"]):
            shutil.rmtree(user_paths["processed_path"])