import re
print(re.findall(r'c.t', 'cat cut c9t ctt apple cant'))

print(re.findall(r'ab*', 'a ab abb abbb abc'))

print(re.findall(r'ab+', 'a ab abb abbb abc'))

print(re.findall(r'colou?r', 'color colour colouur'))

print(re.findall(r'a{3}', 'aa aaa aaaa aaaaa'))

print(re.findall(r'a{2,4}', 'a aa aaa aaaa aaaaa'))

print(re.findall(r'^Hello', 'Hello world\nWorld Hello'))

print(re.findall(r'world$', 'Hello world\nHello world'))

print(re.findall(r'[aeiou]', 'hello world'))

print(re.findall(r'[^aeiou]', 'hello world'))

print(re.findall(r'\d+', 'abc123xyz'))

print(re.findall(r'\D+', 'abc123'))

print(re.findall(r'\s+', 'Hello  world'))

print(re.findall(r'\S+', 'Hello World'))

print(re.findall(r'\w+', 'Hello world_123'))

print(re.findall(r'\W+', 'Hello, world!'))

print(re.findall(r'hello', 'Hello, world', re.IGNORECASE))

print(re.findall(r'^Hello', 'Hello world\nHello again', re.MULTILINE))

print(re.findall(r'a.b', 'a\nb', re.DOTALL))

print(re.match(r'Hello', 'Hello world'))

print(re.fullmatch(r'Hello world', 'Hello world'))

print(re.sub(r'dog', 'cat', 'The dog is barking.'))

print(re.split(r', ', 'apple, banana, cherry'))

print(re.findall(r'\d+', 'There are 3 are and 5 bananas.'))