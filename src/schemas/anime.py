from pydantic import BaseModel


class Anime(BaseModel):
    id: int
    name: str
    russian: str
    english: str
    japanese: str
    episodes: int
    episodes_aired: int
    duration: int
    poster: str # Буду брать тупо jpeg
    # Жанры можно прикрутить позже
    description: str
    description_html: str
    description_source: str
