import datetime
import matplotlib
import matplotlib.pyplot as plt
import random


class modelTime:
    def __init__(self):
        self.day = 0
        self.hour = 0
        self.minute = 0



    def more(self, timer):
        if(self.day<timer.day):
            return False
        elif(self.day>timer.day):
            return True
        else:
            if (self.hour < timer.hour):
                return False
            elif (self.hour > timer.hour):
                return True
            else:
                if (self.minute < timer.minute):
                    return False
                elif (self.minute > timer.minute):
                    return True

def sum(self, timer):
        self.minute += timer.minutes
        if (self.minute + timer.minutes > 60):
            self.minute = self.minute % 60
            if(self.hour+1>9):
                self.hour = 0
                self.day+=1
            else:
                self.hour+=1
        self.hour+=timer.hour
        if (self.hour > 9):
            self.hour = self.hour%9
            self.day += 1
        self.day+=timer.day
        return self


def sumMin(time, minutes):
    timer = modelTime()
    timer.minute = time.minute
    timer.hour = time.hour
    timer.day = time.day
    timer.minute += minutes
    if (timer.minute + minutes > 60):
        timer.minute = timer.minute % 60
        if (timer.hour + 1 > 9):
            timer.hour = 0
            timer.day += 1
        else:
            timer.hour += 1
    return timer


def sumHour(time, hours):
    timer = modelTime()
    timer.minute = time.minute
    timer.hour = time.hour
    timer.day = time.day
    timer.hour += hours
    if (timer.hour > 9):
        timer.hour = timer.hour % 9
        timer.day += 1
    return timer


class Entity:
    def __init__(self, kind, service, timer):
        self.type = kind
        self.service = service
        self.time = random.randint(10,45)
        self.timer = modelTime()
        self.timer.minute = timer.minute
        self.timer.hour = timer.hour
        self.timer.day = timer.day

class Worker:
    def __init__(self, kind):
        self.kind = kind
        self.state = "free"
        self.timer = modelTime()
        self.time = 0


    def set_to_work(self, timer, time):
        self.timer.minute = timer.minute
        self.timer.hour = timer.hour
        self.timer.day = timer.day
        self.time = time
        self.state = "work"

class timerBP:
    def __init__(self, type):
        self.minute = random.randint(0,59)
        self.type = type


rate10=[7,12,10,7,5,4,5,4,3]
rate20=[8,11,8,9,6,4,3,3,2]
rate30=[5,6,5,4,3,3,2,2,1]
rate40=[2,3,4,3,2,1,1,1,1]



# Очереди задач
normQ = []
premQ = []
# Внутренняя механика
taskInc = []
i=0
# Рабочие
typeA = 5
typeB = 3
workersA = []
workersB = []
# Вероятность попадания в нормальную очередь для заказов разных типов
typesPossibQueue = [35,30,25,15]

# Добавление рабочих
while i<typeA:
    workersA.append(Worker('A'))
    i+=1
i=0
while i<typeB:
    workersB.append(Worker('B'))
    i+=1
i=0
# _________________________________________

