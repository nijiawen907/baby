import threading

# globals.py

_expression_status = False
_pose_status = False
_status_lock = threading.Lock()

def set_expression_status(value):
    global _expression_status, _status_lock
    with _status_lock:
        _expression_status = value

def get_expression_status():
    global _expression_status, _status_lock
    with _status_lock:
        return _expression_status

# 同样可以封装 pose_status
def set_pose_status(value):
    global _pose_status, _status_lock
    with _status_lock:
        _pose_status = value

def get_pose_status():
    global _pose_status, _status_lock
    with _status_lock:
        return _pose_status