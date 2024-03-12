from uuid import UUID

from sqlalchemy import Connection, Table, insert, select
from sqlalchemy.exc import IntegrityError

from src.core.exceptions import AlreadyExistsError, DoesNotExistError
from src.core.interfaces.repositories import BaseRepository
from src.core.models import ShortenedUrl
from src.infrastructure.database.tables.url import url_table


class UrlRepository(BaseRepository[UUID, ShortenedUrl]):
    def __init__(self, connection: Connection) -> None:
        self._conn = connection

    def get(self, pk: UUID) -> ShortenedUrl:
        stmt = select(self._table).where(self._table.c.short_url == pk).limit(1)
        result = self._conn.execute(stmt).first()
        if not result:
            raise DoesNotExistError(
                f"{self.__class__.__name__} could not find {self._model.__name__} with given PK - {pk}",
            )
        return ShortenedUrl.model_validate(result)

    def persist(self, model: ShortenedUrl) -> None:
        stmt = insert(self._table).values(**model.model_dump())
        try:
            self._conn.execute(stmt)
        except IntegrityError:
            raise AlreadyExistsError(
                f"{self.__class__.__name__} could not persist {model}: record with given PK already exists",
            )

    @property
    def _table(self) -> Table:
        return url_table
