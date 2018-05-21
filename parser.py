import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as mat_pyplot
import json
import urllib.request
import matplotlib.dates
import datetime


class ConvertArgumentTypes(object):
    """
    Переводим аргументы args функции f 
    в специализированные типы для удобной
    работы.
    """
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, f):
        def func(*args, **kwargs):
            zip_args = [x[0](x[1]) for x in zip(self.args, args)]
            invalid_kwargs = [x for x in kwargs if x not in self.kwargs]
            if len(invalid_kwargs) > 0:
                raise TypeError(f.func_name + "() got an unexpected keyword argument '%s'" % invalid_kwargs[0])
            kwargs = dict([(x, self.kwargs[x](kwargs[x])) for x in kwargs])
            v = f(*zip_args, **kwargs)
            return v
        return func


@ConvertArgumentTypes(str, str)
def crate(crypt_codes='USD', crypt_to='RUB'):
    """
    :param crypt_codes: Крипт, который надо перевести
    :param crypt_to=USD: Крипт, в который надо перевести 
    :return: текущее значение crypt в эквивалентах crypt_to
    """
    response = json.loads(
        urllib.request.urlopen(
            'https://min-api.cryptocompare.com/data/price?fsym=' +
            crypt_codes + '&tsyms=' + crypt_to).read().decode('utf-8'))
    return json.dumps(response)


@ConvertArgumentTypes(str, int, int, str, str)
def history(crypt_codes: str, begin_time: int, end_time: int, resolution: str, crypt_to: str):
    """
    С помощью специальных библиотек парсит информацию с указанной ссылки, и 
    по следующим аргументам выводит историю изменения курса:
    :param crypt_codes: Крипт, который надо перевести
    :param begin_time: Время,начиная с которого надо просчитать историю изменения курса
    :param end_time: Время,до с которого надо просчитать историю изменения курса
    :param resolution: Шаг разделения временного промежутка (день и т.п.)
    :param crypt_to=USD: Крипт, в который надо перевести 
    :return: текущее значение crypt в эквивалентах crypt_to
"""
    api_res = {'minute': 1, 'hour': 60, 'day': 1440}
    limit = (end_time - begin_time) // (api_res[resolution] * 60)
    request = 'https://min-api.cryptocompare.com/data/histo' + resolution + '?fsym=' + crypt_codes + '&tsym=' + crypt_to + '&limit=' + str(
        limit) + '&toTs=' + str(end_time)
    response = json.loads(urllib.request.urlopen(request).read().decode('utf-8'))
    if(bool(response) is False):
        bot.send_message(chat_id=update.message.chat_id, text='Вводить надо в правильные крипты :)')
    dates = matplotlib.dates.date2num(list(map(lambda x: datetime.datetime.fromtimestamp(x['time']), response['Data'])))
    values = list(map(lambda x: x['close'], response['Data']))
    mat_pyplot.scatter(dates, values)
    mat_pyplot.plot_date(dates, values, '-o')
    mat_pyplot.gcf().autofmt_xdate()
    mat_pyplot.title(crypt_codes + ' currency')
    mat_pyplot.xlabel('Date')
    mat_pyplot.ylabel(crypt_codes + ' to ' + crypt_to)
    mat_pyplot.savefig('tmp_fig.png')
    mat_pyplot.close()

        
