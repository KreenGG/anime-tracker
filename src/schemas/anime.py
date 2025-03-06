from pydantic import BaseModel


class Anime(BaseModel):
    # TODO: добавить валидацию полей к примеру duration>0
    id: int
    name: str | None
    russian: str | None
    english: str | None
    japanese: str | None
    episodes: int | None
    episodes_aired: int | None
    duration: int | None
    poster: str | None  # Буду брать тупо jpeg
    # Жанры можно прикрутить позже
    description: str | None
    description_html: str | None
    description_source: str | None

    class Config:
        from_attributes = True
