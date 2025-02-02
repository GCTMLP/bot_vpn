from abc import ABC, abstractmethod
from typing import Union

from database.connect import db_session


class AbstractRepository(ABC):
    @abstractmethod
    def add_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    def get_one(self, filters: dict):
        raise NotImplementedError

    @abstractmethod
    def delete_one(self, obj):
        raise NotImplementedError

    @abstractmethod
    def get_all(self, filters: dict = None):
        raise NotImplementedError

    @abstractmethod
    def update_one(self, obj, data: dict):
        raise NotImplementedError

    @abstractmethod
    def create_all(self, objects: list):
        raise NotImplementedError

    @abstractmethod
    def get_by_entry(self, field: str, values: Union[list, set]):
        raise NotImplementedError

    @abstractmethod
    def session_commit(self, obj):
        raise NotImplementedError

    @abstractmethod
    def bulk_delete(self, field: str, value: Union[list, set]):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def _filters(self, filters: dict) -> list:
        return [
            self.model.__table__.c[field] == value for field, value in filters.items()
        ]

    def add_one(self, data: dict):
        """
        Добавляет один объект в БД.
        :param data: Параметры для добавления {fild_name: value}.
        """
        with db_session() as session:
            obj = self.model(**data)
            session.add(obj)
            session.commit()
            session.refresh(obj)
            return obj

    def get_one(self, filters: dict):
        """
        Получает один объект из БД.
        :param filters: Фильтры, по которым необходимо получить объект.
        """
        with db_session() as session:
            query = session.query(self.model).filter(*self._filters(filters))
            return query.first()

    def delete_one(self, obj):
        """Удаление объекта из БД."""
        with db_session() as session:
            session.delete(obj)
            session.commit()

    def get_all(self, filters: dict = None):
        """
        Получает все объекты из БД.
        :param filters: Фильтры, можно задать, при необходимости.
        """
        with db_session() as session:
            query = session.query(self.model).order_by(self.model.crated_at.desc())
            if not filters:
                return query.all()
            query = query.filter(*self._filters(filters))
            return query.all()

    def update_one(self, obj, data: dict):
        """
        Обновляет объекта в БД.
        :param data: Новые данные.
        :param obj: Объект, который нужно обновить.
        """
        with db_session() as session:
            obj = session.merge(obj)
            for key, value in data.items():
                setattr(obj, key, value)
            session.add(obj)
            session.commit()
            session.refresh(obj)
            return obj

    def create_all(self, objects: list):
        """
        Массовое добавление объектов.
        :param objects: Список объектов
        """
        with db_session() as session:
            session.add_all(objects)
            session.commit()
            for obj in objects:
                session.refresh(obj)
            return objects

    def get_by_entry(self, field: str, values: Union[list, set]):
        """Получить данные по вхождению заданного поля в массив."""
        with db_session() as session:
            query = session.query(self.model).filter(
                getattr(self.model, field).in_(values)
            )
            return query.all()

    def session_commit(self, obj):
        with db_session() as session:
            session.add(obj)
            session.commit()
            session.refresh(obj)
            return obj

    def bulk_delete(self, field: str, values: Union[list, set]):
        """Удаление объектов по вхождению заданного поля."""
        with db_session() as session:
            session.query(self.model).filter(
                getattr(self.model, field).in_(values)
            ).delete()
            session.commit()

    def native_sql(self, raw):
        with db_session() as session:
            data = session.execute(raw)
            return data.scalars().all()
