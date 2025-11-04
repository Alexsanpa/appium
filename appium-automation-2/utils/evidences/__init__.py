
from .video import VideoRecorder
from .capture import EvidenceCapturer
from .report import Reporter

# compat API (mantiene las mismas funciones que usabas)
_default_manager = {
    "video": VideoRecorder,
    "capture": EvidenceCapturer,
    "report": Reporter
}

def start_video_recording(driver, test_name: str):
    return _default_manager["video"].start_video_recording(driver, test_name)

def take_evidence(driver, step_log: str = "N/A"):
    return _default_manager["capture"].take_evidence(driver, step_log)

def stop_and_save_video_if_recording(driver, test_name: str):
    return _default_manager["video"].stop_and_save_video_if_recording(driver, test_name)

def generate_html_report(driver, status="PASSED", company_logo_base64=None):
    return _default_manager["report"].generate_html_report(driver, status=status, company_logo_base64=company_logo_base64)

def generate_pdf_report(driver, status="PASSED", company_name=None):
    return _default_manager["report"].generate_pdf_report(driver, status=status, company_name=company_name)

__all__ = [
    "start_video_recording",
    "take_evidence",
    "stop_and_save_video_if_recording",
    "generate_html_report",
    "generate_pdf_report"
]
