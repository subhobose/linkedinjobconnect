# print("hello")

testString = b'Subhrangsu Bose'
print(type(""))
print(type(repr(testString)[2:-1]))
comp = "AMD"
name = "Bose"

textMessage = "Hi {},\n\
I am a MSCS student at UT Dallas and I am currently on the hunt for a Fall 2023 internship.\n\
{} is one of the companies I have closely followed for a long time. Would you be willing to connect with me for an informational interview for 15 mins at your convenience?\n\
Thanks!".format(name, comp)

print(textMessage)