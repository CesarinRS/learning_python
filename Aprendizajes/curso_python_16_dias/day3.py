"""
Text analyzer, this script request at the user a text (article, poem or any text) print 5 variables by parsing the text and analyzing it.
"""

text = input("Enter the text for analysis: ") # Pide al usuario ingresar un texto para su analisis
words_in_text = len(text.split()) # Cuenta cuantas palabras ingresó el usuario
first_letter = text[0] # Primer letra del texto ingresado por el usuario
last_letter = text[-1] # Ultima letra del texto ingresado por el usuario
reverse = text.split()[::-1] # Texto ingresado por el usuario al reves (solo el orden del palabras)
ask_python = "python" in text.lower() # Revisa si la palabra "python" esta en el texto (Ignora si es mayuscula o minuscula)

while True:
    param = input("Select 3 letters for the analysis: ") # Pide al usuario ingresar 3 letras como parametros para el analisis
    if len(param) == 3 and param.isalpha():
        break
    else:
        print("Please enter a valid parameter. (3 letters only)")
param = param.lower()
count1 = text.lower().count(param[0])
count2 = text.lower().count(param[1])
count3 = text.lower().count(param[2])

print(f'La letra "{param[0]}" esta {count1} veces en el texto')
print(f'La letra "{param[1]}" esta {count2} veces en el texto')
print(f'La letra "{param[2]}" esta {count3} veces en el texto')
print(f'La cantidad de palabras en el texto es "{words_in_text}"')
print(f'La primera letra en el texto es "{first_letter}" y la ultima "{last_letter}"')
print(f'El texto alreves es "{reverse}"')
if ask_python == True:
    print('La palabra "python" esta en el texto')
else: print('La palabra "python" no esta en el texto')

