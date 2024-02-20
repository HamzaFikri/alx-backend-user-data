#!/usr/bin/env python3

"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Returns User
        Adds a new user using email and hashed password,
        into the database
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        - Returns the first row found in the users table,
        as filtered by the method’s input arguments.
        - method takes in arbitrary keyword arguments, which
        is used for filtering
        """
        if not kwargs:
            raise InvalidRequestError

        fields = User.__table__.columns.keys()
        for key in kwargs.keys():
            if key not in fields:
                raise InvalidRequestError

        try:
            user = self._session.query(User).filter_by(**kwargs).first()
        except TypeError:
            raise InvalidRequestError

        if user is None:
            raise NoResultFound
        return user

    def update_user(self, user_id: str, **kwargs) -> None:
        """
        locate the user to update, then will update the user’s
        attributes as passed in the method’s arguments,
        then commit changes to the database.
        """
        user = self.find_user_by(id=user_id)
        fields = User.__table__.columns.keys()

        for key in kwargs.keys():
            if key not in fields:
                raise ValueError

        for key, value in kwargs.items():
            setattr(user, key, value)

        self._session.commit()
