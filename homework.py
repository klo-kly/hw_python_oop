import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today = dt.datetime.now().date()
        today_stats = 0
        for i in self.records:
            if today == i.date:
                today_stats += i.amount
        return today_stats

    def show_records(self):
        s = ''
        for i in self.records:
            s += str(i)
            s += '\n'
        return s

    def get_week_stats(self):
        week = dt.timedelta(7)
        today = dt.datetime.now().date()
        week_stats = 0
        for i in self.records:
            date_in_record = i.date
            if (today >= date_in_record > today - week):
                week_stats += i.amount
        return week_stats


class CashCalculator(Calculator):
    USD_RATE = 77.39
    EURO_RATE = 92.14

    def get_today_cash_remained(self, currency):

        cash_remained = 0

        if currency == 'rub':
            cash_remained = self.get_today_stats()
            limit = self.limit
            currency = 'руб'
        elif currency == 'usd':
            cash_remained = self.get_today_stats() / self.USD_RATE
            limit = self.limit / self.USD_RATE
            currency = 'USD'
        elif currency == 'eur':
            cash_remained = self.get_today_stats() / self.EURO_RATE
            limit = self.limit / self.EURO_RATE
            currency = 'Euro'

        if self.limit > self.get_today_stats():
            rest_of_the_limit = round(limit - cash_remained, 2)
            return (f'На сегодня осталось {rest_of_the_limit} {currency}')
        elif self.limit == self.get_today_stats():
            return 'Денег нет, держись'
        else:
            rest_of_the_limit = round(cash_remained - limit, 2)
            return ('Денег нет, держись: твой долг - '
                    + f'{rest_of_the_limit} {currency}')


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        if self.limit > self.get_today_stats():
            rest_of_the_limit = self.limit - self.get_today_stats()
            return ('Сегодня можно съесть что-нибудь ещё, '
                    + 'но с общей калорийностью '
                    + f'не более {rest_of_the_limit} кКал')
        else:
            return 'Хватит есть!'


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        self.comment = comment
        self.date = dt.datetime.now().date()
        if date:
            date = dt.datetime.strptime(date, '%d.%m.%Y')
            date = dt.datetime.strftime(date, '%Y-%m-%d')
            date = dt.datetime.strptime(date, '%Y-%m-%d')
            self.date = date.date()

    def __str__(self):
        return f'{self.amount} | {self.comment} | {self.date}'


# создадим калькулятор денег с дневным лимитом 1000
cash_calculator = CashCalculator(1000)

# дата в параметрах не указана,
# так что по умолчанию к записи
# должна автоматически добавиться сегодняшняя дата
cash_calculator.add_record(Record(amount=145, comment='кофе'))
# и к этой записи тоже дата должна добавиться автоматически
cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
# а тут пользователь указал дату, сохраняем её
cash_calculator.add_record(Record(amount=3000,
                                  comment='бар в Танин др',
                                  date='01.11.2019'))

print(cash_calculator.get_today_cash_remained('rub'))
