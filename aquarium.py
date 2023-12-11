#=====================================================================================================================================================================================================================
#                                                                     ~ Continuous-Time Simulation Of Chemical Concentration in Aquariums ~
#                                                                      File: aquarium.py
#                                                                      Authors: 
#                                                                      Description: Keeps track of the values of relevant chemicals in an aquarium system over time.
#
#
#
#=====================================================================================================================================================================================================================
# Imports 
import numpy as np
import math
import random
import matplotlib.pyplot as plt
from alive_progress import alive_bar
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QComboBox,QHBoxLayout,QProgressBar
from fish import fish





# Constants
Xmin = 0
Xmin = 0
Xmax = (24*math.pi)
Ymin = -(6*math.pi)
Ymax = (5* math.pi)
Zmin = (-6* math.pi)
Zmax = (2* math.pi)
Wishbone = (5 * pow(10,-6))
Wishbone1 = (2 * pow(10,-8))
Wishbone2 = (3 * pow(10,-6))
V = 4838400     # Period of time to run sim over before list is cleared
numV = 1        # Amount of times period of V is simulated 
tmin = 0


def p1(t):  # function for ammonia production
  step1 = np.arctan(t0(t))             
  step2 = step1 - np.arctan(t0(0))              
  step3 = Wishbone * step2
  return step3

p2 = pow(10,-4) # oxygen production within the aquarium
p3 = 0 # p3 nitrite consumtion 
p4 = (2* pow(10,-17)) # nitrate consumption 
q1 = (1/5) # constant limiting coefficient for ammonia growth
q2 = (1/8.5) # limiting coefficient for oxygen growth 

# inital p2 and p4 for calculation
p2i = p2
p4i = p4




# Define Functions

def convert_seconds_to_weeks(seconds):
    dtWeeks = []
    for t in seconds:
        weeks = t/(604800)  # 604800 seconds in a week
        dtWeeks.append(weeks)
    return dtWeeks  
# Mu s, which represent efficiencies of different bacteria 
def mu1(t): #nitrosominous 
  result = Wishbone1*(np.arctan([t1(t)])-np.arctan([t1(tmin)]))
  return result
  
def mu2(t): # nitrobacter 
  result = Wishbone2*(np.arctan(t2(t))-np.arctan(t2(tmin)))
  return result

# t functions, act as constants in our equation, were described by paper  
def t0(t):
    return(((Xmax - Xmin) / V)*t + Xmin)

def t1(t):
    return(((Ymax - Ymin) / V)*t + Ymin)
    
def t2(t):
    return(((Zmax - Zmin) / V)*t + Zmin)  


# Change of concentration of Nitrate

def changeInAmmonia(t,C1,C2):
  step1 = p1(t) * (1 - ((q1) * C1))
  step2 = step1 - mu1(t) * ((C1 * C1) * (C2 * C2 * C2))
  concentrationChange = step2
  return concentrationChange

def changeInOxygen(t,C1,C2,C3):    # Change of Oxygen concentration over time 
    result = p2*(1-(q1)*(C2))-mu1(t)*pow(C1,2)*pow(C2,3)-mu2(t)*np.sqrt(C2)*C3
    return result
  
def changeInNitrite(t,C1,C2,C3):    # Change of Nitrite concentration over time 
    result = mu1(t)*(pow(C1,2))*(pow(C2,3))-mu2(t)*np.sqrt(C2)*C3-p3*C3
    return result

def changeInNitrate(t,C2,C3,C4):    # Change of Nitrate concentration over time 
  dt = 1
  dC4 = dt*(mu2(t)* np.sqrt(C2)*C3-(p4*C4))
  return dC4


   


