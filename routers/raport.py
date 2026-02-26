from fastapi import Response, Depends, APIRouter
from fpdf import FPDF
import io

import storage
from utils.auth_utils import get_current_user

router = APIRouter(
    prefix="/raport",
    tags=["raport"],
)

@router.get("/generate")
async def generate_tasks_pdf(current_user = Depends(get_current_user)):
    user_tasks = [task for task in storage.tasks_list if task.user_id == current_user.id]

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial','B',15)

    pdf.cell(0,10, f'User: {current_user.username} task list', ln=True, align='C')
    pdf.ln(10)

    pdf.set_font('Arial','B',12)
    for task in user_tasks:
        status = "Done" if task.is_done else "Not Done/In Progress"
        is_finish = task.finished_at if task.is_done else "---"
        text = f"Task: {task.title} | ID: {task.id} | Status: {status} | Started_at: {task.started_at} | Finished_at: {is_finish}"
        pdf.multi_cell(0,10, text, ln=True, align='C', border=1)
        pdf.ln(2)

    pdf_output = pdf.output()

    return Response(
        content=bytes(pdf_output),
        media_type='application/pdf',
        headers={"Content-Disposition": f"attachment; filename=tasks_{current_user.id}.pdf"},
    )