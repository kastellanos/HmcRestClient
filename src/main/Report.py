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
            back_to_menu()
        elif x== 2:
            cls()
            generate_report(credentials.name)
            back_to_menu()
        elif x == 5:
            cls()
            return True
        elif x == 6:
            cls()
            sys.exit(1)
        elif x == 7:
            print(open(directory + "/help/Report/ReportOptions.txt").read())
        elif x == 8:
            sys.exit(1)
        else:
            print("\nTry again using valid option")
            back_to_menu()

def generate_report( name ):
    path = None
    filen= None
    while True:
        path = input("Ingrese la ruta para guardar el archivo : ")
        filen = input("Ingrese el nombre del archivo : ")
        if path is not None and filen is not None:
            break;
        else:
            cls()
            print("**Ingrese datos validos**")
    if path[len(path)-1]=="/":
        #Do nothing
        pass
    else:
        path +="/"
    filen +=".xlsx"
    CPU = 0
    S_CPU = 1
    MEM = 2
    cliente = {}
    valid_state = ["running"]
    sum_total = [0.0,0.0,0.0]
    for i in ManagedSystem.select().where(ManagedSystem.associated_hmc==name):
        # verificar!!!! Id almacenado en lpar de associated con el id de managed system
        for k in LogicalPartition.select().where(LogicalPartition.associated_managed_system==i.id):
            if k.state in valid_state:
                kname = extract_client( k )
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
        sum_total[CPU]+= cliente[i][CPU]
        sum_total[MEM] += cliente[i][MEM]
        sum_total[S_CPU] += cliente[i][S_CPU]
    data_column.append(sum_total)
    head_index.append("Suma total")
    write2excel.add( head_index,head_column,data_column,name)
    write2excel.writeExcel(file_path=path,file_name=filen)
    print("Report generated in ",write2excel.file_path," as ",write2excel.file_name)


def extract_client(lpar):
    domain_list = ["co", "com", "local","org"]
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
    if not LogicalPartition.table_exists():
        LogicalPartition.create_table()
    else:
        LogicalPartition.drop_table()
        LogicalPartition.create_table()
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

    ms_list = ManagedSystem.select()
    for i in ms_list:

        logicalpartition_object = ListLogicalPartition.ListLogicalPartition()
        lpar_object_list = logicalpartition_object.list_LogicalPartition(ip, i.id, x_api_session)
        if lpar_object_list is not None:
            for j in lpar_object_list:
                lpar_cpu = j.PartitionProcessorConfiguration.HasDedicatedProcessors.value()
                if lpar_cpu:
                    uuidMS = j.AssociatedManagedSystem.href.split('/')
                    print( uuidMS)
                    LogicalPartition.create(id=j.PartitionID.value(),
                                            name=j.PartitionName.value(),
                                            type=j.PartitionType.value(),
                                            state=j.PartitionState.value(),
                                            uuid=j.PartitionUUID.value(),
                                            associated_managed_system=uuidMS[len(uuidMS)-1],
                                            maximum_memory=j.PartitionMemoryConfiguration.MaximumMemory.value(),
                                            desired_memory=j.PartitionMemoryConfiguration.DesiredMemory.value(),
                                            minimum_memory=j.PartitionMemoryConfiguration.MinimumMemory.value(),
                                            has_dedicated_processors=j.PartitionProcessorConfiguration.HasDedicatedProcessors.value(),
                                            maximum_processors=j.PartitionProcessorConfiguration.DedicatedProcessorConfiguration.MaximumProcessors.value(),
                                            desired_processors=j.PartitionProcessorConfiguration.DedicatedProcessorConfiguration.DesiredProcessors.value(),
                                            minimum_processors=j.PartitionProcessorConfiguration.DedicatedProcessorConfiguration.MinimumProcessors.value(),
                                            maximum_processing_units=0,
                                            desired_processing_units=0,
                                            minimum_processing_units=0
                                            )

                else:
                    uuidMS = j.AssociatedManagedSystem.href.split('/')
                    print(uuidMS)
                    LogicalPartition.create(id=j.PartitionID.value(),
                                            name=j.PartitionName.value(),
                                            type=j.PartitionType.value(),
                                            state=j.PartitionState.value(),
                                            uuid=j.PartitionUUID.value(),
                                            associated_managed_system=uuidMS[len(uuidMS)-1],
                                            maximum_memory=j.PartitionMemoryConfiguration.MaximumMemory.value(),
                                            desired_memory=j.PartitionMemoryConfiguration.DesiredMemory.value(),
                                            minimum_memory=j.PartitionMemoryConfiguration.MinimumMemory.value(),
                                            has_dedicated_processors=j.PartitionProcessorConfiguration.HasDedicatedProcessors.value(),
                                            maximum_processors=0,
                                            desired_processors=0,
                                            minimum_processors=0,
                                            maximum_processing_units=j.PartitionProcessorConfiguration.SharedProcessorConfiguration.MaximumProcessingUnits.value(),
                                            desired_processing_units=j.PartitionProcessorConfiguration.SharedProcessorConfiguration.DesiredProcessingUnits.value(),
                                            minimum_processing_units=j.PartitionProcessorConfiguration.SharedProcessorConfiguration.MinimumProcessingUnits.value()
                                            )



    for i in ManagedSystem.select():
        print(i.name,i.id)

    for i in LogicalPartition.select():
        print(i.name, i.associated_managed_system)