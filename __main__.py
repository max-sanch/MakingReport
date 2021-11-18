from makingreport.handlers import report_data, report_data_to_file


def main():
	users_data = report_data.get()
	report_data_to_file.start(users_data)


if __name__ == "__main__":
	try:
		main()
	except Exception as err:
		print('Exception:', err)
	else:
		print('Completed successfully!')
