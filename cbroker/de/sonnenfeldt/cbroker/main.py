'''
Created on 15 Nov 2015

@author: rudi
'''
from sqlite3.dbapi2 import paramstyle

if __name__ == '__main__':
    pass


from Numberjack import *
from de.sonnenfeldt.cbroker.Container import Container
import pandas as pd
from pandas import DataFrame


def get_host_requirements():
    c = Container()
    c.assign_cpus(2)
    c.assign_memory(4)
    c.assign_disk_size(0)
    c.assign_disk_type(c.DISK_TYPES.index("HDD"))
    c.assign_regions(c.REGIONS.index("Germany"))
    c.assign_compute_optimized(c.IS_OPTIMIZED.index("no"))
    c.assign_memory_optimized(c.IS_OPTIMIZED.index("no"))
    c.assign_storage_optimized(c.IS_OPTIMIZED.index("no"))
    c.assign_host_type(c.HOST_TYPES.index("virtual"))
    c.assign_environment_type(c.ENVIRONMENT_TYPES.index("prod"))
    c.assign_ha_scale(1)
    c.assign_dr_scale(1)
    c.assign_price_limit(100)
    
    print c
    
    return c
    
    
    
def get_hosts():
    csv_file = "./hosts.csv"
    print "Hosts input file: %s" % csv_file

    hosts_raw = pd.read_csv(csv_file, sep=',', names=['#', 'Provider', 'Region', 'CPUs', 'Memory', 
                                                  'Storage', 'DiskType', 'OS', 'Cost','Comment'])

    hosts = DataFrame(hosts_raw)
    hosts = hosts[1:]
    hosts = hosts.convert_objects(convert_numeric=True)
    
    print hosts
    
    return hosts


def AND(b1, b2, b3, b4, b5, b6, b7, b8, b9):
    return (b1 & b2 & b3 & b4 & b5 & b6 & b7 & b8 & b9)

def OR(b1, b2):
    return (b1 | b2)

def compute_host(param):

    c = get_host_requirements()
    h = get_hosts()
    
    # define the variables with their domains
    host = Variable(0, len(h)-1,"host")
    provider = Variable(0,len(c.PROVIDERS)-1, "provider")
    region = Variable(0,len(c.REGIONS)-1,"region")
    cpu = Variable(1,64,"cpu")
    memory = Variable(1,512,"memory")
    disk_size = Variable(0,1024,"disk_size")
    disk_type = Variable(0,len(c.DISK_TYPES)-1,"disk_type")    
    os_type = Variable(0,len(c.OS_TYPES)-1, "os_type")
    cost = Variable(1,999999,"cost")

    model = Model()
    
    or_expr = False
    # add hosts to model    
    for index,row in h.iterrows():
        and_expr = AND(host == int(row['#']), 
                       provider == int(row['Provider']),
                       region == int(row['Region']),
                       cpu == int(row['CPUs']),
                       memory == int(row['Memory']),
                       disk_size == int(row['Storage']),
                       disk_type == int(row['DiskType']),  
                       os_type == int(row['OS']),
                       cost == int(row['Cost']))
        or_expr = OR(or_expr, and_expr)
 
    model.add(or_expr)

#        model.add(imply(host == int(row['#']), provider == int(row['Provider'])))
#        model.add(imply(host == int(row['#']), region == int(row['Region'])))
#        model.add(imply(host == int(row['#']), cpu == int(row['CPUs'])))
#        model.add(imply(host == int(row['#']), memory == int(row['Memory'])))
#        model.add(imply(host == int(row['#']), disk_size == int(row['Storage'])))
#        model.add(imply(host == int(row['#']), disk_type == int(row['DiskType'])))  
#        model.add(imply(host == int(row['#']), os_type == int(row['OS'])))
#        model.add(imply(host == int(row['#']), cost == int(row['Cost'])))       
           
    # add constraints to match 
    
    model.add([region == r for r in c.get_regions()])
    model.add(cpu >= c.get_cpus())
    model.add(memory >= c.get_memory())
    model.add(disk_size >= c.get_disk_size())
    model.add(disk_type == c.get_disk_type())

    budget = cost

    model.add(Minimise(budget))

    # search for solutions
    print model
    
    solver = model.load(param['solver'])
    solver.setVerbosity(1)
    
    if solver.solve():
        solver.printStatistics()
        number_solutions = 1
        print "provider = ", c.PROVIDERS[provider.get_value()]
        print "region = ", c.REGIONS[region.get_value()]
        print "cpu = ", cpu.get_value()
        print "memory = ", memory.get_value()        
        print "cost = ", cost.get_value()
        
        while solver.getNextSolution() == SAT:
            print "provider = ", c.PROVIDERS[provider.get_value()]
            print "region = ", c.REGIONS[region.get_value()]
            print "cpu = ", cpu.get_value()
            print "memory = ", memory.get_value()
            print "cost = ", cost.get_value()            
            number_solutions += 1
        
        print "Number Solution: ", number_solutions
        print 'Nodes:', solver.getNodes(), ' Time:', solver.getTime()
    else:
        print "No solution"
    
compute_host(input({'solver':'Mistral'}))