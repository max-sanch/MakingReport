from pydantic import BaseModel, Field, ValidationError, parse_raw_as

from makingreport.services import api_handler
import config


class Todo(BaseModel):
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


class User(BaseModel):
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
    """
    Формируем и возвращаем структуру с данными для удобного использования
    """
    users = parse_json(User, api_handler.get_data(config.API_URL_USERS))
    todos = parse_json(Todo, api_handler.get_data(config.API_URL_TODOS))
    tasks_list_for_users = {}

    for todo in todos:
        if todo.user_id is not None and todo.id is not None and\
                todo.title is not None and todo.completed is not None:
            # Создаём список заданий определённого пользователя, если его нету
            if tasks_list_for_users.get(str(todo.user_id)) is None:
                tasks_list_for_users[str(todo.user_id)] = {
                    'completed_tasks': [],
                    'remaining_tasks': []
                }

            title = todo.title if len(todo.title) <= 48 else todo.title[:48] + '...'
            if todo.completed:
                tasks_list_for_users[str(todo.user_id)]['completed_tasks'].append(title)
            else:
                tasks_list_for_users[str(todo.user_id)]['remaining_tasks'].append(title)
    del todos

    for user in users:
        # Создаём список заданий определённого пользователя, если его нету
        if tasks_list_for_users.get(str(user.id)) is None:
            tasks_list_for_users[str(user.id)] = {
                    'completed_tasks': [],
                    'remaining_tasks': []
                }

        # Расширяем список данных пользователя в итоге получая структуру:
        # {'user_id': {
        #   'completed_tasks': list,
        #   'remaining_tasks': list,
        #   'username': str,
        #   'name': str,
        #   'email: str',
        #   'company_name: str
        #   }
        # }
        tasks_list_for_users[str(user.id)].update({
            'username': user.username,
            'name': user.name,
            'email': user.email,
            'company_name': user.company.name
        })
    del users
    return tasks_list_for_users
