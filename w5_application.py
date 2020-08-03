# Mike Colbert
# 08/01/2020
# week 5

'''
I used three design patterns in my assignment.

A Singleton pattern was used to create a logger that logs to the command line and to the file system. After first run,
the log file can be found in the log folder which is in the same directory as this application file.

A Facade pattern was used to create a faux database connection. In Main() you can see where I connect to the database,
take an action, then close the database connection using the Facade.

The Factory pattern was used in two places. First to create the different types of leave requests (vacation, sick, or unpaid).
I also used this pattern to create employees, managers, and hr personel who have differing responsibilites with each leave request.

My driver application Main() is using comments and print statements to document what is happening as it demonstrates application functionality.

'''


from datetime import datetime #used to calculate days
from abc import ABCMeta, abstractmethod  #used for factory pattern
import logging #used for logger
import os #used for logger


### Singleton pattern

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
        
class Logger(metaclass=Singleton):
    def __init__(self):
        self._logger = logging.getLogger("crumbs")
        self._logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s \t [%(levelname)s | %(filename)s:%(lineno)s] > %(message)s')

        now = datetime.now()
        dirname = "./log"

        if not os.path.isdir(dirname):
            os.mkdir(dirname)
        fileHandler = logging.FileHandler(dirname + "/log_" + now.strftime("%Y-%m-%d")+".log")

        streamHandler = logging.StreamHandler()

        fileHandler.setFormatter(formatter)
        streamHandler.setFormatter(formatter)

        self._logger.addHandler(fileHandler)
        self._logger.addHandler(streamHandler)

        print("Generate new instance")

    def get_logger(self):
        return self._logger


### Facade pattern
class DatabaseFacade():
    def __init__(self, dbname=None, host=None, user=None, password=None):
        self.dbname = "leave_management"
        self.host = "postgres_server_url"
        self.user = "myusername"
        self.password = "mypassword"

    def connect(self):
        return "create connection to the database"

    
    def close(self):
        return "close the connection to the database"



### Factory pattern

class LeaveRequest(metaclass=ABCMeta):
    def __init__(self, firstDayOfLeave, lastDayOfLeave, employee, manager): 
        self.firstDayOfLeave = firstDayOfLeave
        self.lastDayOfLeave = lastDayOfLeave
        self.employee = employee  #employee object
        self.manager = manager #manager object

    def countDaysOfLeave(self):
        format_string = "%m/%d/%Y"
        lastDayOfLeave = datetime.strptime(self.lastDayOfLeave, format_string)
        firstDayOfLeave = datetime.strptime(self.firstDayOfLeave, format_string)

        return ((lastDayOfLeave - firstDayOfLeave).days)
        
    
    def __repr__(self):
        return "LeaveRequest('{0}', '{1} \nEmployee:{2} \n Manager: {3}')".format(self.firstDayOfLeave, self.lastDayOfLeave, employee.getFullName(), manager.getEmail())


class VacationRequest(LeaveRequest):
    def __init__(self, firstDayOfLeave, lastDayOfLeave, employee, manager):
        super().__init__(firstDayOfLeave, lastDayOfLeave, employee, manager)  #references the class we have inhertited from - LeaveRequest super class
        self.requestApproved = False
        self.leaveType = 'vacation'
    
    def getRequestApproved(self):
        return self.requestApproved
    
    def setRequestApproved(self):
        self.requestApproved = True 
        
    def getLeaveType(self):
        return self.leaveType
    
    def useVacationDays(self):
        # deduct vacation days in this request from employee's total vacation days
        if self.getRequestApproved() == True:
            if self.employee.getVacationEligible() == True:
                if self.employee.getVacationDays() >= self.countDaysOfLeave():
                    self.employee.setVacationDays(self.employee.getVacationDays() - self.countDaysOfLeave())
                    print("{0} vacation days approved message sent to employee email {1}".format(self.countDaysOfLeave(), self.employee.getEmail()))  
                    return True
                return "Vacation days requested exceed vacation days accrued message sent to employee email {0}".format(self.employee.getEmail())
            return "Not yet eligible to use vacation days message sent to employee email {0}".format(self.employee.getEmail())
        return "Vacation days were not approved by your manager message sent to employee email {0}".format(employee.getEmail())
    
    
    def emailManager(self):
        return "Vacation request pending email sent to {0}".format(self.manager.getEmail())
        
        
    def __repr__(self):
        return "VacationRequest('{0}', '{1}', {2}, {3})".format(self.firstDayOfLeave, self.lastDayOfLeave, self.employee.getFullName(), self.manager.getEmail())
 
  
