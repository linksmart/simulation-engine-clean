import logging
import json
import os
import time
import sys

from profess.JSONparser import *
from profess.Profess import *
from simulator.openDSS import OpenDSS
from data_management.redisDB import RedisDB
from profiles.profiles import *
#from simulation_management import simulation_management as SM
from data_management.inputController import InputController
from data_management.utils import Utils
import threading

logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s: %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__file__)


class gridController(threading.Thread):

    def __init__(self, id, duration):
        super(gridController, self).__init__()
        logger.info("Initializing simulation controller")
        self.sim = OpenDSS(id)
        self.id = id
        logger.debug("id "+str(id))
        self.nodeNames =[]
        self.allBusMagPu=[]
        self.yCurrent = []
        self.losses = []
        self.voltage_bases = []
        self.city = None
        self.country = None
        self.redisDB = RedisDB()
        self.lock_key = "id_lock"
        self.stop_signal_key = "opt_stop_" + self.id
        self.finish_status_key = "finish_status_" + self.id
        self.redisDB.set(self.stop_signal_key, "False")
        self.redisDB.set(self.finish_status_key, "False")
        self.sim_days = duration
        logger.debug("Starting input controller")
        self.input = InputController(id, self.sim, self.sim_days)
        self.topology = self.input.get_topology()
        self.utils = Utils()

        self.stopRequest = threading.Event()
        logger.debug("Simulation controller initiated")


    def get_profess_url(self):
        return self.profess_url



    def getId(self):
        return self.id



    def join(self, timeout=None):
        self.stopRequest.set()
        super(gridController, self).join(timeout)

    def Stop(self):
        try:
            self.sim.Stop()
        except Exception as e:
            self.logger.error("error stopping simulator " + str(e))

        self.redisDB.set(self.stop_signal_key, "True")
        if self.isAlive():
            self.join(1)


    def get_finish_status(self):
        return self.redisDB.get(self.finish_status_key)


    def run(self):#self, id, duration):
        #self.id = id
        #self.duration = duration

        common = self.topology["common"]
        radial = self.topology["radials"]

        self.input.setNewCircuit(self.id, common)




        # ----------PROFESS----------------#
        if common["url_storage_controller"]:
            self.profess_url = common["url_storage_controller"]
            logger.debug("profess url "+str(self.profess_url))
        else:
            self.profess_url = "http://localhost:8080"
        self.domain = self.get_profess_url() + "/v1/"
        logger.debug("profess url: " + str(self.domain))
        self.profess = Profess(self.domain)
        self.profess.json_parser.set_topology(common)

        # ----------PROFILES----------------#
        self.profiles = Profiles()
        # profess.json_parser.set_topology(data)

        self.input.setup_elements_in_simulator(self.topology, self.profiles, self.profess)





        logger.debug("Simulation of grid " + self.id + " started")
        logger.debug("These are the parameters")
        logger.debug("GridID: "+str(self.id))

        #self.sim.runNode13()
        self.sim.enableCircuit(self.id)

        logger.debug("Active circuit: "+str(self.sim.getActiveCircuit()))

        ##################################################################################PROBLEM################################
      
        #self.sim.setVoltageBases(115, 4.16, 0.48)
        self.sim.setVoltageBases(self.voltage_bases)
        #self.sim.setMode("snap")
        self.sim.setMode("daily")
        self.sim.setStepSize("hours")
        self.sim.setNumberSimulations(1)
        logger.info("Solution mode 2: " + str(self.sim.getMode()))
        logger.info("Number simulations 2: " + str(self.sim.getNumberSimulations()))
        logger.info("Solution step size 2: " + str(self.sim.getStepSize()))
        logger.info("Voltage bases: " + str(self.sim.getVoltageBases()))
        logger.info("Starting Hour : " + str(self.sim.getStartingHour()))
        numSteps=self.sim_days
        self.redisDB.set("sim_days_"+str(self.id),numSteps)
        #numSteps=3
        logger.debug("Number of steps: "+str(numSteps))
        result=[]

        nodeNames = self.sim.get_node_list()

        #logger.debug("node_ names "+str(nodeNames))
        voltages = [[] for i in range(len(nodeNames))]
        currents = [[] for i in range(len(nodeNames))]
        losses = [[] for i in range(len(nodeNames))]
        powers = [[] for i in range(len(nodeNames))]

        charging = True
        logger.debug("+++++++++++++++++++++++++++++++++++++++++++")
        flag_is_storage = self.input.is_Storage_in_Topology(self.topology)

        logger.debug("flag is storage "+str(flag_is_storage))


        for i in range(numSteps):
            #time.sleep(0.5)
            logger.info("#####################################################################")
            logger.info("loop  numSteps, i= " + str(i) )
            hours = self.sim.getStartingHour()
            logger.info("Starting Hour : " + str(hours))
            logger.info("#####################################################################")

            self.redisDB.set("timestep_"+str(self.id), i)


            if flag_is_storage:
            #if "storageUnits" in self.topology["radials"][0].keys():
                logger.debug("---------storage control in the loop--------------------------------")
                #
                #logger.debug("timestep " + str(hours))
                professLoads = self.sim.getProfessLoadschapes(hours, 24)
                #logger.debug("professLoads: " + str(professLoads))
                professPVs = self.sim.getProfessLoadschapesPV(hours, 24)
                #logger.debug("professPVs: " + str(professPVs))
                dummyPrice = [3] * 24
                dummyGESSCON = [3] * 24
                logger.debug("######################Setting profess##################################")
                #profess.set_up_profess(topology, professLoads, professPVs)
                #profess.start_all()
                logger.debug("######################Ending profess##################################")

                SoC = float(self.sim.getSoCfromBattery("Akku1"))
                logger.debug("SoC_value: " + str(SoC))
                logger.debug("charging " + str(charging))
                if charging is True:
                    logger.debug("Entered to charging")
                    if SoC >= 100:
                        logger.debug("Setting charging to false")
                        charging = False
                    self.sim.setActivePowertoBatery("Akku1", -0.5)
                else:
                    logger.debug("Entered to discharging")
                    if SoC <= 20:
                        charging = True
                    self.sim.setActivePowertoBatery("Akku1",0.5)



                #profess.set_up_profess_for_existing_topology(professLoads, professPVs, dummyPrice, dummyGESSCON)
                """self.profess.set_up_profess_for_existing_topology( professLoads, self.dummyPV, self.dummyPrice, self.dummyGESSCON)
                self.profess.start_all()
                print("--------------------start profess results----------------------------")
                print(self.profess.dataList)
                print(self.profess.wait_and_get_output())
                soc_list = [{"633": {"SoC": 5}}, {"671": {"SoC": 4}}, {"634": {"SoC": 20}}]
                self.profess.update(professLoads, self.dummyPV, self.dummyPrice, soc_list, self.dummyGESSCON)
                print(self.profess.dataList)
                print("--------------------end profess results----------------------------")"""
            else:
                logger.debug("No Storage Units present")


            puVoltages, Currents, Losses = self.sim.solveCircuitSolution()
            #logger.debug("Voltage "+str(puVoltages[0]))
            for i in range(len(nodeNames)):
                voltages[i].append(puVoltages[i])
                currents[i].append(Currents[i])
                losses[i].append(Losses[i])



        #logger.debug("volt finish "+str(voltages))

        data ={}
        raw_data={}

        for i in range(len(nodeNames)):
            raw_data[nodeNames[i]] = {"Voltage": voltages[i], "Current": currents[i], "Loss": losses[i]}
            data[nodeNames[i]]={"Voltage": {"max":max(voltages[i]), "min":min(voltages[i])}, "Current":max(currents[i]), "Loss":max(losses[i])}

        data2={}
        for key, value in data.items():
            node, phase = key.split(".", 1)
            if node not in data2.keys():
                data2[node] = {}

            data2[node]["Phase_" + phase] = value


        result=data2
        #logger.debug("result: "+str(result))


        fname = (str(self.id))+"_result"
        path = os.path.join("data", str(self.id), fname)
        logger.debug("Storing results in data folder")
        self.utils.store_data(path, result)
        logger.debug("Results succesfully stored")
        logger.debug("Stroring raw data in data folder")
        fname_row = (str(self.id)) + "_result_row.json"
        path = os.path.join("data", str(self.id), fname_row)
        self.utils.store_data(path, raw_data)
        logger.debug("Raw data successfully stored")
        self.redisDB.set(self.finish_status_key, "True")



        #return id
    
    #def results(self):   
        #return (self.nodeNames, self.allBusMagPu)
        #self.finish_status = True
        #return "OK"
        """#ToDo test with snap and daily
        self.sim.setMode("daily")
        self.sim.setStepSize("minutes")
        self.sim.setNumberSimulations(1)
        self.sim.setStartingHour(0)
        self.sim.setVoltageBases(0.4,16)

        #for i in range(numSteps):
            #self.sim.solveCircuitSolution()
            #setStorageControl()
            #If
            #DSSSolution.Converged
            #Then
            #V = DSSCircuit.AllBusVmagPu

        df = self.sim.utils.lines_to_dataframe()
               data = df[['Bus1', 'Bus2']].to_dict(orient="index")
               for name in data:
                   self.sim.Circuit.SetActiveBus(f"{name}")
                   if phase in self.sim.Bus.Nodes():
                       index = self.sim.Bus.Nodes().index(phase)
                       re, im = self.sim.Bus.PuVoltage()[index:index+2]
                       V = abs(complex(re,im))
               logger.info("Voltage: " + str(V))"""
        # logger.info("Solution step size 2: " + str(self.sim.getStepSize()))
        """logger.info("Node Names: "+ str(nodeNames))
        logger.info("All Bus MagPus: " + str(allBusMagPu))
        # !TODO: return node names, voltage and current in json
        # data = {"NodeNames": nodeNames, "Voltage": allBusMagPu}
        # return json.dumps(data)
        logger.info("YCurrent: " + str(yCurrent))
        logger.info("losses: " + str(losses))
        # return ("Nodes: " + str(nodeNames), "\nVoltages " + str(allBusMagPu))
        # return (nodeNames, allBusMagPu)
        # filename = str(id)+"_results.txt"
        # !TODO: Create filename with id so serve multiple simultaneous simulations#DONE
        # json_data = json.dumps(allBusMagPu)"""
