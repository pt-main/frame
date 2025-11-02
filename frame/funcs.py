def str_to_int(string: str, summing: bool = True) -> list | int:
    '''
# String to integrear method
Convert any value to int (list or number).
### Args:
- {string}: str - any string for convertation.
- {summing}: bool - function will return sum of list[indexes] if true, else list[indexes]
### Example:
Code:
```
print(str_to_int('test'))
print(str_to_int('test', summing = False))
```
Output:
```
169
[41, 39, 48, 41]
```
'''
    string = str(string)
    alphabet = list('1234567890 ' +
                    'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm' +
                    'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЁЯЧСМИТЬБЮйцукенгшщзхъфывапролджэёячсмитьбю' +
                    '!@#$%^&*()_+¡™£¢∞§¶•ªº–≠[]{}\\|/?.,<>\'":;±§`~\n\t')
    res = []
    for i in list(string):
        if i in alphabet: res.append(alphabet.index(i))
        else: 
            alphabet.append(i)
            res.append(alphabet.index(i))
    return sum(res) if summing else res
