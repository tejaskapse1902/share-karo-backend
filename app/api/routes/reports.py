from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from app.schemas.report import ReportCreateSchema
from app.db.mongodb import report_collection
from app.core.dependencies import get_current_user
from bson import ObjectId

router = APIRouter()

# ✅ CREATE REPORT
@router.post("/reports")
async def create_reports(
    data: ReportCreateSchema,
    user=Depends(get_current_user)
):
    report = {
        "title": data.title,
        "content": data.content,
        "created_by": user["sub"],  # email from JWT
        "created_at": datetime.utcnow()
    }

    await report_collection.insert_one(report)

    return {"message": "Report created successfully"}

# ✅ GET ALL REPORTS
@router.get("/reports")
async def get_reports(user=Depends(get_current_user)):
    reports = []
    cursor = report_collection.find({}, {"_id": 0})

    async for report in cursor:
        reports.append(report)

    return reports

# ✅ UPDATE REPORTS
@router.put("/reports/{report_id}")
async def update_report(
    report_id: str,
    data: ReportCreateSchema,
    user=Depends(get_current_user)
):
    update_data = {k: v for k, v in data.dict().items() if v is not None}

    result = await report_collection.update_one(
        {"_id": ObjectId(report_id)},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Report not found")

    return {"message": "Report updated successfully"}

# ✅ DELETE REPORT
@router.delete("/reports/{report_id}")
async def delete_report(
    report_id: str,
    user=Depends(get_current_user)
):
    result = await report_collection.delete_one(
        {"_id": ObjectId(report_id)}
    )

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Report not found")

    return {"message": "Report deleted successfully"}