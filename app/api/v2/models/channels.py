from __future__ import annotations

from . import BaseModel

class Channel(BaseModel):
    id: int
    name : str
    topic : str | None
    read_priv : int
    write_priv : int
    auto_join : int