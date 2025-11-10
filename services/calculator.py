from datetime import datetime


def calculate_day_number(birth_date_str: str) -> int:
    """
    birth_date_str: "дд.мм.гггг" (но для расчёта дня используем только дд.мм)
    Возвращает число от 1 до 9
    """
    # Сегодняшняя дата
    today = datetime.today()
    today_str = today.strftime("%d%m%Y")  # "01112025"

    # Дата рождения (только день и месяц)
    birth_day_month = birth_date_str.replace(".", "")[:4]  # "1602"

    # Собираем все цифры
    all_digits = birth_day_month + today_str  # "160201112025"

    # Суммируем
    total = sum(int(d) for d in all_digits if d.isdigit())

    # Сводим к однозначному
    while total > 9:
        total = sum(int(d) for d in str(total))

    return total


def reduce_number(num: int) -> int:
    """
    Сводит число к значению в диапазоне 1-22
    Специальная логика:
    - 10, 11, 22 остаются как есть (мастер-числа)
    - Остальные числа сводим до двузначного
    - Двузначные числа сводим только если они > 22
    """
    # Проверяем на мастер-числа
    if num in [10, 11, 22]:
        return num

    # Сводим до двузначного, если число > 22
    current = num
    while current > 22:
        current = sum(int(d) for d in str(current))
        # Проверяем получившееся число
        if current in [10, 11, 22]:
            return current

    return current


def calculate_personality(day: int) -> int:
    """
    Рассчитывает число личности (день рождения) по специальной логике:
    - Если день 1-22 - возвращаем как есть
    - Если день > 22 - складываем цифры, но сохраняем 10, 11, 22 как мастер-числа
    """
    if 1 <= day <= 22:
        return day

    # Для дней больше 22 складываем цифры
    return reduce_number(day)


def calculate_spirituality(month: int) -> int:
    """Рассчитывает число духовности (месяц рождения)"""
    return reduce_number(month)


def calculate_career(year: int) -> int:
    """Рассчитывает число карьеры (год рождения)"""
    year_sum = sum(int(d) for d in str(year))
    return reduce_number(year_sum)


def calculate_health(birth_date: str) -> int:
    """Рассчитывает число здоровья (сумма всех цифр даты)"""
    total = sum(int(d) for d in birth_date if d.isdigit())
    return reduce_number(total)