from fastapi import APIRouter, Depends, HTTPException
from database import events_collection
from models import Event
from bson import ObjectId
from typing import List

router = APIRouter()

# Convert MongoDB document to a dictionary with 'id' field
def serialize_event(event):
    return {
        "id": str(event["_id"]),  # Convert ObjectId to string
        "title": event["title"],
        "description": event.get("description", ""),
        "date": event["date"],
        "location": event["location"],
        "available_tickets": event["available_tickets"]
    }
    
    


# Create a new event : no need to pass id
@router.post("/events", response_model=Event)
async def create_event(event: Event):
    new_event = await events_collection.insert_one(event.dict())
    created_event = await events_collection.find_one({"_id": new_event.inserted_id})
    return serialize_event(created_event)

# Get all events
@router.get("/events")
async def get_events():
    events = await events_collection.find().to_list(100)
    return [serialize_event(event) for event in events]


# Get event by ID
@router.get("/events/{event_id}")
async def get_event(event_id: str):
    event = await events_collection.find_one({"_id": ObjectId(event_id)})
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return serialize_event(event)


# Update an event
@router.put("/events/{event_id}", response_model=Event)
async def update_event(event_id: str, event: Event):
    updated_event = await events_collection.find_one_and_update(
        {"_id": ObjectId(event_id)},
        {"$set": event.dict()},
        return_document=True
    )
    if not updated_event:
        raise HTTPException(status_code=404, detail="Event not found")
    return serialize_event(updated_event)

# Update available tickets for an event
@router.put("/events/{event_id}/update_tickets")
async def update_event_tickets(event_id: str, update_data: dict):
    # Find the event
    event = await events_collection.find_one({"_id": ObjectId(event_id)})

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Update available tickets
    result = await events_collection.update_one(
        {"_id": ObjectId(event_id)},
        {"$set": {"available_tickets": update_data["available_tickets"]}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to update available tickets")

    return {"message": "Available tickets updated"}

# Delete an event
@router.delete("/events/{event_id}")
async def delete_event(event_id: str):
    delete_result = await events_collection.delete_one({"_id": ObjectId(event_id)})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"message": "Event deleted successfully"}


# Update available tickets for an event
@router.put("/events/{event_id}/update_tickets")
def update_event_tickets(event_id: str, update_data: dict):
    # Find the event
    event = events_collection.find_one({"_id": ObjectId(event_id)})

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Update available tickets
    events_collection.update_one({"_id": ObjectId(event_id)}, {"$set": {"available_tickets": update_data["available_tickets"]}})

    return {"message": "Available tickets updated"}