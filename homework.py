import datetime as dt


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
        return self.limit - self.get_today_stats()

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

        currency_dict = {
            'rub': (1, 'руб'),
            'usd': (self.USD_RATE, 'USD'),
            'eur': (self.EURO_RATE, 'Euro')
        }

        currency_name = currency_dict[currency][1]

        cash_remained = round(
            self.get_rest_limit() / currency_dict[currency][0], 2
        )

        if cash_remained > 0:
            return ('На сегодня осталось '
                    f'{cash_remained} {currency_name}')
        elif cash_remained == 0:
            return 'Денег нет, держись'
        else:
            cash_remained = abs(cash_remained)
            return ('Денег нет, держись: твой долг - '
                    f'{cash_remained} {currency_name}')


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        if self.get_rest_limit() > 0:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    'но с общей калорийностью '
                    f'не более {self.get_rest_limit()} кКал')
        else:
            return 'Хватит есть!'


class Record:

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            date = dt.datetime.strptime(date, '%d.%m.%Y')

            self.date = date.date()

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
