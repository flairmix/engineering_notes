from litestar import Controller, post, get, Response
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
import pdfkit
from datetime import datetime
from typing import Dict, Any

# Настройка Jinja2: ищем шаблоны в templates/calculations/
env = Environment(loader=FileSystemLoader("app/templates/calculations"))

# Путь к wkhtmltopdf (настройте под свою ОС)
WKHTMLTOPDF_PATH = r"S:\Общие документы\Донченко\flair_smoke\wkhtmltox\bin\wkhtmltopdf.exe"

class PDFController(Controller):
    path = "/pdf"

    @post("/generate")
    async def generate_pdf(
        self,
        data: Dict[str, Any]
    ) -> Response:
        """
        Генерирует PDF по указанному типу расчёта.
        Ожидаемые поля в data:
        - calculation_type: str (например, "smoke_intake")
        - index, project_name, system_name, params, results, conclusion (как раньше)
        """
        calculation_type = data.get("calculation_type")
        if not calculation_type:
            return Response(
                content={"error": "Параметр calculation_type не указан"},
                status_code=400,
                media_type="application/json"
            )

        # Формируем имя шаблона (добавляем .html)
        template_name = f"{calculation_type}.html"

        try:
            # Пытаемся загрузить шаблон
            template = env.get_template(template_name)
        except TemplateNotFound:
            return Response(
                content={"error": f"Шаблон '{template_name}' не найден"},
                status_code=404,
                media_type="application/json"
            )

        # Подготовка контекста (как раньше)
        context = {
            "index": data.get("index", "—"),
            "project_name": data.get("project_name", "Не указано"),
            "date": datetime.now().strftime("%d.%m.%Y"),
            "system_name": data.get("system_name", "Не указано"),
            "params": data.get("params", {}),
            "results": data.get("results", []),
            "conclusion": data.get("conclusion", "Заключение отсутствует.")
        }

        # Рендеринг HTML
        html_output = template.render(context)

        # Генерация PDF
        config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)
        pdf_bytes = pdfkit.from_string(
            html_output,
            False,
            configuration=config,
            options={
                "page-size": "A4",
                "margin-top": "20mm",
                "margin-right": "20mm",
                "margin-bottom": "20mm",
                "margin-left": "20mm",
                "encoding": "UTF-8",
                "no-outline": None,
            },
        )

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{calculation_type}_report.pdf"'
            }
        )

    @get("/templates")
    async def list_templates(self) -> Response:
        """
        Возвращает список доступных шаблонов (для отладки).
        """
        try:
            # Получаем список всех шаблонов в директории
            templates = env.list_templates()
            return Response(
                content={"templates": templates},
                media_type="application/json"
            )
        except Exception as e:
            return Response(
                content={"error": str(e)},
                status_code=500,
                media_type="application/json"
            )
