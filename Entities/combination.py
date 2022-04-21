import math
class combination():

    def comb(self, num1, num2):
        answer = math.factorial(num1)/(math.factorial(num2) * math.factorial(num1-num2))
        print(str(answer))
        return int(answer)

