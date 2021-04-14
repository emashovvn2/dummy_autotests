import win32com.client
import pytest
import EventLogWorker
from time import sleep as sleep
from shutil import copyfile as cf
import win32serviceutil

ics = win32com.client.Dispatch("InfinitySecurity.Security")


def sec_file_change(source):
    cf(source, r'C:\Program Files (x86)\EleSy\SCADA Infinity\InfinityClientSecurity\security.isam')
    win32serviceutil.StopService('InfinitySecurityServer')
    sleep(5)
    win32serviceutil.StartService('InfinitySecurityServer')
    sleep(15)
    global ics
    ics = win32com.client.Dispatch("InfinitySecurity.Security")
    sleep(2)


@pytest.fixture
def resetDB_unregUser():
    sec_file_change(r'ICS\origin.isam')
    #if (ics.GetUserName() != "test_1"):
    #    ics.UserLogon("test_1", "123")
    #if (ics.GetUserName() != "test_1"):
    #    ics.UserLogoff()
    #ics.SetOriginalDB()
    ics.UserLogoff()
    
@pytest.fixture
def clear_infinty_audit():
    EventLogWorker.clear_log(logtype = "InfinityAudit", server = 'localhost')

@pytest.mark.skip(reason='Разобавться с вызовом ISecurityAdit')
def test_audit_func(clear_infinty_audit):
    aud = win32com.client.Dispatch("ISecurityAdit")
    #for i in range(5):
    #    ics.Audit("Prog" +i, i + "_User", "Act_" + i, i)
    aud.ISecurityAdit.Audit("q","w","e","5567")
    assert EventLogWorker.find_event_by_ID("ics_1160_1") == True
    
@pytest.mark.skip
def test_qwe():
    sec_file_change(r'ICS\test_1_2_3_block_test.isam')
    pass

def test_load_default_DB(clear_infinty_audit, resetDB_unregUser):
    assert ics.SetOriginalDB() == True
    assert EventLogWorker.find_event_by_ID("ics_1050") == True
    


def test_save_DB(clear_infinty_audit):
    assert ics.SaveConfig() == True
    assert EventLogWorker.find_event_by_ID("ics_1160_1") == True
    
def test_role_0_success(clear_infinty_audit):
    assert ics.Role() == 0

def test_empty_GetUserList_success(clear_infinty_audit):
    assert ics.GetUserList() == (1,("Незарегистрированный",))

def test_add_user_test100_failure(clear_infinty_audit):
    assert ics.AddUser("test_100","") == False
    assert EventLogWorker.find_event_by_ID("ics_1114") == True

def test_delete_user_test100_failed(clear_infinty_audit):
    assert ics.DeleteUser("test_100") == False
    assert EventLogWorker.find_event_by_ID("ics_1118") == True

def test_delete_user_test100_to_group_failed(clear_infinty_audit):
    assert ics.AddUserGroup("test_100","Администраторы") == False
    assert EventLogWorker.find_event_by_ID("ics_1100") == True

def test_add_user_test_1_success_1(clear_infinty_audit):
    assert ics.AddUser("test_1","") == True
    assert EventLogWorker.find_event_by_ID("ics_1027_2") == True
    
def test_add_user_test_1_failed(clear_infinty_audit):
    assert ics.AddUser("test_1","") == False
    assert EventLogWorker.find_event_by_ID("ics_1113") == True

def test_add_user_test_1_to_group_failed(clear_infinty_audit):
    assert ics.AddUserGroup("test_1","Админы") == False
    assert EventLogWorker.find_event_by_ID("ics_1101") == True

def test_add_user_test_1_to_admins_success(clear_infinty_audit):
    assert ics.AddUserGroup("test_1","Администраторы") == True
    assert EventLogWorker.find_event_by_ID("ics_1018_1") == True

def test_add_user_test_1_to_admins_failure(clear_infinty_audit):
    assert ics.AddUserGroup("test_1","Администраторы") == False
    assert EventLogWorker.find_event_by_ID("ics_1102") == True

