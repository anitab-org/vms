# third party
import phonenumbers


def validate_phone(my_country, my_phone):
    try:
        country_code = my_country.code2
    except Exception:
        print('No matching country in database')
        return "missing"
    print(country_code)
    parsed_number = phonenumbers.parse(my_phone, country_code)
    return (phonenumbers.is_valid_number(parsed_number) and
            phonenumbers.is_possible_number(parsed_number))
