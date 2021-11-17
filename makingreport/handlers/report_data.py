from pydantic import BaseModel, Field, ValidationError, parse_raw_as

from makingreport.services import api_handler


class Todos(BaseModel):
    user_id: int = Field(alias='userId', default=None)
    id: int = None
    title: str = None
    completed: bool = None


class Geo(BaseModel):
    lat: str = None
    lng: str = None


class Address(BaseModel):
    street: str = None
    suite: str = None
    city: str = None
    zipcode: str = None
    geo: Geo = None


class Company(BaseModel):
    name: str
    catch_phrase: str = Field(alias='catchPhrase', default=None)
    bs: str = None


class Users(BaseModel):
    id: int
    name: str
    username: str
    email: str
    address: Address = None
    phone: str = None
    website: str = None
    company: Company


def parse_json(obj, data):
    """
    Парсим и валидируем данные из json формата
    """
    try:
        parse_data = parse_raw_as(list[obj], data)
    except ValidationError as err:
        raise Exception('В json файле введены некорректные данные:\n %s' % err.json())
    return parse_data


def get():
    users = parse_json(Users, api_handler.get_data('https://json.medrating.org/users'))
    todos = parse_json(Todos, api_handler.get_data('https://json.medrating.org/todos'))
