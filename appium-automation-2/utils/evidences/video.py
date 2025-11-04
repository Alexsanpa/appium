# evidence_manager/video.py
import os
import base64
import time
import allure
from datetime import datetime
from .utils import EvidenceStateHelper
from .constants import (
    VIDEO_OUTPUT_PATH, 
    VIDEO_CODEC, 
    VIDEO_TIME_LIMIT, 
    VIDEO_TIMEOUT,
    ATTACH_TO_ALLURE
)


class VideoRecorder:
    @staticmethod
    def start_video_recording(driver, test_name: str):
        """
        Inicia la grabación de video usando la configuración centralizada
        """
        state = EvidenceStateHelper.get_state(driver)
        if state.get('is_recording', False):
            print("⚠️ Ya hay una grabación en curso")
            return

        try:
            state['test_name'] = test_name
            test_file_name = test_name.split("::")[0].replace("test_", "")
            state['test_module_name'] = test_file_name
            state['start_time'] = time.time()
            state['step_count'] = 0
            state['photo_paths'] = []
            state['video_path'] = None

            # Usar configuración centralizada
            driver.start_recording_screen(
                video_codec=VIDEO_CODEC, 
                time_limit=str(VIDEO_TIME_LIMIT)
            )
            time.sleep(2)
            state['is_recording'] = True

            timestamp = datetime.now().strftime("%H%M%S_%d_%m_%Y")
            state['video_start_timestamp'] = timestamp

            EvidenceStateHelper.set_state(driver, state)
            print(f"🎬 Grabación de video INICIADA para el test: {test_name}")
            print(f"   Codec: {VIDEO_CODEC} | Límite: {VIDEO_TIME_LIMIT}s")

        except Exception as e:
            print(f"⚠️ Error al iniciar la grabación: {e}")

    @staticmethod
    def stop_and_save_video_if_recording(driver, test_name: str):
        """
        Detiene la grabación y guarda el video usando la configuración centralizada
        """
        state = EvidenceStateHelper.get_state(driver)
        if not state.get('is_recording', False):
            print("ℹ️ No hay grabación activa para detener")
            return

        video_timestamp = state.get('video_start_timestamp', datetime.now().strftime("%H%M%S_%d_%m_%Y"))
        original_timeout = None
        
        try:
            # Usar timeout desde configuración
            original_timeout = driver.command_executor._timeout
            driver.command_executor._timeout = VIDEO_TIMEOUT

            print(f"⏳ Deteniendo y descargando video (timeout {VIDEO_TIMEOUT}s)...")
            video_base64 = driver.stop_recording_screen()
            driver.command_executor._timeout = original_timeout
            print("✅ Timeout del driver restaurado.")

            if not video_base64:
                print("❌ ERROR: El string Base64 del video está vacío.")
                return

            video_filename = f"{test_name}_{video_timestamp}.mp4"
            os.makedirs(VIDEO_OUTPUT_PATH, exist_ok=True)
            video_filepath = os.path.join(VIDEO_OUTPUT_PATH, video_filename)

            with open(video_filepath, "wb") as f:
                f.write(base64.b64decode(video_base64))

            print(f"✅ Video guardado en: {video_filepath}")

            state['video_path'] = video_filepath
            
            # Adjuntar a Allure si está habilitado
            if ATTACH_TO_ALLURE:
                try:
                    with open(video_filepath, "rb") as f:
                        allure.attach(
                            f.read(), 
                            name=f"Video - {video_filename}", 
                            attachment_type=allure.attachment_type.MP4
                        )
                    print("✅ Video adjuntado a Allure")
                except Exception as e:
                    print(f"⚠️ No se pudo adjuntar video a Allure: {e}")

            state['is_recording'] = False
            EvidenceStateHelper.set_state(driver, state)

        except Exception as e:
            if original_timeout is not None:
                driver.command_executor._timeout = original_timeout
            print(f"⚠️ Error FATAL al detener/guardar el video: {e}")