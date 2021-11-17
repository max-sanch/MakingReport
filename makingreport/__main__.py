from makingreport.handlers import report_data


def main():
    report_data.get()


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        print('Exception:', err)
