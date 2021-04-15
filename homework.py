import datetime as dt

import date_converter


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today = dt.date.today()
        return sum([i.amount for i in self.records if today == i.date])

    def get_rest_limit(self):
        today = dt.date.today()
        return (
            self.limit
            - sum([i.amount for i in self.records if today == i.date])
        )

    def show_records(self):
        s = ''
        for i in self.records:
            s += str(i)
            s += '\n'
        return s

    def get_week_stats(self):
        week = dt.timedelta(7)
        today = dt.date.today()
        return sum(
            [i.amount for i in self.records if today >= i.date > today - week]
        )


class CashCalculator(Calculator):
    USD_RATE = 77.39
    EURO_RATE = 92.14

    def get_today_cash_remained(self, currency):

        cash_remained = 0

        currency_dict = {
            'rub': (1, 'руб'),
            'usd': (self.USD_RATE, 'USD'),
            'eur': (self.EURO_RATE, 'Euro')
        }

        cash_remained = round(
            self.get_rest_limit() / currency_dict[currency][0], 2
        )

        if self.limit > self.get_today_stats():
            return ('На сегодня осталось '
                    f'{cash_remained} {currency_dict[currency][1]}')
        elif self.limit == self.get_today_stats():
            return 'Денег нет, держись'
        else:
            return ('Денег нет, держись: твой долг - '
                    f'{- cash_remained} {currency_dict[currency][1]}')


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        if self.limit > self.get_today_stats():
            return ('Сегодня можно съесть что-нибудь ещё, '
                    'но с общей калорийностью '
                    f'не более {self.get_rest_limit()} кКал')
        else:
            return 'Хватит есть!'


class Record:

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        self.date = dt.date.today()
        if date:
            date = date_converter.string_to_date(date, '%d.%m.%Y')

            self.date = date

    def __str__(self):
        return f'{self.amount} | {self.comment} | {self.date}'


if __name__ == '__main__':
    # создадим калькулятор денег с дневным лимитом 1000
    cash_calculator = CashCalculator(1000)

    # дата в параметрах не указана,
    # так что по умолчанию к записи
    # должна автоматически добавиться сегодняшняя дата
    cash_calculator.add_record(Record(amount=145, comment='кофе'))
    # и к этой записи тоже дата должна добавиться автоматически
    cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
    # а тут пользователь указал дату, сохраняем её
    cash_calculator.add_record(Record(amount=1300, comment='бар в Танин др'))

    print(cash_calculator.get_today_cash_remained('rub'))
