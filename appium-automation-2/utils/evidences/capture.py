# evidence_manager/capture.py
import os
import inspect
import allure
from .utils import EvidenceStateHelper, FilenameGenerator
from .utils import _file_to_base64, _compress_image_to_bytes  # not used here but kept for parity
from .constants import PHOTO_OUTPUT_PATH

class EvidenceCapturer:
    """Encapsula la lógica para tomar capturas y extraer metadatos del docstring."""

    @staticmethod
    def take_evidence(driver, step_log: str = "N/A"):
        step_description = "N/A: Docstring no encontrado o formato incorrecto."
        expected_result = "N/A: Docstring no encontrado o formato incorrecto."

        try:
            # inspeccionamos varios frames hacia arriba buscando docstring
            stack = inspect.stack()
            found = False
            for frame_info in stack[1:12]:  # limitar búsqueda a los 11 frames superiores
                f = frame_info.frame
                func_name = f.f_code.co_name

                # 1) si es método de instancia
                if 'self' in f.f_locals:
                    try:
                        cls = f.f_locals['self'].__class__
                        if hasattr(cls, func_name):
                            candidate = getattr(cls, func_name)
                            docstring = inspect.getdoc(candidate)
                            if docstring:
                                found = True
                                break
                    except Exception:
                        pass

                # 2) función a nivel de módulo
                try:
                    module = inspect.getmodule(f)
                    if module and hasattr(module, func_name):
                        candidate = getattr(module, func_name)
                        # evitar leer docstring del propio módulo de evidencias
                        module_name = getattr(module, "__name__", "")
                        if module_name and "utils.evidences" not in module_name:
                            docstring = inspect.getdoc(candidate)
                            if docstring:
                                found = True
                                break
                except Exception:
                    pass

                # 3) como último recurso, revisar si en locals hay un objeto función con ese nombre
                try:
                    if func_name in f.f_locals:
                        candidate = f.f_locals.get(func_name)
                        docstring = inspect.getdoc(candidate) if candidate is not None else None
                        if docstring:
                            found = True
                            break
                except Exception:
                    pass

            # Si encontramos docstring en 'docstring' variable, procesarla
            if found and docstring:
                lines = [line.strip() for line in docstring.split('\n') if line.strip()]
                for line in lines:
                    low = line.lower()
                    if low.startswith("descripcion:"):
                        step_description = line.split(":", 1)[1].strip()
                    elif low.startswith("resultado esperado:"):
                        expected_result = line.split(":", 1)[1].strip()
        except Exception as e:
            # no fallamos el flujo por este error, solo registramos
            print(f"⚠️ Error al extraer el docstring del llamador: '{e}'")

        # Generar nombres y timestamp (incrementa contador)
        filename_base, _ = FilenameGenerator.generate_filename_parts(driver)
        state = EvidenceStateHelper.get_state(driver)

        # Captura de pantalla
        try:
            photo_filepath = os.path.join(PHOTO_OUTPUT_PATH, f"{filename_base}.png")
            os.makedirs(PHOTO_OUTPUT_PATH, exist_ok=True)
            driver.save_screenshot(photo_filepath)
            print(f"📸 Evidencia FÍSICA guardada en: {photo_filepath}")

            state.setdefault('photo_paths', []).append({
                "path": photo_filepath,
                "description": step_description,
                "expected": expected_result,
                "log": step_log,
                "step_number": state['step_count']
            })
            EvidenceStateHelper.set_state(driver, state)

            with open(photo_filepath, "rb") as f:
                allure.attach(
                    f.read(),
                    name=f"Captura Allure - {filename_base}",
                    attachment_type=allure.attachment_type.PNG
                )

        except Exception as e:
            print(f"⚠️ Error al tomar la captura de pantalla: {e}")
