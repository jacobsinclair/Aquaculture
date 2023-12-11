#=====================================================================================================================================================================================================================
#                                                                     ~ Continuous-Time Simulation Of Chemical Concentration in Aquariums ~
#                                                                      File: fish.py
#                                                                      Authors: 
#                                                                      Description: 'Fish' object, used to implement fish objects to interact with the system  
#
#
#
#=====================================================================================================================================================================================================================

import random 

class fish:

    def __init__(self, name, eatPercent, poopPercent,peePercent, deathPercent, servingSize, weight,tankSize):
        self.name = name
        self.eatPercent = eatPercent
        self.poopPercent = poopPercent
        self.peePercent = peePercent
        self.deathPercent = deathPercent
        self.servingSize = servingSize
        self.weight = weight
        self.living = True
        self.status = 'Nothing'
        self.deadlyC1 = 2
        self.deadlyC3 = 5
        self.health = 86400 # A day in seconds
        self.tankSize = tankSize
    
    #these still need work, specifically in calculating the chemical changes

    def checkDeath(self,C1,C3):
        C1Conc = C1/self.tankSize
        C3Conc = C3/self.tankSize
        if (C1Conc) > self.deadlyC1 or (C3Conc) > self.deadlyC3:
            self.health -= 1
            #print(f"{self.name} is taking damage C1 (mg/l): {C1Conc} C3 (mg/l): {C3Conc}")
            if self.health <= 0:
                #print(f"{self.name} is at {self.health} health and is dying")
                self.living = False   
        return self.living
    
    def Eat(self):
        self.status = 'Eating'
        result = (self.weight*self.servingSize)
        return result
        
    def Poop(self):
        self.status = 'Pooping'
        result = (self.weight/3)
        self.weight -= result
        return result
        
    def Pee(self,t):
        self.status = 'Peeing'
        days = (t/3600)*24
        ratio = 0.00022046      # G ammonia per G fish per day
        result = self.weight * ratio * days
        return result
    
    def grow(self,t):
        GrowthRate = 13.75/(604800)    #Grows to 440 grams over 8 months
        if self.weight <= 440:
            self.weight += GrowthRate
            
    def getWeight(self):
        return self.weight

    def getAmmountEaten(self):
        return (self.servingSize / 326) # Converts the serving size to a normalized value on the plant biomass and returns it

    def action(self,t):
        fishActionProb = random.random()
        #print(fishActionProb)
        if fishActionProb >= 0.0 and fishActionProb <= self.eatPercent:      #fish eats if the random number is in this range 
            result = self.Eat() 
        elif fishActionProb > self.eatPercent and fishActionProb <= self.poopPercent: #fish poops if the random number is in this range   
            result = self.Poop()
        elif fishActionProb > self.poopPercent and fishActionProb <= self.peePercent: #fish pees if the random number is in this range
            result = self.Pee(t) 
            #print(fishActionProb,self.eatPercent,self.poopPercent,self.peePercent)
            
        else:                                                          #if none of these if statements are fulfilled, the fish is doing no actions
            result = 0
            self.status = "Nothing"
            
        #  print(self.status)
        return result,self.status
    

            
       


   