def test_delete_user_test_100_from_group_failed(clear_infinty_audit):
    assert ics.DeleteUserGroup("test_100","Администраторы") == False
    assert EventLogWorker.find_event_by_ID("ics_1104") == True

def test_delete_user_test_1_from_group_failed(clear_infinty_audit):
    assert ics.DeleteUserGroup("test_1","Админы") == False
    assert EventLogWorker.find_event_by_ID("ics_1105") == True

def test_empty_GetUserList2_success(clear_infinty_audit):
    ics.SaveConfig()
    assert ics.GetUserList() == (1,("test_1",))

def test_delete_user_test_1_from_group_success(clear_infinty_audit):
    assert ics.DeleteUserGroup("test_1","Администраторы") == False
    assert EventLogWorker.find_event_by_ID("ics_1103") == True
    #ics.SaveConfig()

def test_add_user_test_1_success_2(clear_infinty_audit, resetDB_unregUser):
    #sleep(5)
    assert ics.AddUser("test_1","") == True
    assert EventLogWorker.find_event_by_ID("ics_1027_2") == True
    #sleep(5)
    assert ics.AddUserGroup("test_1","Администраторы") == True
    assert EventLogWorker.find_event_by_ID("ics_1018_1") == True
    #ics.SaveConfig()
    
    
#@pytest.mark.skip    
def test_add_user_test_2_success(clear_infinty_audit):
    assert ics.AddUser("test_2","") == True
    assert EventLogWorker.find_event_by_ID("ics_1027_3") == True
    #assert ics.GetUserList() == (2,("test_1","test_2",))
    
#@pytest.mark.skip
def test_add_user_test_3_success(clear_infinty_audit):
    assert ics.AddUser("test_3","") == True
    assert EventLogWorker.find_event_by_ID("ics_1027_4") == True
    ics.SaveConfig()
    assert ics.GetUserList() == (3,("test_1","test_2","test_3",))
    ics.UserLogon("test_1","123")
    
def test_delete_user_test_3_success(clear_infinty_audit):
    #ics.UserLogon("test_1","123")
    assert ics.DeleteUser("test_3") == True
    assert EventLogWorker.find_event_by_ID("ics_1028") == True
    ics.SaveConfig()
    assert ics.GetUserList() == (2,("test_1","test_2",))
    
def test_check_user_test_1_success(clear_infinty_audit):
    assert ics.CheckUser("test_1","123") == True

def test_check_user_test_1_failure(clear_infinty_audit):
    assert ics.CheckUser("test_1","1234") == False

def test_check_user_test_3_success(clear_infinty_audit):
    assert ics.CheckUser("test_3","123") == True

def test_check_user_test_3_failure(clear_infinty_audit):
    assert ics.CheckUser("test_3","1234") == False
    
def test_get_user_rights_test_1_trends_success(clear_infinty_audit):
    #ics.UserLogon("test_1","123")
    assert ics.GetUserRights("TREND_START","") == True

def test_get_user_rights_test_1_trends_failure(clear_infinty_audit):
    #ics.UserLogon("test_1","123")
    assert ics.GetUserRights("TREND_START_qwe","") == False
    
def test_get_user_rights_test_1_trends_with_condition_success(clear_infinty_audit):
    #ics.UserLogon("test_1","123")
    assert ics.GetUserRights("TREND_TAG","*") == True

def test_get_user_rights_test_1_trends_with_condition_failure(clear_infinty_audit):
    #ics.UserLogon("test_1","123")
    assert ics.GetUserRights("TREND_TAG","qwe") == False
    

def test_get_user_rights_test_2_trends_with_condition_failure(clear_infinty_audit):
    #ics.UserLogon("test_1","123")
    assert ics.GetUserRights("TREND_TAG","") == False
    
    
@pytest.mark.skip
def test_delete_all_users(clear_infinty_audit):
    assert ics.DeleteAllUsers() == True
    ics.SaveConfig()