import os
from datetime import datetime, timezone, timedelta

import config


def get_text_report(user_data, time):
	"""
	Формируем отчёт в текстовый вид
	"""
	return f"""Отчёт для {user_data['company_name']}.
{user_data['name']} <{user_data['email']}> {time}
Всего задач: {len(user_data['completed_tasks']) + len(user_data['remaining_tasks'])}

Завершённые задачи ({len(user_data['completed_tasks'])}):
%s

Оставшиеся задачи ({len(user_data['remaining_tasks'])}):
%s""" % ('\n'.join(user_data['completed_tasks']), '\n'.join(user_data['remaining_tasks']))


def read_file(user_data, context):
	try:
		file = open(f"tasks/{user_data['username']}.txt", context)
	except OSError as err:
		raise Exception('Проблемы с чтением файла:\n %s' % err)
	return file


def get_time_from_text(text):
	"""
	Получаем дату создания файла из его содержимого
	"""
	time = ' '.join(text.split('\n')[1].split()[-2:])
	dt = datetime.strptime(time, config.FILE_FORMAT)
	dt = dt.strftime(config.FILE_NAME_FORMAT)
	return dt


def rename_old_file(user_data):
	"""
	Переименовываем старые файлы указывая дату их создания
	"""
	file = read_file(user_data, 'r')
	time = get_time_from_text(file.read())
	file.close()
	os.rename(f"tasks/{user_data['username']}.txt", f"tasks/old_{user_data['username']}_{time}.txt")


def write_to_file(text, user_data):
	file = read_file(user_data, 'w')
	with file:
		file.write(text)
	file.close()


def start(users_data):
	"""
	Формируем отчёты в текстовом виде и сохраняем их в файлы
	"""
	if not os.path.exists('tasks'):
		os.mkdir('tasks')

	for user_data in users_data.values():
		tz = timezone(timedelta(hours=+3.0))  # (UTC+03:00)
		time = datetime.now(tz)
		text = get_text_report(user_data, time.strftime(config.FILE_FORMAT))

		if os.path.exists(f"tasks/{user_data['username']}.txt"):
			rename_old_file(user_data)
		write_to_file(text, user_data)
