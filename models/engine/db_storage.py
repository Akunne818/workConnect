
from models.base_models import Basemodels, Base

import models
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from os import getenv
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from dotenv import load_dotenv
from models.jobSeeker import JobSeeker as User
from models.employer import Employer
from models.job import Job


load_dotenv()

classes = {
    "User": User,
    "Employer": Employer,
    "Job": Job
}


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        WorkConnect_MYSQL_USER = getenv('WorkConnect_MYSQL_USER')
        WorkConnect_MYSQL_PWD = getenv('WorkConnect_MYSQL_PWD')
        WorkConnect_MYSQL_HOST = getenv('WorkConnect_MYSQL_HOST')
        WorkConnect_MYSQL_DB = getenv('WorkConnect_MYSQL_DB')
        WorkConnect_ENV = getenv('WorkConnect_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(WorkConnect_MYSQL_USER,
                                             WorkConnect_MYSQL_PWD,
                                             WorkConnect_MYSQL_HOST,
                                             WorkConnect_MYSQL_DB))
        if WorkConnect_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self.__engine)
            self.__session = DBSession()
        return self.__session

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        print('i am strorage called')
        self.__session.commit()

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def rollback(self):
        """ Roll back a session"""
        self.__session.rollback()

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if cls not in classes.values():
            return None

        all_cls = models.storage.all(cls)
        for value in all_cls.values():
            if value.id == id:
                return value

        return None

    def getjobs(self, cls, id):
        """ 
        Return job based on the id"""

        if cls not in classes.values():
            return None

        all_cls = models.storage.all(cls)
        for value in all_cls.values():
            if value.id == id:
                return value

        return None

    def count(self, cls=None):
        """
        count the number of objects in storage
        """
        if cls is None:
            count = 0
            for clas in classes.values():
                count += len(models.storage.all(clas).values())
        else:
            count = len(models.storage.all(cls).values())

        return count

    

    def add_user(self, email: str, hashed_password: str, username: str) -> User:
        """This is the add user method"""

        new_user = User(email=email, hashed_password=hashed_password,
                        username=username)
        print(new_user.id)
        self._session.add(new_user)
        self._session.flush()  # flush the changes to the database
        self._session.commit()
        self._session.refresh(new_user)  # refresh the user instance
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """This method takes in arbitrary keyword arguments and returns
        the first row found in the users table as filtered by the
        method’s input arguments"""
        try:
            # Construct the query dynamically based on kwargs
            query = self._session.query(User).filter_by(**kwargs)

        except InvalidRequestError:
            # If there is an invalid request error, raise it with a
            # meaningful message
            raise InvalidRequestError

        if query:
            # Get the first result or raise NoResultFound
            user_instance = query.one()

            return user_instance
        else:
            # If no results are found, raise NoResultFound
            raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """This is a method that takes as argument a required user_id
        integer and arbitrary keyword arguments, and returns None"""
        user = self.find_user_by(id=user_id)
        if kwargs:
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
                else:
                    raise ValueError(f"Invalid attribute: {key}")

        # Commit changes to the database
        self._session.commit()

    def delete_user(self, user_id: int) -> None:
        """This method deletes a user from the database"""
        user = self.find_user_by(id=user_id)
        self._session.delete(user)
        self._session.commit()

    def add_employer(self, email: str, hashed_password: str, first_name: str, last_name: str) -> Employer:
        """This is the add user method"""

        new_employer = Employer(email=email, hashed_password=hashed_password,
                        first_name=first_name, last_name=last_name)
        print(new_employer.id)
        self._session.add(new_employer)
        self._session.flush()  # flush the changes to the database
        self._session.commit()
        self._session.refresh(new_employer)  # refresh the user instance
        return new_employer

    def find_employer_by(self, **kwargs) -> User:
        """This method takes in arbitrary keyword arguments and returns
        the first row found in the users table as filtered by the
        method’s input arguments"""
        try:
            # Construct the query dynamically based on kwargs
            query = self._session.query(Employer).filter_by(**kwargs)

        except InvalidRequestError:
            # If there is an invalid request error, raise it with a
            # meaningful message
            raise InvalidRequestError

        if query:
            # Get the first result or raise NoResultFound
            user_instance = query.one()

            return user_instance
        else:
            # If no results are found, raise NoResultFound
            raise NoResultFound

    def update_employer(self, employer_id: int, **kwargs) -> None:
        """This is a method that takes as argument a required user_id
        integer and arbitrary keyword arguments, and returns None"""
        user = self.find_employer_by(id=employer_id)
        if kwargs:
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
                else:
                    raise ValueError(f"Invalid attribute: {key}")

        # Commit changes to the database
        self._session.commit()

    def delete_employer(self, employer_id: int) -> None:
        """This method deletes a user from the database"""
        employer = self.find_user_by(id=employer_id)
        self._session.delete(employer)
        self._session.commit()

    def add_job(self, title: str, description: str, employer_id: int, **kwargs) -> Job:
        """This is the add user method"""

        job = Job(title=title, description=description, employer_id=employer_id, **kwargs)
        print(job.id)
        self._session.add(job)
        self._session.flush()  # flush the changes to the database
        self._session.commit()
        self._session.refresh(job)  # refresh the user instance
        return job

    def find_job_by(self, **kwargs) -> Job:
        """This method takes in arbitrary keyword arguments and returns
        the first row found in the users table as filtered by the
        method’s input arguments"""
        try:
            # Construct the query dynamically based on kwargs
            query = self._session.query(Job).filter_by(**kwargs)

        except InvalidRequestError:
            # If there is an invalid request error, raise it with a
            # meaningful message
            raise InvalidRequestError

        if query:
            # Get the first result or raise NoResultFound
            user_instance = query.one()

            return user_instance
        else:
            # If no results are found, raise NoResultFound
            raise NoResultFound
        
     
    def delete_job(self, job_id: int) -> None:
        """This method deletes a user from the database"""
        job = self.find_user_by(id=job_id)
        self._session.delete(job)
        self._session.commit()