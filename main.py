from numpy import random
from prettytable import PrettyTable
import matplotlib.pyplot as plt


# generate random number in given distribution for IAT for Ordinary Customer
def generate_IAT_O():
    r = random.random()
    if r <= 0.09:
        return 0
    if r <= 0.26:
        return 1
    if r <= 0.53:
        return 2
    if r <= 0.73:
        return 3
    if r <= 0.88:
        return 4
    else:
        return 5


# generate random number in given distribution for IAT for Distinguished Customer
def generate_IAT_D():
    r = random.random()
    if r <= 0.1:
        return 1
    if r <= 0.3:
        return 2
    if r <= 0.6:
        return 3
    else:
        return 4


# generate random number in given distribution for ST for Ordinary Customer
def generate_ST_O():
    s = random.random()
    if s <= 0.20:
        return 1
    if s <= 0.60:
        return 2
    if s <= 0.88:
        return 3
    else:
        return 4


# generate random number in given distribution for ST for Distinguished Customer
def generate_ST_D():
    s = random.random()
    if s <= 0.10:
        return 1
    if s <= 0.4:
        return 2
    if s <= 0.78:
        return 3
    else:
        return 4


def one_teller(C1):
    # List for random variable in calendar
    ordinary_IAT = list()
    ordinary_AT = list()
    ordinary_ST = list()
    distinguished_IAT = list()
    distinguished_AT = list()
    distinguished_ST = list()

    # generate(Random Variables) in Calendar
    for i in range(C1):
        # Inter Arrival Time For Ordinary
        ordinary_IAT.append(generate_IAT_O())
        # Arrival Time For Ordinary
        if i != 0:
            ordinary_AT.append(ordinary_AT[i - 1] + ordinary_IAT[i])
        else:
            ordinary_AT.append(ordinary_IAT[0])
        # Service Time For Ordinary
        ordinary_ST.append(generate_ST_O())

        # Inter Arrival Time For Distinguished
        distinguished_IAT.append(generate_IAT_D())
        # Arrival Time For Distinguished
        if i != 0:
            distinguished_AT.append(distinguished_AT[i - 1] + distinguished_IAT[i])
        else:
            distinguished_AT.append(distinguished_IAT[0])
        # Service Time For Distinguished
        distinguished_ST.append(generate_ST_D())

    Type = list()  # Type for each entered Customer
    IAT = list()  # inter arrive time for System
    AT = list()  # arrive time for System
    ST = list()  # Service time for System
    SST = list()  # Service Start time for System
    WT = list()  # witting time for System
    idle = list()  # Idle time for System
    TimeInSystem = list()  # list contain witting In System for each Customer
    end_time = list()  # list contain end time for each service
    WT_O = list()  # witting time for ordinary Customers
    WT_D = list()  # witting time for ordinary Distinguished

    ordinary_iterator = 0  # iterator iterate in ordinary lists
    distinguished_iterator = 0  # iterator iterate in Distinguished lists
    probability_ordinary = 0  # use to count probability of wait for ordinary Customers
    probability_distinguished = 0  # use to count probability of wait for Distinguished Customers
    for i in range(C1):
        if i == 0:
            # for first customer entered fo bank we take the one with minimum arrival time
            if distinguished_AT[distinguished_iterator] <= ordinary_AT[ordinary_iterator]:
                IAT.append(distinguished_IAT[distinguished_iterator])
                AT.append(distinguished_AT[distinguished_iterator])
                ST.append(distinguished_ST[distinguished_iterator])
                SST.append(distinguished_AT[distinguished_iterator])
                distinguished_iterator += 1
                WT_D.append(0)
                Type.append('D')
            else:
                IAT.append(ordinary_IAT[ordinary_iterator])
                AT.append(ordinary_AT[ordinary_iterator])
                ST.append(ordinary_ST[ordinary_iterator])
                SST.append(ordinary_AT[ordinary_iterator])
                ordinary_iterator += 1
                WT_O.append(0)
                Type.append('O')
            WT.append(0)
            end_time.append(SST[i] + ST[i])
            TimeInSystem.append(ST[i])
            idle.append(IAT[i])
        else:
            # after serve the first customer priority will be for distinguished customer
            # if the end time for provisos serve less than or equal the arrival time for next distinguished customer
            # Or he come before the next ordinary customer or in same moment he will serve first
            if end_time[i - 1] >= distinguished_AT[distinguished_iterator] or distinguished_AT[
                distinguished_iterator] \
                    <= ordinary_AT[ordinary_iterator]:
                IAT.append(distinguished_IAT[distinguished_iterator])
                AT.append(distinguished_AT[distinguished_iterator])
                ST.append(distinguished_ST[distinguished_iterator])
                SST.append(max(end_time[i - 1], distinguished_AT[distinguished_iterator]))
                WT.append(max(0, end_time[i - 1] - distinguished_AT[distinguished_iterator]))
                end_time.append(SST[i] + ST[i])
                TimeInSystem.append(end_time[i] - distinguished_AT[distinguished_iterator])
                if WT[i] > 0:
                    probability_distinguished += 1
                WT_D.append(WT[i])
                distinguished_iterator += 1
                Type.append('D')

            else:
                # if the arrival time for the next ordinary customer less than the arrival time for next distinguished
                # ordinary customer will serve first
                IAT.append(ordinary_IAT[ordinary_iterator])
                AT.append(ordinary_AT[ordinary_iterator])
                ST.append(ordinary_ST[ordinary_iterator])
                SST.append(max(end_time[i - 1], ordinary_AT[ordinary_iterator]))
                WT.append(max(0, end_time[i - 1] - ordinary_AT[ordinary_iterator]))
                end_time.append(SST[i] + ST[i])
                TimeInSystem.append(end_time[i] - ordinary_AT[ordinary_iterator])
                if WT[i] > 0:
                    probability_ordinary += 1
                WT_O.append(WT[i])
                ordinary_iterator += 1
                Type.append('O')

            idle.append(max(0, SST[i] - end_time[i - 1]))
    probability_of_Idle = sum(i > 0 for i in idle) / len(idle)
    avg_service = sum(ST) / C1
    avg_WT_d = sum(WT_D) / max(len(WT_D), 1)
    avg_WT_o = sum(WT_O) / max(len(WT_O), 1)
    probability_ordinary /= ordinary_iterator
    probability_distinguished /= distinguished_iterator
    portion_of_Idle = sum(idle) / end_time[C1 - 1]

    t = PrettyTable(['Type', 'IAT', 'AT', 'ST', 'SST', 'WT',
                     'CT', 'TIS', 'idle'])

    for i in range(C1):
        t.add_row([Type[i], IAT[i], AT[i], ST[i], SST[i], WT[i], end_time[i], TimeInSystem[i], idle[i]])

    print(t)
    print('\n')
    # Print what you calculate
    print("Probability of IDle= ", probability_of_Idle)
    print("For Ordinary Customer, Average Waiting Time= ", avg_WT_o, "  and Probability of Wait= ",
          probability_ordinary)
    print("For Distinguished Customer, Average Waiting Time= ", avg_WT_d, "  and Probability of Wait= ",
          probability_distinguished)
    print("Average Service Time= ", avg_service)
    print("Portion Of Idle Time= ", portion_of_Idle)

    print("Max Queue Length, for ordinary customers=", ordinary_iterator, "  and for distinguished customers=",
          distinguished_iterator)
    print('\n')
    # show histogram for waiting for both types of Customer
    plt.hist(WT_O)
    plt.ylabel("Probability of Wait for Ordinary Customers")
    plt.xlabel("Values of Waiting Time Ordinary Customers")
    plt.show()
    plt.hist(WT_D)
    plt.ylabel("Probability of Wait for Distinguished Customers")
    plt.xlabel("Values of Waiting Time Distinguished Customers")
    plt.show()


