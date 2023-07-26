# print("hello")

testString = b'Subhrangsu Bose'
print(type(""))
print(type(repr(testString)[2:-1]))

textMessage = "Hi Bose,\n\
I am a MSCS student at UT Dallas and I am currently on the hunt for a Fall 2023 internship.\n\
AMD is one of the companies I have closely followed for a long time. Would you be willing to connect with me for an informational interview for 15 mins at your convenience?\n\
Thanks!"

print(textMessage.split('\n')[0])

#extract company from above text
# criterias - starts with it in a new line(before = \n), followed by 'is one of the companies'(after = is)