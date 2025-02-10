import datetime


def logger(path):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            result = old_function(*args, **kwargs)
            log_entry = (
                f"{datetime.datetime.now()} | "
                f"Функция: {old_function.__name__} | "
                f"Аргументы: {args}, {kwargs} | "
                f"Результат: {result}\n"
            )


            with open(path, "a", encoding="utf-8") as log_file:
                log_file.write(log_entry)

            return result

        return new_function

    return __logger