import requests
from bs4 import BeautifulSoup
from babel.numbers import format_currency

# run in your terminal "pip install -r requirements.txt"

country_list = []

url = "https://www.iban.com/currency-codes"
user_agent = {"User-Agent": "Mozilla/5.0"}
url_wise = "https://wise.com/gb/currency-converter/"


def coin_trader_request(url):
    try:
        request = requests.get(url)
        request_text = request.text
        soup = BeautifulSoup(request_text, 'html.parser')
        countries = soup.find("tbody").find_all("tr")
        for country in countries:
            result_country = country.find_all("td")
            country_dict = {
                "country": result_country[0].get_text(),
                "code": result_country[2].get_text(),
            }
            if country_dict["code"] == '':
                continue
            else:
                country_list.append(country_dict)
    except:
        print("An error has occurred")


def coverting_coin(origin_country, destination_country, value_to_convert):
    try:
        request = requests.get(
            f"{url_wise}{origin_country}-to-{destination_country}-rate?amount={value_to_convert}", headers=user_agent)
        request_text = request.text
        soup = BeautifulSoup(request_text, 'html.parser')
        result = soup.find(
            "h3", class_="cc__source-to-target").find_all("span", class_="text-success")
        for texto in result:
            converting_value = float(texto.string)
            return converting_value

    except:
        print("--------------------------------------------------------------")
        print("\nAn error has occurred")


def menu_choice_coin_trader():
    while True:
        try:
            choice = int(input("\nChoose the country number: "))
            if choice not in range(len(country_list)):
                print("--------------------------------------------------------------")
                print("Does not exist. Choose one of the options from the list.")

            else:
                print("--------------------------------------------------------------")
                print(f"\n(x): {country_list[choice]['country']}")
                print(f"Currency code: {country_list[choice]['code']}\n")
                print("--------------------------------------------------------------")

                choice_input = f"{country_list[choice]['code'].lower()}"
                return choice_input
        except ValueError:
            print("--------------------------------------------------------------")
            print("this is not a number.")


if __name__ == "__main__":
    print("<<<<<<<Welcome to Coin Trader>>>>>>>\n<<<<<<<Below is a list of countries>>>>>>>")
    print("<<<<<<<Choose by number, two countries you want to verify the currency>>>>>>>\n")
    coin_trader_request(url)

    for number in range(len(country_list)):
        print(f"[{number}]-->{country_list[number]['country']}")
    try:
        origin_country = menu_choice_coin_trader()

        print("Do you want to trade with which country?")
        destination_country = menu_choice_coin_trader()
        try:
            value_to_convert = float(input(
                f"How many {origin_country.lower()} do you want to convert to {destination_country.lower()}: "))
            converting = coverting_coin(
                origin_country, destination_country, value_to_convert)
            result_coverting = converting * float(value_to_convert)
            amout = result_coverting
            currency = destination_country.upper()
            print("--------------------------------------------------------------")
            print(
                f"\nThe converted value is: {format_currency(amout, currency)}")
            print("--------------------------------------------------------------")
            print("\n THANKS FOR USING :)")
        except:
            print("--------------------------------------------------------------")
            print("Type only numbers!!")

    except:
        print("--------------------------------------------------------------")
        print("\nUnable to convert currency")
        print("This currency is probably not registered on the site")
