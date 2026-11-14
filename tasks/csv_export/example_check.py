from solution import export_rows
assert export_rows([{'name': 'A,B', 'age': 3}], ['name', 'age']) == 'name,age\n"A,B",3\n'
print('Example passed')
