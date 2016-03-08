from cities_light.models import Country
import phonenumbers

def validate_phone(my_country, my_phone):
	try:
		entry = Country.objects.get(name__iexact=my_country)
		country_code = entry.code2
	except:
		print ('No matching country in database')
		return "missing"
	print (country_code)
	parsed_number = phonenumbers.parse( my_phone, country_code)
	return (phonenumbers.is_valid_number(parsed_number) and phonenumbers.is_possible_number(parsed_number))
	