class SickRequest(LeaveRequest):
    def __init__(self, firstDayOfLeave, lastDayOfLeave, employee, manager):
        super().__init__(firstDayOfLeave, lastDayOfLeave, employee, manager)  #references the class we have inhertited from - LeaveRequest super class
        self.requestApproved = False
        self.leaveType = 'sick'
    
    def getRequestApproved(self):
        return self.requestApproved
    
    def setRequestApproved(self):
        self.requestApproved = True  # set to TRUE
    
    def getLeaveType(self):
        return self.leaveType
    
    def useSickDays(self):
       # deduct sick days in this request from employee's total sick days
        if self.getRequestApproved() == True:
            if self.employee.getSickDays() >= self.countDaysOfLeave():
                self.employee.setSickDays(self.employee.getSickDays() - self.countDaysOfLeave())
                print("{0} sick days approved message sent to employee email {1}".format(self.countDaysOfLeave(), self.employee.getEmail()))  
                return True
            return "Number of sick days requested exceeds number accrued message sent to employee email {0}".format(self.employee.getEmail())
        return "Sick days were not approved by your manager message sent to employee email {0}".format(self.employee.getEmail())
    
    def emailManager(self):
        return "Sick request pending email sent to {0}".format(self.manager.getEmail())

    
    def __repr__(self):
        return "SickRequest('{0}', '{1}', {2}, {3})".format(self.firstDayOfLeave, self.lastDayOfLeave, self.employee.getFullName(), self.manager.getEmail())
  

class UnpaidRequest(LeaveRequest):
    def __init__(self, firstDayOfLeave, lastDayOfLeave, employee, manager):
        super().__init__(firstDayOfLeave, lastDayOfLeave, employee, manager) #references the class we have inhertited from - LeaveRequest super class
        self.requestApproved = False 
        self.leaveType = 'unpaid'
    
    def getRequestApproved(self):
        return self.requestApproved
    
    def setRequestApproved(self):
        self.requestApproved = True
    
    def getLeaveType(self):
        return self.leaveType
    
    def useUnpaidDays(self):
        # add unpaid days in this request to employee's total unpaid days off
        if self.getRequestApproved() == True:
            self.employee.setUnpaidDays(self.countDaysOfLeave())
            print("{0} unpaid days approved message sent to employee email {1}".format(self.countDaysOfLeave(), self.employee.getEmail()))  
            return True
        return "Unpaid days were not approved by your manager message sent to employee email {0}".format(self.employee.getEmail())

    def emailManager(self):
        return "Unpaid leave request email sent to {0}".format(self.manager.getEmail())
        
    def __repr__(self):
        return "UnpaidRequest('{0}', '{1}', {2}, {3})".format(self.firstDayOfLeave, self.lastDayOfLeave, self.employee.getFullName(), self.manager.getEmail() )


class LeaveRequestFactory(object):
    @classmethod
    def create(cls, requestType, *args):
        requestType = requestType.lower().strip()

        if requestType == "vacation":
            return VacationRequest(*args)
        elif requestType == "sick":
            return SickRequest(*args)
        elif requestType == "unpaid":
            return UnpaidRequest(*args)



