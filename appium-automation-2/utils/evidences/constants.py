"""
Constantes del sistema de evidencias
Ahora usa el sistema de configuración centralizado
"""
from config.settings import evidence

# Rutas de salida (desde la configuración)
VIDEO_OUTPUT_PATH = str(evidence.VIDEO_DIR)
PHOTO_OUTPUT_PATH = str(evidence.PHOTO_DIR)
HTML_OUTPUT_PATH = str(evidence.HTML_DIR)
PDF_OUTPUT_PATH = str(evidence.PDF_DIR)

# Configuración de video
VIDEO_ENABLED = evidence.VIDEO_ENABLED
VIDEO_CODEC = evidence.VIDEO_CODEC
VIDEO_TIME_LIMIT = evidence.VIDEO_TIME_LIMIT
VIDEO_TIMEOUT = evidence.VIDEO_TIMEOUT

# Configuración de imágenes
IMAGE_MAX_DIMENSION = evidence.IMAGE_MAX_DIMENSION
IMAGE_QUALITY = evidence.IMAGE_QUALITY

# Configuración de reportes
GENERATE_HTML = evidence.GENERATE_HTML
GENERATE_PDF = evidence.GENERATE_PDF
ATTACH_TO_ALLURE = evidence.ATTACH_TO_ALLURE