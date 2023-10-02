from typing import List
from fastapi import APIRouter, Depends, HTTPException, Header, Response, status
from sqlalchemy.orm import Session
from ..Schemas import schemas
from..Models import models
from ..database import get_db
from ..authenticate import get_authenticated_user

router = APIRouter(    
    tags=['assignments']
)





#creating Assignments with the authenticated user
@router.post('/assignments', response_model=schemas.AssignmentResponse)
def create_assignment(assignment: schemas.AssignmentCreate,username: str = Header(None), authenticated_user: models.User = Depends(get_authenticated_user),db: Session = Depends(get_db),  authorization: str = Header(None, description="Basic Authentication Header")):

    if not (1 <= assignment.points <= 10) or not (1 <= assignment.num_of_attempts <= 3):
        raise HTTPException(status_code=400, detail="Invalid input. Points should be between 1 and 10, and num_of_attempts should be between 1 and 3.")

    db_assignment = models.Assignment(**assignment.dict())
    db_assignment.owner_id=authenticated_user.id
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment


#getting assignment with specific id 
@router.get("/assignments/{id}", response_model=schemas.AssignmentResponse)
def get_assignment(id: str,authenticated_user: models.User = Depends(get_authenticated_user), db: Session = Depends(get_db), authorization: str = Header(None, description="Basic Authentication Header")):
    
    assignment = db.query(models.Assignment).filter(models.Assignment.id == id).first()

    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    return assignment


#getting  the assignments created by the  user
@router.get("/assignments", response_model=List[schemas.AssignmentResponse])
def get_assignments(authenticated_user: models.User = Depends(get_authenticated_user),db: Session = Depends(get_db), authorization: str = Header(None, description="Basic Authentication Header")):
   
    assignments = db.query(models.Assignment).filter(models.Assignment.owner_id == authenticated_user.id).all()

    return assignments


#delete the assignment based on id and only if the user is authenticated 
@router.delete("/assignments/{assignment_id}",status_code=status.HTTP_204_NO_CONTENT )
def delete_assignment(assignment_id: str,authenticated_user: models.User = Depends(get_authenticated_user), db: Session = Depends(get_db),authorization: str = Header(None, description="Basic Authentication Header")):
    
    assignment = db.query(models.Assignment).filter(models.Assignment.id == assignment_id).first()

    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    # Check if the authenticated user is the owner of the assignment
    if assignment.owner_id != authenticated_user.id:
        raise HTTPException(status_code=403, detail="Permission denied. You can only delete assignments you own.")

   
    db.delete(assignment)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


#updating the user based on the user authenticationn and providing the whole object 
@router.put("/assignments/{assignment_id}", response_model=schemas.AssignmentResponse, status_code=status.HTTP_200_OK)
def update_assignment(
    assignment_id: str,
    assignment_update: schemas.AssignmentCreate,
    authenticated_user: models.User = Depends(get_authenticated_user),
    db: Session = Depends(get_db)
):
    
     # Query the assignment by its ID
    assignment = db.query(models.Assignment).filter(models.Assignment.id == assignment_id).first()
   
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    # Check if the authenticated user is the owner of the assignment
    if assignment.owner_id != authenticated_user.id:
        raise HTTPException(status_code=403, detail="Permission denied. You can only update assignments you own.")

    # Update assignment details
    assignment.name = assignment_update.name
    assignment.points = assignment_update.points
    assignment.num_of_attempts = assignment_update.num_of_attempts
    assignment.deadline = assignment_update.deadline

    db.commit()

    return assignment

# @router.patch("/assignments/{assignment_id}", response_model=schemas.AssignmentResponse)
# def partial_update_assignment(
#     assignment_id: str,
#     assignment_patch: schemas.AssignmentCreate,
#     authenticated_user: models.User = Depends(get_authenticated_user),
#     db: Session = Depends(get_db)
# ):
  

#     # Query the assignment by its ID
#     assignment = db.query(models.Assignment).filter(models.Assignment.id == assignment_id).first()

#     if not assignment:
#         raise HTTPException(status_code=404, detail="Assignment not found")

#     # Check if the authenticated user is the owner of the assignment
#     if assignment.owner_id != authenticated_user.id:
#         raise HTTPException(status_code=403, detail="Permission denied. You can only update assignments you own.")

#     # Partially update assignment details based on the patch data
#     if assignment_patch.name is not None:
#         assignment.name = assignment_patch.name
#     if assignment_patch.points is not None:
#         assignment.points = assignment_patch.points
#     if assignment_patch.num_of_attempts is not None:
#         assignment.num_of_attempts = assignment_patch.num_of_attempts
#     if assignment_patch.deadline is not None:
#         assignment.deadline = assignment_patch.deadline

#     db.commit()

#     return assignment