class Employee(metaclass=ABCMeta):
    #generic superclass
    def __init__(self, firstName, lastName, vacationLeave, vacationEligible, sickLeave, unpaidLeave): 
        self.accountType = "employee"
        self.firstName = firstName
        self.lastName = lastName
        self.vacationLeave = vacationLeave  #earned vacation leave
        self.vacationEligible = vacationEligible  #must be an employee for 6 months before using vacation
        self.sickLeave = sickLeave  #earned sick leave
        self.unpaidLeave = unpaidLeave  #quantitiy of unpaid leave taken by employee

    def getFullName(self):
        return self.firstName + " " + self.lastName
    
    def getEmail(self):
        return self.firstName + "." + self.lastName + "@company.corp"

    def getVacationDays(self):
        #get number of vacation days from employee class
        return self.vacationLeave
    
    def setVacationDays(self, days):
        self.vacationLeave = days
    
    def getVacationEligible(self):
        #get from employee class
        return self.vacationEligible
        
    def getSickDays(self):
        #get number of vacation days from employee class
        return self.sickLeave
    
    def setSickDays(self, days):
        self.sickLeave = days
        
    def getUnpaidDays(self):
        return self.unpaidLeave
    
    def setUnpaidDays(self, days):
        self.unpaidLeave = self.unpaidLeave + days
    
    def getAccountType(self):
        return self.accountType
    
    def __repr__(self):
        return "Employee('{0}', '{1}', {2}, {3}, {4}, {5})".format(self.firstName, self.lastName, self.vacationLeave, self.vacationEligible, self.sickLeave, self.unpaidLeave)


class Manager(Employee):
    #approves requests
    def __init__(self, firstName, lastName, vacationLeave, vacationEligible, sickLeave, unpaidLeave):
        super().__init__(firstName, lastName, vacationLeave, vacationEligible, sickLeave, unpaidLeave)
        self.accountType = "manager"
    
    def approveVacationLeave(self, vacation):
        vacation.setRequestApproved()
        
    def approveSickLeave(self, sick):
        sick.setRequestApproved()
        
    def approveUpaidLeave(self, unpaid):
        unpaid.setRequestApproved()

    #def getEmail(self):
     #   return self.firstName + "." + self.lastName + "@company.corp"


    def __repr__(self):
        return "Manager('{0}', '{1}', {2}, {3}, {4}, {5})".format(self.firstName, self.lastName, self.vacationLeave, self.vacationEligible, self.sickLeave, self.unpaidLeave)


class HR(Employee):
    #approves requests
    def __init__(self, firstName, lastName, vacationLeave, vacationEligible, sickLeave, unpaidLeave):
        super().__init__(firstName, lastName, vacationLeave, vacationEligible, sickLeave, unpaidLeave)
        self.accountType = "hr"
    
    #def getEmail(self):
        #return self.firstName + "." + self.lastName + "@company.corp"

    def setVacationEligible(self, employee):
        employee.vacationEligible = True

    def __repr__(self):
        return "HR('{0}', '{1}', {2}, {3}, {4}, {5})".format(self.firstName, self.lastName, self.vacationLeave, self.vacationEligible, self.sickLeave, self.unpaidLeave)


class EmployeeFactory(object):
    @classmethod
    def create(cls, requestType, *args):
        requestType = requestType.lower().strip()

        if requestType == "employee":
            return Employee(*args)
        elif requestType == "manager":
            return Manager(*args)
        elif requestType == "hr":
            return HR(*args)




