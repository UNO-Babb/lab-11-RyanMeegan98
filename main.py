#GroceryStoreSim.py
#Name: Ryan Meegan
#Date: Apr 27 2025
#Assignment: Lab 11

import simpy
import random
eventLog = []
waitingShoppers = []
idleTime = 0

def shopper(env, id):
    arrive = env.now
    items = random.randint(10, 50)
    shoppingTime = int(items * 0.75)
    yield env.timeout(shoppingTime)
    waitingShoppers.append((id, items, arrive, env.now))

def checker(env):
    global idleTime
    while True:
        while len(waitingShoppers) == 0:
            idleTime += 1
            yield env.timeout(1)

        customer = waitingShoppers.pop(0)
        items = customer[1]
        checkoutTime = items // 8 + 1
        yield env.timeout(checkoutTime)

        eventLog.append((customer[0], customer[1], customer[2], customer[3], env.now))    

def customerArrival(env):
    customerNumber = 0
    while True:
        customerNumber += 1
        env.process(shopper(env, customerNumber))
        yield env.timeout(random.uniform(1, 2)) 

def processResults():
    totalWait = 0
    totalShoppers = 0
    totalItems = 0

    for e in eventLog:
        waitTime = e[4] - e[3]  # depart time - done shopping
        totalWait += waitTime
        totalItems += e[1]
        totalShoppers += 1

    avgWait = totalWait / totalShoppers
    avgItems = totalItems / totalShoppers

    print("------ Simulation Results ------")
    print("Total shoppers served:", totalShoppers)
    print("Average wait time: %.2f minutes" % avgWait)
    print("Average number of items bought: %.2f" % avgItems)
    print("Total idle time:", idleTime, "minutes")
    print("Shoppers still waiting at end of simulation:", len(waitingShoppers))

def main():
    numberCheckers = 5

    env = simpy.Environment()

    env.process(customerArrival(env))
    for i in range(numberCheckers):
        env.process(checker(env))

    env.run(until=240 )
    print(len(waitingShoppers))
    processResults()

if __name__ == '__main__':
    main()