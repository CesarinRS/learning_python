def contar_primos(number):
    primos = []
    for i in range(2, number + 1):
        es_primo = True
        for j in range(2, int(i ** 0.5) + 1):
            if i % j == 0:
                es_primo = False
                break

        if es_primo:
            primos.append(i)
    return primos
print(contar_primos(1000))