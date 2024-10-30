from io import BytesIO
from docxtpl import DocxTemplate
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from schemas.ReportData import ReportData

app = FastAPI()


@app.post("/generate_report/")
async def generate_report(report_data: ReportData):
    doc = DocxTemplate("report_template/template.docx")
    context = {
        "cost": report_data.cost,
        "duration": report_data.duration,
        "afp": report_data.afp,
        "start_date": report_data.start_date.strftime("%Y-%m-%d"),
        "end_date": report_data.end_date.strftime("%Y-%m-%d"),
        "today_date": report_data.today_date.strftime("%Y-%m-%d"),
        "ei": report_data.ei,
        "eq": report_data.eq,
        "eo": report_data.eo,
        "ilf": report_data.ilf,
        "eif": report_data.eif,
    }
    doc.render(context)

    output = BytesIO()
    doc.save(output)
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": "attachment; filename=generated_report.docx"},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9000)
