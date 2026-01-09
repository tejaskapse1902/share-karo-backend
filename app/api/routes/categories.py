from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from app.schemas.category import CategoryCreateSchema, CategoryUpdateSchema
from app.db.mongodb import category_collection
from app.core.dependencies import get_current_user
from bson import ObjectId

router = APIRouter()

# ✅ CREATE CATEGORY
@router.post("/categories")
async def create_category(
    data: CategoryCreateSchema,
    user=Depends(get_current_user)
):
    category = {
        "role": data.role,
        "categories": data.categories,
        "product": data.product,
        "popular": data.popular,
        "category_id": data.category_id,
        "created_by": user["sub"],  # email from JWT
        "created_at": datetime.utcnow()
    }

    await category_collection.insert_one(category)

    return {"message": "Category created successfully"}

# ✅ GET ALL CATEGORIES
@router.get("/categories")
async def get_categories(user=Depends(get_current_user)):
    categories = []
    cursor = category_collection.find({}, {"_id": 0})

    async for category in cursor:
        categories.append(category)

    return categories

# ✅ UPDATE CATEGORY
@router.put("/categories/{category_id}")
async def update_category(
    category_id: str,
    data: CategoryUpdateSchema,
    user=Depends(get_current_user)
):
    update_data = {k: v for k, v in data.dict().items() if v is not None}

    result = await category_collection.update_one(
        {"category_id": category_id},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Category not found")

    return {"message": "Category updated successfully"}

# ✅ DELETE CATEGORY
@router.delete("/categories/{category_id}")
async def delete_category(
    category_id: str,
    user=Depends(get_current_user)
):
    result = await category_collection.delete_one(
        {"category_id": category_id}
    )

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Category not found")

    return {"message": "Category deleted successfully"}