donen =0
donep =0
notdonen =0
notdonep =0
timer = modelTime()
while timer.day < 25:
        while timer.hour < 9:
            # Распределение появления заказов за следующий час
            while i<rate10[timer.hour]:
                taskInc.append(timerBP(1))
                i+=1
            i = 0
            while i<rate20[timer.hour]:
                taskInc.append(timerBP(2))
                i += 1
            i = 0
            while i<rate30[timer.hour]:
                taskInc.append(timerBP(3))
                i += 1
            i = 0
            while i<rate40[timer.hour]:
                taskInc.append(timerBP(4))
                i += 1
            i = 0
            taskInc = sorted(taskInc,key = lambda task: task.minute)
            #--------------------------------------------------------------------------------------------------------

            while timer.minute < 60 :
                # Появление заказа в момент времени и запись его в очередь
                checktime = sumHour(timer,1)
                while   len(taskInc)!=0 and timer.minute == taskInc[0].minute:
                    possib = random.randint(0,100)
                    if(possib<typesPossibQueue[taskInc[0].type-1]):
                            normQ.append(Entity(taskInc[0].type,"n",timer))
                    else:
                            premQ.append(Entity(taskInc[0].type,"p", timer))
                    taskInc.pop(0)
                # ----------------------------------------------------------

                # Распределение заказов между рабочими(можно оптимизировать, добавив время занятости)
                if(timer.hour<8 and timer.minute<30):
                    # Заказы для работников типа А
                    while i < len(workersA):
                        if(workersA[i].state == "free"):
                            j=0
                            while len(premQ)!=0 and j<len(premQ) and checktime.more( sumHour(premQ[j].timer,3) ) :
                                if(premQ[j].type == 1 or premQ[j].type == 2):
                                    workersA[i].set_to_work(timer, premQ[j].time)
                                    donep += 1
                                    premQ.pop(j)
                                    break
                                else:
                                    j+=1

                            j = 0

                            while len(normQ)!=0 and j<len(normQ) and checktime.more(sumHour(normQ[j].timer,3)) and workersA[i].state == "free" :
                                if(normQ[j].type == 1 or normQ[j].type == 2):
                                    workersA[i].set_to_work(timer, normQ[j].time)
                                    donen += 1
                                    normQ.pop(j)
                                    break
                                else:
                                    j+=1
                            j=0

                            while len(premQ)!=0 and j<len(premQ) and workersA[i].state == "free" :
                                if(premQ[j].type == 1 or premQ[j].type == 2):
                                    workersA[i].set_to_work(timer, premQ[j].time)
                                    donep += 1
                                    premQ.pop(j)
                                    break
                                else:
                                    j+=1
                            j=0

                            while len(normQ)!=0 and j<len(normQ) and workersA[i].state == "free" :
                                if(normQ[j].type == 1 or normQ[j].type == 2):
                                    workersA[i].set_to_work(timer, normQ[j].time)
                                    donen += 1
                                    normQ.pop(j)
                                    break
                                else:
                                    j+=1
                            j=0
                        else:
                            if(workersA[i].state == "work"):
                                if(timer.more(sumMin(workersA[i].timer,workersA[i].time))):
                                    workersA[i].state = "free"
                            else:
                                if(timer.more(sumHour(workersA[i].timer, 1))):
                                    workersA[i].state = "free"
                        i+=1
                    i=0

                    #         _______________________________________________________________________________________________
                    # Заказы для работников типа B
                    while i < len(workersB):
                        if (workersB[i].state == "free"):
                            if len(premQ) != 0 and checktime.more(sumHour(premQ[0].timer, 3)):
                                workersB[i].set_to_work(timer, premQ[0].time)
                                donep += 1
                                premQ.pop(0)


                            if len(normQ) != 0 and checktime.more(sumHour(normQ[0].timer, 3)):
                                workersB[i].set_to_work(timer, normQ[0].time)
                                donen += 1
                                normQ.pop(0)


                            if len(premQ) != 0:
                                workersB[i].set_to_work(timer, premQ[0].time)
                                donep += 1
                                premQ.pop(0)


                            if len(normQ) != 0 :
                                workersB[i].set_to_work(timer, normQ[0].time)
                                donen += 1
                                normQ.pop(0)

                        else:
                            if (workersB[i].state == "work"):
                                if (timer.more(sumMin(workersB[i].timer, workersB[i].time))):

                                    workersB[i].state = "free"
                            else:
                                if (timer.more(sumHour(workersB[i].timer, 1))):
                                    workersB[i].state = "free"
                        i+=1
                    i=0
                #             _______________________________________________________________________________________________________
                #
                # Проверка и очистка очередей задач
                while  i<len(normQ) and timer.more(sumHour(normQ[i].timer,9)):
                    normQ.pop(i)
                    notdonen+=1
                    i+=1
                i=0
                while  i<len(premQ) and timer.more(sumHour(premQ[i].timer,9)):
                    premQ.pop(i)
                    notdonep += 1
                    i+=1
                i=0


                timer.minute+=1
            timer.minute =0
            timer.hour+=1
        timer.hour = 0
        timer.day += 1

print(donen)
print(donep)
print(notdonen)
print(notdonep)