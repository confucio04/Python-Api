from fastapi import APIRouter, HTTPException
from sqlmodel import select
from database import SessionDep
from models.estudiante import EstudianteModelo

router = APIRouter(prefix="/estudiantes", tags=["Estudiantes"])


@router.get("/estudiantes", )
def obtener_estudiantes(
    estudiante: EstudianteModelo, session: SessionDep,
    ) -> EstudianteModelo:
    estudiante = session.exec(select(EstudianteModelo)).all()
    session.add(estudiante)
    session.commit()
    session.refresh(estudiante)
    return estudiante

@router.get("/{id}")
def obtener_estudiantes(
    id: int,
    session: SessionDep):
    estudiantes = session.get(EstudianteModelo, id)
    if not estudiantes:
        raise HTTPException(status_code=404, detail="No encontrado")
    return estudiantes
    
    