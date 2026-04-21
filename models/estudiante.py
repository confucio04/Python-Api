from sqlmodel import Field, SQLModel


class EstudianteModelo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length= 30)