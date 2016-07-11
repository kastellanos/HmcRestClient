#!/usr/bin/python3

# Copyright 2015, 2016 IBM Corp.
#
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from src.login_credentials import LogonRequest, LogoffModule
from src.utility import HTTPClient, HMCClientLogger,HmcHeaders
from src.generated_src import UOM
from src.common import SelectManagedSystem, PrintModule, ListModule
from src.management_console import ListManagementConsole
import sys
import os
import time
import getch
import warnings
import xml.etree.ElementTree as etree
from peewee import *
from src.management_console.HardwareManagementConsole import HardwareManagementConsole
log_object = HMCClientLogger.HMCClientLogger(__name__)
print_obj = PrintModule.PrintModule()


class HmcRestClient:
    """Interacts with client"""

    def logon_menu(self):
        while True:
            print_list = ['List managed HMC', 'Register managed HMC', 'Remove managed HMC',
                          'Active managed HMC']
            print_obj = PrintModule.PrintModule()
            auth_choice = int(print_obj.print_on_screen(print_list))

            if auth_choice == 1:
                for i in HardwareManagementConsole.select():
                    print(i.name, i.ip)
            elif auth_choice == 2:
                cls()
                self.logon_save()
            elif auth_choice == 3:
                cls()
                try:
                    hmc_list = HardwareManagementConsole.select()
                    for i in range(0, len(hmc_list)):
                        print("%s.%s " % (i + 1, hmc_list[i].name))
                    try:
                        c = int(input("\nSelect any HMC index the operation to be performed:"))
                        ch = c - 1
                        q = HardwareManagementConsole.delete().where(HardwareManagementConsole.name == hmc_list[ch].name)
                        q.execute()

                    except IndexError:
                        print("\nTry again using valid option")

                except (TypeError, AttributeError):
                    log_object.log_warn("No hmc are Available")
            elif auth_choice == 4:
                cls()
                try:
                    hmc_list = HardwareManagementConsole.select()
                    for i in range(0, len(hmc_list)):
                        print("%s.%s " % (i + 1, hmc_list[i].name))
                    try:
                        c = int(input("\nSelect any HMC index the operation to be performed:"))
                        ch = c - 1
                        hmc = hmc_list[ch]
                        return hmc
                    except IndexError:
                        print("\nTry again using valid option")

                except (TypeError, AttributeError):
                    log_object.log_warn("No hmc are Available")
    def logon_save(self):
        cls()
        logon_obj = LogonRequest.Logon()
        lro = logon_obj.LoginRequestSave()
        #try:
        print( lro )
        hmc = HardwareManagementConsole(ip=lro[0],name=lro[1],username=lro[2],password=lro[3])
        hmc.save()
        print( HardwareManagementConsole.select() )
        #except:
        #    print("Error creating HMC on database")

    def logon(self):
        """
        Initialise the process by calling logon request and
        returns the hmc ip address, current X_API_Session 


        log_object.log_debug("logon started")
        print_list = ['List managed HMC', 'Register managed HMC', 'Remove managed HMC',
                      'Active managed HMC']
        auth_choice = int(print_obj.print_on_screen(print_list))"""
        logon_obj = LogonRequest.Logon()
        self.ip,self.x_api_session = logon_obj.LogonRequest()
        global ip,x_api_session
        ip = str(self.ip)
        x_api_session = str(self.x_api_session)
                    
    def logoff_request(self):
        """ Calls Logoff Request Definition """

        logoff_obj = LogoffModule.logoff(ip, x_api_session)




def get_selectedobject(object_list):
        """
        return the logicalpartition object of users choice
        """
    
        try:
             
              for i in range(0,len(object_list)):
                 print("%s.%s " % (i+1,object_list[i].PartitionName.value()))
              try:
                  c = int(input("\nSelect any partition index the operation to be performed:"))
                  ch = c-1
                  return object_list[ch]
              except IndexError :
                  print("\nTry again using valid option")
              
        except (TypeError, AttributeError):
              log_object.log_warn("No partitions are Available")
              
def get_selectedvirtualnetwork(object_list):
        """
        Returns the virtual network of users choice
        """
        try:
              for i in range(0,len(object_list)):
                 print("%s.%s " % (i+1,object_list[i].NetworkName.value()))
              try:
                  c = int(input("\nSelect any VirtualNetwork index the operation to be performed:"))
                  ch = c-1
                  return object_list[ch]
              except IndexError :
                  print("\nTry again using valid option")
              
        except (TypeError, AttributeError):
              log_object.log_warn("No VirtualNetworks are Available")
              
def HMC_Help():
    """
    Gives the overview of each operation
    """
    cls()
    while True:
        print ("\n\n","Help".center(50))
        print_list = ["ManagedSystem","LogicalPartition","VirtualIOServer","Cluster","Performance Capaity Monitoring","Return to Main Menu"]
        choice = int(print_obj.print_on_screen(print_list))
        directory = os.path.dirname(os.path.dirname(__file__))
        if choice == 1:
             path = directory+"/help/ManagedSystem"
             files = [f for f in os.listdir(path)if os.path.isfile(os.path.join(path,f))]
             for f in files :
                 print(open(path+"/%s"%(f)).read())
        elif choice == 2:
             path = directory+"/help/LogicalPartition"
             files = [f for f in os.listdir(path)if os.path.isfile(os.path.join(path,f))]
             for f in files :
                 print(open(path+"/%s"%(f)).read())
        elif choice == 3:
             path = directory+"/help/VirtualIOServer"
             files = [f for f in os.listdir(path)if os.path.isfile(os.path.join(path,f))]
             for f in files :
                 print(open(path+"/%s"%(f)).read())
        elif choice == 4:
             print(open(directory+"/help/Cluster.txt").read())
        elif choice == 5:
             print(open(directory+"/help/PerformanceCapacityMonitoring.txt").read())
        elif choice == 6:
             cls()
             return
        else:
            print("\nTry using Valid option")
            back_to_menu()

def cls():
    os.system( 'cls' if os.name=='nt' else 'clear' )

def back_to_menu():
    print("\nPress ENTER to Proceed ")
    getch.getch()
    cls()