#======================================================================================================================================
# Sim Function 
#======================================================================================================================================
def simulation(tank_size, number_of_fish, type_of_fish, duration, production, save_log, fish_list):
    print("=============================================================================================================================")
    print("\n\n")
    print("                              Agent-Based Continuous-Time Simulation of Aquaculture Systems                                     ")
    print("                           Written By: Alex Puskaric, Devon Godde, Elijah Muzzi, Jacob Sinclair                                 ") 
    print("\n")
    print("=============================================================================================================================")
    print("\n\nStarting Simulation...\n\n")


    # Plant Biomass List
    plantPopulation = [0.5, (0.00000019*1)] # Normalized Plant Biomass, Growth Rate per Second

    # Constants
    fish_population = fish_list
    V = int(duration)
    dt = 1
    alivebaramount = V // dt
    dead_fish = []
    numFish = []
    
    #numFish.append(number_of_fish)

    

   
    # Reset chemical concentrations for each simulation run
    C1, C2, C3, C4 = 0, 8.5, 0, 0
    C1i, C2i, C3i, C4i = 0, 8.5, 0, 0
    dC1, dC2, dC3, dC4, dT = [], [], [], [], []
    aC1,aC2,aC3,aC4 = [],[],[],[]
    log = []
    output_file = open('event_log.txt','w')
    selfSufficient = True


    with alive_bar(alivebaramount) as bar:
        for t in range(V):
            for fish in fish_population:
                index = fish_population.index(fish) + 1
                action_result, status = fish.action(t)
                if status == 'Eating':
                    if save_log:
                        log.append(f"{fish.name} is eating at time {t} seconds\n")
                    plantPopulation[0] = plantPopulation[0] - fish.getAmmountEaten()
                    # Modify chemicals accordingly
                    
                elif status == 'Pooping':
                    #C1 += action_result  # Assuming action_result is the increase in Ammonia
                    if save_log:
                        log.append(f"{fish.name} is pooping at time {t} seconds\n")
                elif status == 'Peeing':
                    if save_log:
                        log.append(f"{fish.name} is peeing at {t} seconds\n")
                    # Modify chemicals accordingly
                    C1 += action_result
                fish.grow(t)
                if not fish.checkDeath(C1,C3):
                    if save_log:
                        log.append(f"{fish.name} has died at {t} seconds at C1 (mg/L) {C1/tank_size} & C3 (mg/L) {C3/tank_size}\n")
                    selfSufficient = False
                    fish_population.remove(fish)
                    dead_fish.append(fish)
            
      

            # If plant biomass is greater than max, set it to max
            if((plantPopulation[0] + plantPopulation[1]) >= 1):
                plantPopulation[0] = 1
            # If plant biomass is at or less than 0, keep it at 0
            elif(plantPopulation[0] <= 0):
                plantPopulation[0] = 0
            # Otherwise, grow
            elif(plantPopulation[0] > 0):
                plantPopulation[0] = plantPopulation[0] + plantPopulation[1]

            p2 = p2i * (0.5 + plantPopulation[0])
            p4 = p4i * (0.5 + plantPopulation[0])  

            C1 += changeInAmmonia(t,C1,C2)
            C2 += changeInOxygen(t,C1,C2,C3)
            C3 += changeInNitrite(t,C1,C2,C3)
            C4 += changeInNitrate(t,C2,C3,C4)

            dC1.append(C1 - C1i)
            dC3.append(C3 - C3i)
            dC4.append(C4 - C4i)
            
            aC1.append((C1/tank_size))
            aC3.append((C3/tank_size))
            aC4.append((C4/tank_size))
            dT.append(t)
            numFish.append(len(fish_population))

                
             
            bar()
    if save_log:
        print("Saving log...")
        for event in log:
            output_file.write(event)   
        output_file.close()
    plot_results(dC1, dC3, dC4, dT, number_of_fish, fish_population, production, tank_size,selfSufficient,V,numFish,aC1,aC3,aC4,plantPopulation)

    