def main():
    print("************** use Singleton to create a logger *******************")
    #Singleton
    logger1=Logger()
    print(logger1)
    
    logger2=Logger()
    print(logger2)

    #instantiate logger
    logger = Logger.__call__().get_logger()
    
    print("")
    print("")    
    print("************** instantiate the database using a Facade *******************")
    #Facade
    db = DatabaseFacade()
    
    
    print("")
    print("")    
    print("************** instantiate employee, manager, and hr *******************")
    #employee = Employee("Mike", "Colbert", 6, False, 7, 0) #instantiate an employee object -- vacationLeave, vacationEligible, sickLeave, unpaidLeave 
    #manager = Manager("Matt", "Colbert", 14, True, 10, 0)
    #hr = HR("Amy", "Colbert", 14, True, 10, 0)
    
    
    employeeFactory = EmployeeFactory() #instantiate an employee factory object
    
    employee = employeeFactory.create("employee", "Mike", "Colbert", 6, False, 7, 0) #instantiate a employee object using the factory
    manager = employeeFactory.create("manager", "Matt", "Colbert", 14, True, 10, 0)
    hr = employeeFactory.create("hr", "Amy", "Colbert", 14, True, 10, 0)
    
    
    print(employee)
    print(manager)
    print(hr)
    
    
    
    factory = LeaveRequestFactory() #instantiate a factory object
    
    print("")
    print("")    
    print("************** use Factory to create vacation request *******************")
    vacation = factory.create("vacation", "07/17/2020", "07/20/2020", employee, manager) #instantiate a vacation object using the factory
    
    print("")
    print("- - - - - - ")
    print(db.connect())  # save connect and close the database using the Facade pattern
    print("save the request to the database")
    print(db.close())
    print("- - - - - - ")
    print("")
    
    print(vacation)
    print("****************")
    
    print("The employee has been here 6 months and is eligible for vacation: {0}".format(employee.getVacationEligible()))
    hr.setVacationEligible(employee)
    print("The employee has now been here 6 months and is eligible for vacation: {0}".format(employee.getVacationEligible()))
    
    print("")
    print("- - - - - - ")
    print(db.connect())
    print("update the employee record in the database")
    print(db.close())
    print("- - - - - - ")
    print("")


    print(vacation.emailManager())
    print("The manager has approved the request: {0}".format(vacation.getRequestApproved()))
    manager.approveVacationLeave(vacation)
    print("The manager has approved the request: {0}".format(vacation.getRequestApproved()))
    
    print("")
    print("- - - - - - ")
    print(db.connect())
    print("mark the request as approved in the database")
    print(db.close())
    print("- - - - - - ")
    print("")
    

    print("vacation days used successfully: {0}".format(vacation.useVacationDays()))
    
    print("")
    print("- - - - - - ")
    print(db.connect())
    print("archive the request and modify the employee vacation day field")
    print(db.close())
    print("- - - - - - ")
    print("")
    
    print("vacation days remaining: {0}".format(employee.getVacationDays()))
    logger.info("vaction request for {0} was approved by {1}".format(employee.getFullName(), manager.getFullName()))  #log the request using the Singleton
    
    print("")
    print("")
    print("************** use factory to create sick leave request *******************")
    sick = factory.create("sick", "07/17/2020", "07/20/2020", employee, manager) #instantiate a vacation object using the factory
    
    print("")
    print("- - - - - - ")
    print(db.connect())
    print("save the request to the database")
    print(db.close())
    print("- - - - - - ")
    print("")
    
    print(sick)
    print("****************")
    
    print(sick.emailManager())
    print("The manager has approved the request: {0}".format(sick.getRequestApproved()))
    manager.approveSickLeave(sick)
    print("The manager has approved the request: {0}".format(sick.getRequestApproved()))
    
    print("")
    print("- - - - - - ")
    print(db.connect())
    print("mark the request as approved in the database")
    print(db.close())
    print("- - - - - - ")
    print("")
    

    print("sick days used successfully: {0}".format(sick.useSickDays()))
    
    print("")
    print("- - - - - - ")
    print(db.connect())
    print("archive the request and modify the employee sick day field")
    print(db.close())
    print("- - - - - - ")
    print("")
    
    print("sick days remaining: {0}".format(employee.getSickDays()))
    logger.info("sick day request for {0} was approved by {1}".format(employee.getFullName(), manager.getFullName()))
    
    print("")
    print("")
    print("************** use factory to create unpaid leave request *******************")
    unpaid = factory.create("unpaid", "07/17/2020", "07/20/2020", employee, manager) #instantiate a vacation object using the factory
    
    print("")
    print("- - - - - - ")
    print(db.connect())
    print("save the request to the database")
    print(db.close())
    print("- - - - - - ")
    print("")
    
    print(unpaid)
    print("****************")
    
    print(unpaid.emailManager())
    print("The manager has approved the request: {0}".format(unpaid.getRequestApproved()))
    manager.approveUpaidLeave(unpaid)
    print("The manager has approved the request: {0}".format(unpaid.getRequestApproved()))
    
    print("")
    print("- - - - - - ")
    print(db.connect())
    print("mark the request as approved in the database")
    print(db.close())
    print("- - - - - - ")
    print("")
    
    print("unpaid days used successfully: {0}".format(unpaid.useUnpaidDays()))
    
    print("")
    print("- - - - - - ")
    print(db.connect())
    print("archive the request and modify the employee unpaid day field")
    print(db.close())
    print("- - - - - - ")
    print("")
    
    print("unpaid days used: {0}".format(employee.getUnpaidDays()))
    logger.info("unpaid time off request for {0} was approved by {1}".format(employee.getFullName(), manager.getFullName()))




main()





