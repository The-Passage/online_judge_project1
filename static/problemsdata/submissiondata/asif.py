import re
phoneNumRegex = re.compile(r'\d\d\d-\d\d\d-\d\d\d\d')
print('enter your phone number: ')
s = str(input())
mo = phoneNumRegex.search(s)
if mo:
    print('Phone number found: ' + mo.group())
else:
    print('invalid')