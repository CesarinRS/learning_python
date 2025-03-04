"""
Random game, generate random number in the range 1-101, the user have 8 times to win, if not catch the number he lose.
"""
from random import randint

number_random = randint(1, 101)
lifes = 8
times = 1

user_name = input("Please enter your name: ")

# Impresión explicativa del juego
print(f"Welcome, {user_name} \n You have 8 times to win, the goal in this game is hit the random number. \n"
      f"The numbers range is 1-101. \nGood luck, gamer!")

# loop While para controlar el flujo del juego
while lifes > 0:
    try:
        select_number = int(input("Please select your number: "))
        # Condicionales para controlar los casos posibles en el juego (Numero erroneo, < que el numero, > que el numero o == que el numero)
        if select_number in range (1, 101):
            if select_number ==  number_random:
                print(f"You are a winner!\n You win in {times} times.")
                break
            elif select_number > number_random:
                times = times + 1
                lifes -= 1
                print(f"The selected number is higher, please try again!  \nYou have {lifes} life left")

            elif select_number < number_random:
                times = times + 1
                lifes -= 1
                print(f"The selected number is lower, please try again!  \nYou have {lifes} life left")

        else:
            print(f"Your choice isn't valid")

    except ValueError:
        print("⚠️ Please enter a valid number.")

if lifes == 0:
    print(f"Game over! The correct number was {number_random}.")