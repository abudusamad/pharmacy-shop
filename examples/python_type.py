from typing import List

def get_full_name(first_name:str, last_name:str):
    full_name = first_name.title() + " " + last_name.upper()
    return full_name
print(get_full_name("richard ", "fordjour"))

def get_name_with_age(name:str, age:int):
    name_with_age = name + "is this old " + age
    return name_with_age

def process_item(items:list[str]):
    for item in items:
        print(item)  
        
def process_item(items:List[str]):
    for item in items:
        print(item)