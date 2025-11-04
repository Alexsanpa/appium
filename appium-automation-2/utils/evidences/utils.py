# evidence_manager/utils.py
import os
import base64
import io
from datetime import datetime
import time
from PIL import Image
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors

def _format_duration_hms(seconds):
    try:
        s = int(seconds)
        hh = s // 3600
        mm_ = (s % 3600) // 60
        ss = s % 60
        hms = f"{hh:02d}:{mm_:02d}:{ss:02d}"
        if hh == 0:
            return f"{hms} ({mm_} min. {ss} seg.)"
        return hms
    except Exception:
        return str(seconds)

def _compress_image_to_bytes(img_path, max_dim=2000, quality=70):
    try:
        with Image.open(img_path) as im:
            if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
                bg = Image.new("RGB", im.size, (255, 255, 255))
                bg.paste(im, mask=im.split()[-1])
                im = bg
            else:
                im = im.convert("RGB")
            w, h = im.size
            max_side = max(w, h)
            if max_side > max_dim:
                scale = max_dim / max_side
                new_w = int(w * scale)
                new_h = int(h * scale)
                im = im.resize((new_w, new_h), Image.LANCZOS)
            bio = io.BytesIO()
            im.save(bio, format="JPEG", quality=quality, optimize=True)
            bio.seek(0)
            return bio
    except Exception as e:
        print(f"⚠️ Error al comprimir imagen {img_path}: {e}")
        return None

def _file_to_base64(filepath, mime_type):
    try:
        if not os.path.exists(filepath):
            return ""
        with open(filepath, "rb") as f:
            encoded_string = base64.b64encode(f.read()).decode('utf-8')
            return f"data:{mime_type};base64,{encoded_string}"
    except Exception as e:
        print(f"⚠️ Error al convertir {filepath} a Base64: {e}")
        return ""

class EvidenceStateHelper:
    @staticmethod
    def get_state(driver):
        return getattr(driver, 'evidence_state', {})

    @staticmethod
    def set_state(driver, state):
        setattr(driver, 'evidence_state', state)

class FilenameGenerator:
    @staticmethod
    def generate_filename_parts(driver):
        state = EvidenceStateHelper.get_state(driver)
        if 'photo_paths' not in state:
            state['photo_paths'] = []
        step_count = state.get('step_count', 0) + 1
        state['step_count'] = step_count
        step_prefix = f"{step_count:02d}"
        now = datetime.now()
        timestamp = now.strftime("%H%M%S_%d_%m_%Y")
        test_name = state.get('test_name', 'UNKNOWN_TEST')
        filename_base = f"{step_prefix}_{test_name}_{timestamp}"
        EvidenceStateHelper.set_state(driver, state)
        return filename_base, timestamp
