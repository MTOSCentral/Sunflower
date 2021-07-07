# Sunflower Language Pack Reader.
from langcodes import *
langs='zh-Hans'
a=Language.get(langs).display_name(langs)
print(a)