#======================================================================================================================================
# Plotting Start
#======================================================================================================================================
def plot_results(dC1, dC3, dC4, dT, number_of_fish, fish_population, production, tank_size, selfSufficient, duration, numFish, aC1, aC3, aC4,plantPopulation):
    plt.style.use('Solarize_Light2')  # Using a predefined style for nicer plots
    fig, ax = plt.subplots(2, 2, figsize=(12, 10))
    
    #print(plt.style.available)
    

    # Chemical Change plots
    time_weeks = convert_seconds_to_weeks(dT)
    ax[0, 0].plot(time_weeks, dC1, label='Ammonia', color='tab:orange')
    ax[0, 0].plot(time_weeks, dC3, label='Nitrite', color='tab:red')
    ax[0, 0].plot(time_weeks, dC4, label='Nitrate', color='tab:green')
    ax[0, 0].legend(loc='upper right')
    ax[0, 0].set_title('Change in Chemicals Over Time', fontsize=14, fontweight='bold') 
    ax[0, 0].set_xlabel('Time (Weeks)', fontsize=12)
    ax[0, 0].set_ylabel('Change in Concentration (mg/L)', fontsize=12)

    # Calculating Total Production
    total_production = sum(fish.getWeight() for fish in fish_population)
    formatted_production = "{:.2f}".format(float(total_production))
    formatted_weeks = "{:.2f}".format(int(duration) / 604800)
    plantBiomass = ("{:.4f}".format( float(plantPopulation[0]) ))

    tankStatus = (f"\n\n\nAquaculture Tank Stats\n"
                  f"________________________________________\n\n\n"
                  f"Tank Size: {tank_size} Liters\n\n"
                  f"The Tank will Grow Harvestable Fish: {selfSufficient}\n\n"
                  f"Amount of Fish Produced (g): {formatted_production}\n\n"
                  f"Time Elapsed in Week(s): {formatted_weeks}\n\n"
                  f"Plant Biomass: {plantBiomass}\n\n")
                    
    
    # Fish Population Plot
    ax[1, 0].plot(time_weeks, numFish, label='Fish Population', color='tab:orange')
    ax[1, 0].set_title('Populations Over Time', fontsize=14, fontweight='bold')
    ax[1, 0].set_xlabel('Time (Weeks)', fontsize=12)
    ax[1, 0].set_ylabel('Population Size', fontsize=12)
    ax[1, 0].legend(loc='upper right')

    # Chemical Concentration Plots
    ax[0, 1].plot(time_weeks, aC1, label='Ammonia', color='tab:orange')
    ax[0, 1].plot(time_weeks, aC3, label='Nitrite', color='tab:red')
    ax[0, 1].plot(time_weeks, aC4, label='Nitrate', color='tab:green')
    # Add horizontal lines for deadly levels
    ax[0, 1].axhline(y=2, color='orange', linestyle='--', label='Deadly Ammonia Level')
    ax[0, 1].axhline(y=5, color='red', linestyle='--', label='Deadly Nitrite Level')
    ax[0, 1].legend(loc='upper right')
   

    # Add text labels for the horizontal lines
   
    ax[0, 1].set_title(f'Chemicals Concentration Over Time ({tank_size} Liters)', fontsize=14, fontweight='bold') 
    ax[0, 1].set_xlabel('Time (Weeks)', fontsize=12)
    ax[0, 1].set_ylabel('Concentration (mg/L)', fontsize=12)

    # Tank Status Text
    ax[1, 1].axis('off')
    ax[1, 1].text(0.410, 0.8681, tankStatus, fontsize=20, ha='center', va='center')

    plt.tight_layout()
    plt.show()

# GUI

