def fibonnacci(n):
    global nombreCalcul
    global memoire
    nombreCalcul += 1
    if n in memoire:
        return(memoire[n])

    if n == 0:
        return(0)
    elif n == 1:
        return(1)
    else:

        memoire[n] = fibonnacci(n-1) + fibonnacci(n-2)
        return(memoire[n])

nombreCalcul = 0
memoire = {}
y = 300
x = fibonnacci(y)

print(f"fibonnacci({y})={fibonnacci(y)}")
print(f"nombre de calcul = {nombreCalcul}")
