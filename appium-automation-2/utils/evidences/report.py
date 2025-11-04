# evidence_manager/report.py
import os
import time
import allure
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader, simpleSplit
from reportlab.lib.units import mm
from reportlab.lib import colors

from .utils import EvidenceStateHelper
from .utils import _compress_image_to_bytes, _file_to_base64, _format_duration_hms
from .constants import HTML_OUTPUT_PATH, PDF_OUTPUT_PATH, PHOTO_OUTPUT_PATH, VIDEO_OUTPUT_PATH

class Reporter:
    @staticmethod
    def generate_html_report(driver, status="PASSED", company_logo_base64=None):
        state = EvidenceStateHelper.get_state(driver)
        test_name_full = state.get('test_name', 'UNKNOWN_TEST::UNKNOWN_CLASS::unknown_method')
        module_name = state.get('test_module_name', 'UNKNOWN_FILE').upper()
        test_method_name = test_name_full.split("::")[-1]

        start_time = state.get('start_time', time.time())
        end_time = time.time()
        duration_seconds = end_time - start_time
        duration_formatted = f"{duration_seconds:.2f}s"
        execution_date = datetime.fromtimestamp(start_time).strftime("%d/%m/%Y %H:%M:%S")

        status = state.get('final_status', status)
        video_path = state.get('video_path')
        photos_data = state.get('photo_paths', [])

        # Build step HTML (kept simple, identical structure)
        step_details_html = ""
        for data in photos_data:
            image_base64_data = _file_to_base64(data['path'], "image/png")
            filename = os.path.basename(data['path'])
            step_details_html += f"""
            <section class="card step-card">
                <header class="step-header">
                    <h3>PASO {data['step_number']}</h3>
                    <span class="badge">Evidencia: {filename}</span>
                </header>
                <div class="step-body">
                    <div class="meta">
                        <div><strong>Descripción:</strong> <span class="meta-text">{data['description']}</span></div>
                        <div><strong>Resultado Esperado:</strong> <span class="meta-text">{data['expected']}</span></div>
                        <div><strong>Acción (Log):</strong> <span class="meta-text">{data.get('log','')}</span></div>
                    </div>
                    <div class="thumb">
                        <img src="{image_base64_data}" alt="{filename}" />
                    </div>
                </div>
            </section>
            """

        video_embed_html = ""
        if video_path:
            video_base64_data = _file_to_base64(video_path, "video/mp4")
            if video_base64_data:
                video_embed_html = f"""
                <section class="card video-card">
                    <h3>🎬 Grabación de la Ejecución</h3>
                    <div class="video-wrap">
                        <video controls preload="none">
                            <source src="{video_base64_data}" type="video/mp4">
                            Tu navegador no soporta el tag de video.
                        </video>
                    </div>
                </section>
                """

        status_class = "pass" if status == "PASSED" else "fail"
        status_icon = "✅" if status == "PASSED" else "❌"

        error_html = ""
        if state.get("error"):
            err_text = str(state.get("error"))
            error_html = f"""
            <section class="card error-card">
                <h3>Error del Test</h3>
                <pre class="error-pre">{err_text}</pre>
            </section>
            """

        # prettier CSS
        styles = """
        :root{
            --bg:#f6f8fa;
            --card:#ffffff;
            --muted:#6b7280;
            --accent:#0b5fff;
            --green:#1e7e34;
            --red:#c0392b;
            --surface:#eef2f6;
            --radius:8px;
        }
        html,body{height:100%;margin:0;font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial; background:var(--bg); color:#222;}
        .container{max-width:980px;margin:28px auto;padding:16px;}
        header.report-header{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:18px;}
        .report-title{font-size:20px;margin:0;color:#0f172a;font-weight:700;}
        .meta-block{background:linear-gradient(90deg,#fff,#fbfdff);padding:14px;border-radius:var(--radius);box-shadow:0 1px 2px rgba(16,24,40,0.04);display:flex;gap:12px;align-items:center;}
        .meta-left{flex:1;}
        .meta-right{text-align:right;min-width:180px;}
        .report-key{display:block;color:var(--muted);font-size:13px;margin-bottom:6px;}
        .report-val{font-weight:700;color:#0b2545;font-size:14px;}
        .status-pill{display:inline-block;padding:6px 10px;border-radius:999px;font-weight:700;}
        .status-pill.pass{background:#e6fff0;color:var(--green);border:1px solid rgba(30,126,52,0.08);}
        .status-pill.fail{background:#fff1f0;color:var(--red);border:1px solid rgba(192,57,43,0.08);}
        .cards{margin-top:18px;display:flex;flex-direction:column;gap:12px;}
        .card{background:var(--card);border-radius:var(--radius);padding:12px;box-shadow:0 6px 18px rgba(11,31,72,0.03);border:1px solid rgba(15,23,42,0.04);}
        .card h3{margin:0 0 8px 0;font-size:15px;color:#0b2545;}
        .error-card{border-left:4px solid var(--red);background:#fff6f6;color:var(--red);}
        .error-pre{white-space:pre-wrap;font-size:12px;color:#6b1b1b;margin:0;padding:8px;border-radius:6px;background:rgba(231,76,60,0.04);}
        /* step card */
        .step-card .step-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;}
        .step-card .badge{background:var(--surface);padding:6px 8px;border-radius:6px;font-size:12px;color:var(--muted);}
        .step-body{display:flex;gap:12px;align-items:flex-start;}
        .step-body .meta{flex:1;font-size:13px;color:#334155;}
        .step-body .meta .meta-text{display:inline-block;margin-left:6px;color:#0b2545;font-weight:500;}
        .thumb{width:260px;flex:0 0 260px;display:flex;align-items:center;justify-content:center;background:#fbfdff;border-radius:6px;padding:6px;}
        .thumb img{max-width:100%;max-height:200px;border-radius:4px;object-fit:contain;display:block;}
        .video-wrap video{width:100%;height:auto;border-radius:6px;background:#000;}
        /* responsive */
        @media (max-width:820px){
            .step-body{flex-direction:column;}
            .thumb{width:100%;}
            .meta-right{text-align:left;}
        }
        footer.report-footer{margin-top:18px;font-size:12px;color:var(--muted);display:flex;justify-content:space-between;align-items:center;}
        """

        report_html = f"""<!doctype html>
        <html lang="es">
        <head>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width,initial-scale=1" />
            <title>Reporte: {test_method_name}</title>
            <style>{styles}</style>
        </head>
        <body>
            <div class="container">
                <header class="report-header">
                    <div>
                        <h1 class="report-title">Reporte: {test_method_name}</h1>
                        <div style="color:var(--muted);font-size:13px;margin-top:6px;">{module_name}.py · Ejecutado: {execution_date}</div>
                    </div>
                    <div style="text-align:right;">
                        <div class="status-pill {status_class}">{status_icon} {status.upper()}</div>
                        <div style="color:var(--muted);font-size:12px;margin-top:8px;">Duración: {duration_formatted}</div>
                    </div>
                </header>

                <section class="meta-block">
                    <div class="meta-left">
                        <span class="report-key">Caso de Prueba (Método)</span>
                        <div class="report-val">{test_method_name}</div>
                    </div>
                    <div class="meta-right">
                        <div class="report-key">Total de Pasos</div>
                        <div class="report-val">{len(photos_data)}</div>
                    </div>
                </section>

                <div class="cards">
                    {error_html}
                    {video_embed_html}
                    {step_details_html}
                </div>

                <footer class="report-footer">
                    <div>Archivos locales: Capturas: <code>{os.path.abspath(PHOTO_OUTPUT_PATH)}</code></div>
                    <div>Video: <code>{os.path.abspath(VIDEO_OUTPUT_PATH)}</code></div>
                </footer>
            </div>
        </body>
        </html>
        """

        os.makedirs(HTML_OUTPUT_PATH, exist_ok=True)
        report_filename = f"reporte_{test_method_name}_{datetime.now().strftime('%H%M%S')}.html"
        report_filepath = os.path.join(HTML_OUTPUT_PATH, report_filename)

        try:
            with open(report_filepath, "w", encoding="utf-8") as f:
                f.write(report_html)
            print(f"✅ Reporte HTML profesional generado en: {report_filepath}")
        except Exception as e:
            print(f"⚠️ Error al guardar el reporte HTML: {e}")

        try:
            outputs = Reporter.generate_pdf_report(driver, status=status, company_name="MiEmpresa")
            if outputs:
                print(f"✅ PDF de capturas generado en: {outputs}")
        except Exception as e:
            print(f"⚠️ Error al generar PDF/Excel automáticamente: {e}")

    @staticmethod
    def generate_pdf_report(driver, status="PASSED", company_name=None):
        """
        Genera PDF:
        - Página 1: Resumen (y Paso 1 debajo si existe).
        - Páginas siguientes: Paso 2..N cada uno en página propia.
        El Log se muestra únicamente en la página del paso que contenga 'log'.
        """
        try:
            state = EvidenceStateHelper.get_state(driver)
            test_name_full = state.get("test_name", "UNKNOWN_TEST::UNKNOWN_CLASS::unknown_method")
            module_name = state.get("test_module_name", "UNKNOWN_FILE").upper()
            test_method_name = test_name_full.split("::")[-1]
            test_case_id = state.get("test_case_id", f"TC_{module_name}_{datetime.now().strftime('%d%m%y%H%M%S')}")
            start_time = state.get("start_time", time.time())
            end_time = time.time()
            duration_seconds = max(0, end_time - start_time)
            duration_formatted = _format_duration_hms(duration_seconds)
            execution_date = datetime.fromtimestamp(start_time).strftime("%d/%m/%Y %H:%M:%S")
            photos_data = state.get("photo_paths", []) or []

            os.makedirs(PDF_OUTPUT_PATH, exist_ok=True)
            timestamp = datetime.now().strftime("%H%M%S")
            pdf_filepath = os.path.join(PDF_OUTPUT_PATH, f"reporte_{test_method_name}_{timestamp}.pdf")

            page_w, page_h = A4
            margin = 18 * mm
            c = canvas.Canvas(pdf_filepath, pagesize=A4)
            c.setTitle(f"Reporte - {test_method_name}")

            # -------------------------
            # PÁGINA 1: RESUMEN (y opcional Paso 1 debajo)
            # -------------------------
            c.setFont("Helvetica-Bold", 20)
            title_y = page_h - margin
            c.drawString(margin, title_y, "Resumen de la Ejecución")

            # Línea naranja
            line_y = title_y - 8
            c.setLineWidth(2)
            c.setStrokeColorRGB(0.95, 0.55, 0.12)
            c.line(margin, line_y, page_w - margin, line_y)
            c.setStrokeColorRGB(0, 0, 0)

            # Tabla resumen
            table_x = margin
            table_w = page_w - 2 * margin
            row_height = 14
            spacing = 8
            start_y = line_y - 22

            rows = [
                ("Caso de Prueba (Método):", test_method_name),
                ("Archivo de Prueba (Módulo):", f"{module_name}.py"),
                ("Fecha de Ejecución:", execution_date),
                ("Tiempo Total de Ejecución:", duration_formatted),
                ("Total de Pasos:", str(len(photos_data))),
                ("Estado Final:", status.upper()),
            ]

            c.setFont("Helvetica-Bold", 10)
            label_x = table_x + 6
            value_x = table_x + table_w - 6
            row_y = start_y
            for idx, (label, value) in enumerate(rows):
                c.setFillColorRGB(0.14, 0.24, 0.31)
                c.setFont("Helvetica-Bold", 10)
                c.drawString(label_x, row_y, label)
                c.setFont("Helvetica", 10)
                c.setFillColorRGB(0.05, 0.2, 0.35)
                if label.lower().startswith("archivo"):
                    c.setFont("Helvetica-Bold", 10)
                    c.setFillColorRGB(0.06, 0.45, 0.75)
                    c.drawRightString(value_x, row_y, value)
                    c.setFont("Helvetica", 10)
                    c.setFillColorRGB(0, 0, 0)
                elif label.lower().startswith("estado"):
                    pill_w = 86
                    pill_h = 14
                    pill_x = value_x - pill_w + 6
                    pill_y = row_y - 4
                    if str(status).upper() in ("PASSED", "PASS", "OK"):
                        c.setFillColorRGB(0.78, 0.95, 0.80)
                        c.roundRect(pill_x, pill_y, pill_w, pill_h, 6, stroke=0, fill=1)
                        c.setFillColorRGB(0, 0.45, 0.14)
                        c.setFont("Helvetica-Bold", 9)
                        c.drawString(pill_x + 6, pill_y + 3, "✅  " + str(status).upper())
                    else:
                        c.setFillColorRGB(0.99, 0.85, 0.85)
                        c.roundRect(pill_x, pill_y, pill_w, pill_h, 6, stroke=0, fill=1)
                        c.setFillColorRGB(0.55, 0.06, 0.06)
                        c.setFont("Helvetica-Bold", 9)
                        c.drawString(pill_x + 6, pill_y + 3, "❌  " + str(status).upper())
                    c.setFillColorRGB(0, 0, 0)
                else:
                    c.drawRightString(value_x, row_y, value)

                row_y -= (row_height + spacing)
                c.setLineWidth(0.3)
                c.setStrokeColorRGB(0.85, 0.85, 0.85)
                c.line(table_x + 2, row_y + 13, table_x + table_w - 2, row_y + 13)
                c.setStrokeColorRGB(0, 0, 0)

            # espacio disponible bajo la tabla en la portada
            content_start_y = row_y - 12

            def _draw_text_block_on_page(cobj, item, top_y, page_top):
                """
                Dibuja descripción, resultado esperado y LOG (solo si existe y si el estado final es FAILED)
                en la página actual, empezando desde top_y (coordenada Y).
                Devuelve la Y máxima disponible para la imagen (img_top_limit).
                """
                desc_w = page_w - 2 * margin

                # Descripción
                cobj.setFont("Helvetica-Bold", 9)
                cobj.drawString(margin, top_y, "Descripcion:")
                cobj.setFont("Helvetica", 9)
                descr_x = margin + 80
                descr_w = page_w - descr_x - margin
                descr_lines = simpleSplit(str(item.get("description", "") or ""), "Helvetica", 9, descr_w)
                ty = top_y
                for ln in descr_lines:
                    cobj.drawString(descr_x, ty, ln)
                    ty -= 11

                # Resultado esperado
                ty -= 4
                cobj.setFont("Helvetica-Bold", 9)
                cobj.drawString(margin, ty, "Resultado Esperado:")
                cobj.setFont("Helvetica", 9)
                exp_x = margin + 110
                exp_w = page_w - exp_x - margin
                exp_lines = simpleSplit(str(item.get("expected", "") or ""), "Helvetica", 9, exp_w)
                for ln in exp_lines:
                    cobj.drawString(exp_x, ty, ln)
                    ty -= 11

                # LOG — solo mostrar si el estado final es FAILED y el log contiene contenido útil
                log_text = item.get("log", "")
                status_upper = str(status).upper()
                if status_upper == "FAILED":
                    log_norm = str(log_text or "").strip()
                    # defender contra "N/A" u valores irrelevantes
                    if log_norm and log_norm.lower() != "n/a":
                        # considerar como log real si contiene keywords o es razonablemente largo
                        low = log_norm.lower()
                        consider = ("exception" in low) or ("traceback" in low) or ("error" in low) or (len(log_norm) > 20)
                        if consider:
                            ty -= 6
                            # altura de caja tentativa
                            box_h = 36 * mm
                            box_top = ty
                            box_bottom = box_top - box_h
                            min_bottom = margin + 18
                            if box_bottom < min_bottom:
                                # ajustar box_h para no invadir margen inferior
                                box_h = box_top - min_bottom
                                box_bottom = min_bottom
                            cobj.setFillColorRGB(0.99, 0.94, 0.94)
                            cobj.rect(margin, box_bottom, page_w - 2 * margin, box_h, stroke=0, fill=1)
                            cobj.setFillColorRGB(0.55, 0.06, 0.06)
                            cobj.setFont("Helvetica-Bold", 9)
                            cobj.drawString(margin + 6, box_bottom + box_h - 12, "Log / Error:")
                            cobj.setFont("Helvetica", 8)
                            wrapped = simpleSplit(log_norm, "Helvetica", 8, page_w - 2 * margin - 12)
                            ly = box_bottom + box_h - 26
                            for line in wrapped:
                                if ly < box_bottom + 6:
                                    break
                                cobj.drawString(margin + 6, ly, line)
                                ly -= 9
                            cobj.setFillColorRGB(0, 0, 0)
                            img_top_limit = box_bottom - 8
                            return img_top_limit

                # no log mostrado -> imagen disponible justo debajo del último texto
                img_top_limit = ty - 12
                return img_top_limit

            # -------------------------
            # Dibujar Paso 1 en la portada (si existe)
            # -------------------------
            if photos_data:
                first = photos_data[0]
                # título del paso en portada
                c.setFont("Helvetica-Bold", 12)

                # decidir si marcar como error en portada: solo si estado es FAILED y el log del paso 1 es relevante
                is_error_first = False
                status_upper = str(status).upper()
                if status_upper == "FAILED":
                    ll = str(first.get("log", "") or "").strip().lower()
                    if ll and ll != "n/a" and ("exception" in ll or "traceback" in ll or "error" in ll or len(ll) > 20):
                        is_error_first = True

                if is_error_first:
                    c.setFillColorRGB(0.6, 0.08, 0.08)
                    c.drawString(margin, content_start_y, f"Paso {first.get('step_number', 1)}  ❌")
                else:
                    c.setFillColorRGB(0.06, 0.2, 0.45)
                    c.drawString(margin, content_start_y, f"Paso {first.get('step_number', 1)}")
                c.setFillColorRGB(0, 0, 0)

                # dibujar la parte textual y obtener el límite superior disponible para la imagen
                img_top = _draw_text_block_on_page(c, first, content_start_y - 18, page_h)

                # imagen en la portada: escalar para el espacio disponible (img_top - margin - footer)
                img_bottom_margin = margin + 18
                avail_h = img_top - img_bottom_margin
                img_path = first.get("path")
                if img_path and os.path.exists(img_path) and avail_h > (20 * mm):
                    img_bio = _compress_image_to_bytes(img_path, max_dim=1400, quality=75)
                    if img_bio:
                        try:
                            img_reader = ImageReader(img_bio)
                            iw, ih = img_reader.getSize()
                            max_w = page_w - 2 * margin
                            max_h = avail_h
                            scale = min(max_w / iw, max_h / ih, 1.0)
                            dw, dh = iw * scale, ih * scale
                            img_x = (page_w - dw) / 2
                            img_y = img_bottom_margin + (avail_h - dh) / 2
                            c.drawImage(img_reader, img_x, img_y, width=dw, height=dh, preserveAspectRatio=True)
                        except Exception as e:
                            c.setFont("Helvetica-Oblique", 9)
                            c.drawString(margin, img_bottom_margin + 6, f"Error incrustando imagen: {e}")
                else:
                    c.setFont("Helvetica-Oblique", 8)
                    c.drawCentredString(page_w / 2, margin + 28, "No hay imagen o espacio insuficiente para mostrarla en la portada.")

                # pie y siguiente página
                c.setFont("Helvetica-Oblique", 8)
                c.drawRightString(page_w - margin, margin / 2 + 6, f"{test_case_id} - Paso {first.get('step_number', 1)}")
                c.showPage()
            else:
                c.showPage()


            # -------------------------
            # Páginas siguientes: Paso 2..N (cada uno en su página correspondiente)
            # -------------------------
            if len(photos_data) > 1:
                for idx, item in enumerate(photos_data[1:], start=2):
                    _draw_step_page = None  # asegurar no sombra de nombres previos
                    # Reusar la rutina pero dibujando en página nueva
                    def _draw_page_for_item(it, stepnum, canvas_obj):
                        # copiar la misma lógica que en _draw_step_page (pero aquí como closure)
                        cobj = canvas_obj
                        # determinar si es paso con error
                        has_log = bool(it.get("log"))
                        is_error = False
                        if has_log:
                            ll = str(it.get("log", "")).lower()
                            if "exception" in ll or "traceback" in ll or "error" in ll or str(status).upper() == "FAILED":
                                is_error = True
                        # header
                        cobj.setFont("Helvetica-Bold", 12)
                        if is_error:
                            cobj.setFillColorRGB(0.6, 0.08, 0.08)
                            cobj.drawString(margin, page_h - margin, f"Paso {stepnum}  ❌")
                        else:
                            cobj.setFillColorRGB(0.06, 0.2, 0.45)
                            cobj.drawString(margin, page_h - margin, f"Paso {stepnum}")
                        cobj.setFillColorRGB(0, 0, 0)

                        # dibujar texto y log (reutilizamos helper)
                        top_y_local = page_h - margin - 18
                        img_top_local = _draw_text_block_on_page(cobj, it, top_y_local, page_h)

                        # imagen
                        img_path_local = it.get("path")
                        img_bottom_margin_local = margin + 18
                        avail_h_local = img_top_local - img_bottom_margin_local
                        if img_path_local and os.path.exists(img_path_local) and avail_h_local > (18 * mm):
                            img_bio_local = _compress_image_to_bytes(img_path_local, max_dim=1400, quality=75)
                            if img_bio_local:
                                try:
                                    img_reader_local = ImageReader(img_bio_local)
                                    iw_l, ih_l = img_reader_local.getSize()
                                    max_w_l = page_w - 2 * margin
                                    max_h_l = avail_h_local
                                    scale_l = min(max_w_l / iw_l, max_h_l / ih_l, 1.0)
                                    dw_l, dh_l = iw_l * scale_l, ih_l * scale_l
                                    img_x_l = (page_w - dw_l) / 2
                                    img_y_l = img_bottom_margin_local + (avail_h_local - dh_l) / 2
                                    cobj.drawImage(img_reader_local, img_x_l, img_y_l, width=dw_l, height=dh_l, preserveAspectRatio=True)
                                except Exception as e:
                                    cobj.setFont("Helvetica-Oblique", 9)
                                    cobj.drawString(margin, img_bottom_margin_local + 6, f"Error incrustando imagen: {e}")
                        else:
                            cobj.setFont("Helvetica-Oblique", 8)
                            cobj.drawCentredString(page_w / 2, margin + 28, "No hay imagen o espacio insuficiente para mostrarla.")

                        # pie
                        cobj.setFont("Helvetica-Oblique", 8)
                        cobj.drawRightString(page_w - margin, margin / 2 + 6, f"{test_case_id} - Paso {stepnum}")
                        cobj.showPage()

                    _draw_page_for_item(item, idx, c)

            # Guardar PDF
            c.save()
            print(f"✅ PDF generado en: {pdf_filepath}")

            try:
                with open(pdf_filepath, "rb") as f:
                    allure.attach(f.read(), name=os.path.basename(pdf_filepath), attachment_type=allure.attachment_type.PDF)
            except Exception as e:
                print(f"⚠️ No se pudo adjuntar PDF a Allure: {e}")

            return pdf_filepath

        except Exception as e:
            print(f"⚠️ Error generando PDF profesional: {e}")
            return None
