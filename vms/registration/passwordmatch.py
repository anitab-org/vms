# account can only be created if both passwords match
def match_password(password1, password2):
    if password1 != password2:
        return False
    else:
        return True
