from sqlmodel import SQLModel


class SystemStatus(SQLModel):
    version: str