class AquariumSimulatorGUI(QWidget):
    def __init__(self):
        super().__init__()
        x = 600
        y = 400
        
        # GUI layout
        self.setWindowTitle('Aquaculture Simulation')
        self.setFixedSize(x, y)  # Width, Height in pixels
        layout = QVBoxLayout()
        header = QLabel('<h1 style="color: blue; text-align: center; margin-top: -10px; margin-bottom: -10px; line-height: 1">Aquaculture Simulation</h1>')
        layout.addWidget(header)

        # Tank Size Input
        volumeLayout = QHBoxLayout()  # Horizontal layout for volume input and unit dropdown
        self.tankSizeInput = QLineEdit(self)
        volumeLayout.addWidget(QLabel('Tank Size:'))
        volumeLayout.addWidget(self.tankSizeInput)
        self.volUnitDropdown = QComboBox(self)
        self.volUnitDropdown.setFixedWidth(int (y/2))
        self.tankSizeInput.setFixedWidth(int (y/2))  # Set the width to half of the GUI width
        self.volUnitDropdown.addItems(["Liters", "Gallons"])
        volumeLayout.addWidget(self.volUnitDropdown)
        layout.addLayout(volumeLayout)  # Add the horizontal layout to the main layout

        # Number of Fish Input
        numFishLayout = QHBoxLayout()  # Horizontal layout for number of fish input 
        self.numberOfFishInput = QLineEdit(self)
        numFishLayout.addWidget(QLabel('Number of Fish:'))
        #self.numberOfFishInput.setFixedWidth(int (y/2))
        numFishLayout.addWidget(self.numberOfFishInput)
        layout.addLayout(numFishLayout)  # Add the horizontal layout to the main layout
       

        # Creating a QComboBox
        sizeFishLayout = QHBoxLayout()  # Horizontal layout for size of fish input 
        self.dropdown = QComboBox()
        sizeFishLayout.addWidget(QLabel('Size of Fish:'))
        self.dropdown.addItem('Fry- 1 gram')
        self.dropdown.addItem('Juveniles- 8 to 9 grams')
        self.dropdown.addItem('Adults- 220 to 440 grams (1 to 2 pounds)')

        # Connecting a function to handle the item selection change
        self.dropdown.currentIndexChanged.connect(self.on_selection_change)

        sizeFishLayout.addWidget(self.dropdown)
        layout.addLayout(sizeFishLayout)  # Add the horizontal layout to the main layout

         # Duration of Simulation Input with Unit Dropdown
        durationLayout = QHBoxLayout()  # Horizontal layout for duration input and unit dropdown
        self.durationInput = QLineEdit(self)
        self.durationInput.setFixedWidth(int (y/2))  # Set the width to half of the GUI width
        durationLayout.addWidget(QLabel('Duration of Simulation:'))
        durationLayout.addWidget(self.durationInput)

        # Unit of Time Dropdown
        self.unitDropdown = QComboBox(self)
        self.unitDropdown.addItems(["Seconds", "Weeks", "Months"])
        durationLayout.addWidget(self.unitDropdown)

        layout.addLayout(durationLayout)  # Add the horizontal layout to the main layout
       


        # Other input fields and buttons...
        
        
        # Save Log Checkbox
        self.saveLogCheckbox = QCheckBox('Save Log to Folder', self)
        layout.addWidget(self.saveLogCheckbox)

        # Start Simulation Button
        self.startButton = QPushButton('Start Simulation', self)
        self.startButton.clicked.connect(self.start_simulation)
        layout.addWidget(self.startButton)
        

        
        self.setLayout(layout)

       
        

      


    def on_selection_change(self, index):
        selected_item = self.dropdown.currentText()
        print(f"Selected: {selected_item}")

    def start_simulation(self):
        
        if not self.tankSizeInput.text().isdigit() or not self.numberOfFishInput.text().isdigit():
            print("Please enter valid numeric inputs for tank size and number of fish.")
        # Get input values
        tank_size = int (self.tankSizeInput.text())
        number_of_fish = int (self.numberOfFishInput.text())
        fish_weights = 0
        timeRatio = 1
        volumeRatio = 1

        # choosing the starting weight of the fish based on the value the user selects
        if 'Fry- 1 gram' in self.dropdown.currentText():
            fish_weights = 1
        elif 'Juveniles- 8 to 9 grams' in self.dropdown.currentText():
            fish_weights = random.randint(8, 9)
        elif 'Adults- 220 to 440 grams (0.5 to 1 pound)' in self.dropdown.currentText():
            fish_weights = random.randint(220, 440)
            
        if 'Seconds' in self.unitDropdown.currentText():
            timeRatio = 1
        elif 'Weeks' in self.unitDropdown.currentText():
            timeRatio = 604800  # Seconds in a week
        elif 'Months' in self.unitDropdown.currentText():
            timeRatio = 2630000  # Approximate seconds in a month
            
        if 'Liters' in self.volUnitDropdown.currentText():
            volumeRatio = 1
        elif 'Gallons' in self.volUnitDropdown.currentText():
            volumeRatio = 0.264172  # Gallons in a Liter

        duration = int(self.durationInput.text()) * timeRatio
        save_log = self.saveLogCheckbox.isChecked()
        production = 0
        tank_size = int (tank_size * volumeRatio)
        
        fish_population = [fish(f'Tilapia{x}', 0.0000069, 0.0000104, 0.0000173, 0, 0.02, fish_weights,tank_size) for x in range(number_of_fish)]
    
        


        # Start the simulation with these parameters
        print(f"Starting simulation with: Tank size: {tank_size} liters, Number of fish: {number_of_fish}, Size of fish: {self.dropdown.currentText()}, Duration: {duration} seconds, Save log: {save_log}")
        simulation(tank_size, number_of_fish, fish_weights, duration, production, save_log, fish_population)

          
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AquariumSimulatorGUI()
    window.show()
    sys.exit(app.exec_())

