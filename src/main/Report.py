from src.main.HmcRestClient import *
from src.managed_system import ListManagedSystem
from src.logical_partition import ListLogicalPartition
import sys
import os
from src.managed_system.ManagedSystem import ManagedSystem
from src.logical_partition.LogicalPartition import LogicalPartition
directory = os.path.dirname(os.path.dirname(__file__))
from src.utility.ExcelUtil import ExcelUtil
def report_children(credentials):
    cls()
    ip = str(credentials.ip)
    logon_obj = LogonRequest.Logon()
    ip_temp, x_api_session = logon_obj.LogonRequest(credentials.ip,credentials.username,credentials.password)

    while True:
        print("\n\n", "Report Operations".center(50))
        print_list = ['Popullate database', 'Generate Report',
                      'Return to ManagedSystem Menu',
                      'Return to MainMenu', 'Help', 'Exit']
        # select any managed system operation
        x = int(print_obj.print_on_screen(print_list))
        if x == 1:
            cls()
            popullate_database( credentials.name, ip, x_api_session )
        elif x== 2:
            cls()
            generate_report(credentials.name)
        elif x == 5:
            cls()
            return True
        elif x == 6:
            cls()
            return False
        elif x == 7:
            print(open(directory + "/help/Report/ReportOptions.txt").read())
        elif x == 8:
            sys.exit(1)
        else:
            print("\nTry again using valid option")
            back_to_menu()

def generate_report( name ):
    CPU = 0
    S_CPU = 1
    MEM = 2
    cliente = {}
    for i in ManagedSystem.select().where(ManagedSystem.associated_hmc==name):

        for j in i:
            # verificar!!!! Id almacenado en lpar de associated con el id de managed system
            for k in LogicalPartition.select().where(LogicalPartition.associated_managed_system==j.id):
                kname = extract_client( k.name )
                if kname not in cliente:
                    cliente[kname] = [0.0,0.0,0.0]
                cliente[kname][CPU] += k.desired_processors
                cliente[kname][S_CPU] += k.desired_processing_units
                cliente[kname][MEM] += k.desired_memory
    write2excel = ExcelUtil()
    head_index = []
    head_column = ["DEDICATED CPU","SHARED CPU","MEMORY"]
    data_column = []
    for i in cliente.keys():
        head_index.append(i)
        data_column.append(cliente[i])
    write2excel.add( head_index,head_column,data_column,name)
    write2excel.writeExcel()
    print("Report generated in ",write2excel.file_path," as ",write2excel.file_name)


def extract_client(self, lpar):
    domain_list = ["co", "com", "local"]
    name = None
    for i in lpar.name.split(".")[1:]:
        if i.strip() not in domain_list:
            name = i.strip().lower()
    return name if name is not None else "No client"


def popullate_database( name, ip, x_api_session ):
    #db = SqliteDatabase('/home/afcastel/database.sql')
    #db.connect()
    if not ManagedSystem.table_exists():
        ManagedSystem.create_table()
    else:
        ManagedSystem.drop_table()
        ManagedSystem.create_table()

    managedsystem_object = ListManagedSystem.ListManagedSystem()
    object_list = managedsystem_object.list_ManagedSystem(ip, x_api_session)
    print( object_list )
    print("Start object list")
    for i in range(0, len(object_list)):
        ManagedSystem.create(id=object_list[i].Metadata.Atom.AtomID.value(),
                                       name=object_list[i].SystemName.value(),
                                       machine_type=object_list[i].MachineTypeModelAndSerialNumber.MachineType.value(),
                                       model=object_list[i].MachineTypeModelAndSerialNumber.Model.value(),
                                       associated_hmc=name
                                       )
    for i in ManagedSystem.select():
        logicalpartition_object = ListLogicalPartition.ListLogicalPartition()
        lpar_object_list = logicalpartition_object.list_LogicalPartition(ip, i.Metadata.Atom.AtomID.value(), x_api_session)
        for j in lpar_object_list:
            if j.HasDedicatedProcessors.value():
                LogicalPartition.create(id=j.PartitionID.value(),
                                        name=j.PartitionName.value(),
                                        type=j.PartitionType.value(),
                                        state=j.PartitionState.value(),
                                        uuid=j.PartitionUUID.value(),
                                        associated_managed_system=j.AssociatedManagedSystem.href,
                                        maximum_memory=j.MaximumMemory.value(),
                                        desired_memory=j.DesiredMemory.value(),
                                        minimum_memory=j.MinimumMemory.value(),
                                        has_dedicated_processors=j.HasDedicatedProcessors.value(),
                                        maximum_processors=j.PartitionProcessorConfiguration.DedicatedProcessorConfiguration.MaximumProcessors.value(),
                                        desired_processors=j.PartitionProcessorConfiguration.DedicatedProcessorConfiguration.DesiredProcessors.value(),
                                        minimum_processors=j.PartitionProcessorConfiguration.DedicatedProcessorConfiguration.MinimumProcessors.value(),
                                        maximum_processing_units=0,
                                        desired_processing_units=0,
                                        minimum_processing_units=0
                                        )
            else:
                LogicalPartition.create(id=j.PartitionID.value(),
                                        name=j.PartitionName.value(),
                                        type=j.PartitionType.value(),
                                        state=j.PartitionState.value(),
                                        uuid=j.PartitionUUID.value(),
                                        associated_managed_system=j.AssociatedManagedSystem.href,
                                        maximum_memory=j.MaximumMemory.value(),
                                        desired_memory=j.DesiredMemory.value(),
                                        minimum_memory=j.MinimumMemory.value(),
                                        has_dedicated_processors=j.HasDedicatedProcessors.value(),
                                        maximum_processors=0,
                                        desired_processors=0,
                                        minimum_processors=0,
                                        maximum_processing_units=j.PartitionProcessorConfiguration.SharedProcessorConfiguration.MaximumProcessingUnits.value(),
                                        desired_processing_units=j.PartitionProcessorConfiguration.SharedProcessorConfiguration.DesiredProcessingUnits.value(),
                                        minimum_processing_units=j.PartitionProcessorConfiguration.SharedProcessorConfiguration.MinimumProcessingUnits.value()
                                        )
    """
    try:
        print("Start object list")
        for i in range(0, len(object_list)):
            managed_object = ManagedSystem(id=object_list[i].Metadata.Atom.AtomID.value(),name=object_list[i].SystemName.value(),
                                           machine_type=object_list[i].MachineTypeModelAndSerialNumber.MachineType.value(),
                                           model=object_list[i].MachineTypeModelAndSerialNumber.Model.value(),
                                           associated_hmc=name
                                           )
            print( managed_object )
            managed_object.save()


        else:
            print("\nTry again using valid option")
    except (TypeError, AttributeError, IndexError):
        log_object.log_warn("No ManagedSystems available ")

    1. Get Managed Systems list
    2. Get Logical Partitions from Managed Systems list

    """
    for i in ManagedSystem.select():
        print(i.name,i.id)

    for i in LogicalPartition.select():
        print(i.name, i.associated_managed_system)