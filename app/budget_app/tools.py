import math
import random

tools = {
    'version': '0.1',
    'dollarRound': lambda num: round(num*100)/100,
    'percentRound': lambda num: round(num*10000)/100,
    'currencyPrint': lambda currency, num: str(currency)+" "+str(round(num*100)/100),
    # Same as Python's randInt
    'randomNumber': lambda min, max: math.ceil(random.random() * (max-min)+min),
    # 'twoParameterDoubleCallback': lambda callbackA, callbackB, ObjectA, ObjectB: callbackA(ObjectA, ObjectB),
    # 'called': lambda **kwargs: caller(**kwargs),
}
