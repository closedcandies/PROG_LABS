import requests
from xml.etree import ElementTree




class CurrencyRates:
    URL = "https://www.cbr.ru/scripts/XML_daily.asp"

    # CODES = {"USD": "R01235", "EUR": "R01239", "GBP": "R01035"}
    # CODES - словарь отслеживаемых валют
    {"USD": 82.45, }
    def __init__(self, char_codes=['USD', 'EUR', 'GBP']):
        self._rates = {}
        self._char_codes = None

        # сделать проверку на валидность значений
        if self._check_char_codes(char_codes):
            self._char_codes = char_codes
            # self._fetch_rates()
        else:
            raise ValueError('Some char code is not correct')

    @property
    def rates(self):
        return self._rates

    # дописать сеттеры и делитеры

    @property
    def char_codes(self):
        return self._char_codes

    def _check_char_codes(self, char_codes):
        response = requests.get(self.URL)
        if response.status_code == 200:
            tree = ElementTree.fromstring(response.content)
            # for _code in _char_codes:
            available_codes = []
            for _code in tree.findall('.//CharCode'):
                available_codes.append(_code.text)

            return all(list(map(lambda _code: _code in available_codes, char_codes)))

        else:
            raise ConnectionError("Не удалось получить данные с сайта ЦБ РФ")

    def _get_valute_ids(self):
        response = requests.get(self.URL)
        if response.status_code == 200:
            tree = ElementTree.fromstring(response.content)
            for _code in self._char_codes:
                pass
        # self._codes[_code] =

    def _fetch_rates(self):
        response = requests.get(self.URL)
        if response.status_code == 200:
            tree = ElementTree.fromstring(response.content)
            for code, val_id in self._codes.items():
                element = tree.find(f".//Valute[@ID='{val_id}']/Value")
                if element is not None:
                    self._rates[code] = float(element.text.replace(",", "."))
        else:
            raise ConnectionError("Не удалось получить данные с сайта ЦБ РФ")

    @property
    def rates(self):
        return self._rates

    # написать код для делитера свойства rates


# Пример использования
if __name__ == "__main__":
    c_r = CurrencyRates()

    print(c_r.rates)  # Вывод всех курсов
    # print("Курс USD:", c_r.rates.get("USD"))