def two_teller(C2):
    ordinary_IAT = list()
    ordinary_AT = list()
    ordinary_ST = list()

    distinguished_IAT = list()
    distinguished_AT = list()
    distinguished_ST = list()

    # generate(Random Variables) in Calendar
    for i in range(C2):
        # Inter Arrival Time For Ordinary
        ordinary_IAT.append(generate_IAT_O())
        # Arrival Time For Ordinary
        if i != 0:
            ordinary_AT.append(ordinary_AT[i - 1] + ordinary_IAT[i])
        else:
            ordinary_AT.append(ordinary_IAT[0])
        # Service Time For Ordinary
        ordinary_ST.append(generate_ST_O())

        # Inter Arrival Time For Distinguished
        distinguished_IAT.append(generate_IAT_D())
        # Arrival Time For Distinguished
        if i != 0:
            distinguished_AT.append(distinguished_AT[i - 1] + distinguished_IAT[i])
        else:
            distinguished_AT.append(distinguished_IAT[0])
        # Service Time For Distinguished
        distinguished_ST.append(generate_ST_D())

    Type = list()  # Type for each entered Customer
    IAT = list()  # inter arrive time for System
    AT = list()  # arrive time for System
    ST = list()  # Service time for System
    SST = list()  # Service Start time for System
    WT = list()  # witting time for System
    idle = list()  # Idle time for System
    TimeInSystem = list()  # list contain witting In System for each Customer
    end_time_t1 = list()  # list contain end time for each service for first teller
    end_time_t2 = list()  # list contain end time for each service for second teller
    WT_O = list()  # witting time for ordinary Customers
    WT_D = list()  # witting time for ordinary Distinguished

    ordinary_iterator = 0  # iterator iterate in ordinary lists
    distinguished_iterator = 0  # iterator iterate in Distinguished lists
    probability_ordinary = 0  # use to count probability of wait for ordinary Customers
    probability_distinguished = 0  # use to count probability of wait for Distinguished Customers

    for i in range(C2):
        if i == 0:
            # first serve the first customer entered if the arrival time less than the other next customer
            if distinguished_AT[distinguished_iterator] <= ordinary_AT[ordinary_iterator]:
                IAT.append(distinguished_IAT[distinguished_iterator])
                AT.append(distinguished_AT[distinguished_iterator])
                ST.append(distinguished_ST[distinguished_iterator])
                SST.append(distinguished_AT[distinguished_iterator])
                distinguished_iterator += 1
                end_time_t1.append(0)
                end_time_t2.append(SST[i] + ST[i])
                Type.append('D')
            else:
                IAT.append(ordinary_IAT[ordinary_iterator])
                AT.append(ordinary_AT[ordinary_iterator])
                ST.append(ordinary_ST[ordinary_iterator])
                SST.append(ordinary_AT[ordinary_iterator])
                ordinary_iterator += 1
                end_time_t1.append(SST[i] + ST[i])
                end_time_t2.append(0)
                Type.append('O')
            WT.append(0)
            TimeInSystem.append(ST[i])
            idle.append(IAT[i])
        else:
            # serve one with less arrival time
            # teller 1 for Ordinary Customers, teller 2 for Distinguished Customers
            if distinguished_AT[distinguished_iterator] <= ordinary_AT[ordinary_iterator]:
                IAT.append(distinguished_IAT[distinguished_iterator])
                AT.append(distinguished_AT[distinguished_iterator])
                ST.append(distinguished_ST[distinguished_iterator])
                SST.append(max(end_time_t2[i - 1], distinguished_AT[distinguished_iterator]))
                WT.append(max(0, end_time_t2[i - 1] - distinguished_AT[distinguished_iterator]))
                end_time_t1.append(end_time_t1[i - 1])
                end_time_t2.append(SST[i] + ST[i])
                TimeInSystem.append(end_time_t1[i] - distinguished_AT[distinguished_iterator])

                # if waiting time more than 0, that mean there are probability of wait
                if WT[i] > 0:
                    probability_distinguished += 1
                WT_D.append(WT[i])
                distinguished_iterator += 1
                Type.append('D')
            else:
                IAT.append(ordinary_IAT[ordinary_iterator])
                AT.append(ordinary_AT[ordinary_iterator])
                ST.append(ordinary_ST[ordinary_iterator])
                SST.append(max(end_time_t1[i - 1], ordinary_AT[ordinary_iterator]))
                WT.append(max(0, end_time_t1[i - 1] - ordinary_AT[ordinary_iterator]))
                end_time_t1.append(SST[i] + ST[i])
                end_time_t2.append(end_time_t2[i - 1])
                TimeInSystem.append(end_time_t1[i] - ordinary_AT[ordinary_iterator])

                # if waiting time more than 0, that mean there are probablity of wait
                if WT[i] > 0:
                    probability_ordinary += 1
                WT_O.append(WT[i])
                ordinary_iterator += 1
                Type.append('O')
            idle.append(max(0, SST[i] - end_time_t1[i - 1]))
    avg_service = sum(ST) / C2
    avg_WT_d = sum(WT_D) / len(WT_D)
    avg_WT_o = sum(WT_O) / len(WT_O)
    probability_of_Idle = sum(i > 0 for i in idle) / len(idle)

    probability_ordinary /= ordinary_iterator
    probability_distinguished /= distinguished_iterator
    portion_of_Idle = sum(idle) / end_time_t1[C2 - 1]

    t = PrettyTable(['Type', 'IAT', 'AT', 'ST', 'SST', 'WT', 'CT-t1', 'CT-t2', 'TIS', 'idle'])
    for i in range(C2):
        t.add_row(
            [Type[i], IAT[i], AT[i], ST[i], SST[i], WT[i], end_time_t1[i], end_time_t2[i], TimeInSystem[i], idle[i]])

    print(t)
    print('\n')
    # Print what you calculate
    print("For Ordinary Customer, Average Waiting Time= ", avg_WT_o, "  and Probability of Wait= ", probability_ordinary)
    print("For Distinguished Customer, Average Waiting Time= ", avg_WT_d, "  and Probability of Wait= ",
          probability_distinguished)
    print("Probability of IDle= ", probability_of_Idle)
    print("Average Service Time= ", avg_service)
    print("Portion Of Idle Time= ", portion_of_Idle)
    print("Max Queue Length, for ordinary customers=", ordinary_iterator, "  and for distinguished customers=",
          distinguished_iterator)
    print('\n')

    # show histogram for waiting for both types of Customer
    plt.hist(WT_O)
    plt.ylabel("Probability of Wait for Ordinary Customers")
    plt.xlabel("Values of Waiting Time Ordinary Customers")
    plt.show()
    plt.hist(WT_D)
    plt.ylabel("Probability of Wait for Distinguished Customers")
    plt.xlabel("Values of Waiting Time Distinguished Customers")
    plt.show()


Customers = int(input("Enter the Number of Customers to be served:\t"))
option = input("If you wanna 1 teller for both Types Enter 1, and for one teller for each Type Enter:\t")
trails = int(input("Enter the Number of Trails:\t"))
# if user type 1, 1 teller will serve both types of customers
if option == '1':
    print("For One teller")
    for i in range(trails):
        print("Trail ", i + 1)
        one_teller(Customers)
# if user type anything not 1, will be one teller to serve each type of Customers
else:
    print("For Two teller")
    for i in range(trails):
        print("Trail ", i + 1)
        two_teller(Customers)
