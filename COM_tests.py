import win32com.client
import pytest
import EventLogWorker
from time import sleep as sleep
from shutil import copyfile as cf
import win32serviceutil


def sec_file_change(source):
    win32serviceutil.StopService('InfinitySecurityServer')
    sleep(1)
    cf(source, r'C:\Program Files (x86)\EleSy\SCADA Infinity\InfinityClientSecurity\security.isam')
    sleep(5)
    win32serviceutil.StartService('InfinitySecurityServer')
    sleep(25)

@pytest.fixture
def get_ics_connect():
    return win32com.client.Dispatch("InfinitySecurity.Security")

    
@pytest.fixture
def resetDB_unregUser():
    sec_file_change(r'ICS\origin.isam')
    
@pytest.fixture
def clear_infinty_audit():
    pass
    #EventLogWorker.clear_log(logtype = "InfinityAudit", server = 'localhost')

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

def test_load_default_DB(resetDB_unregUser, clear_infinty_audit, get_ics_connect):
    assert get_ics_connect.SetOriginalDB() == True
    assert EventLogWorker.find_event_by_ID("ics_1050") == True
    
def test_get_user_name_unreg(get_ics_connect):
    assert get_ics_connect.GetUserName() == 'Незарегистрированный'
    
def test_save_DB(clear_infinty_audit, get_ics_connect):
    assert get_ics_connect.SaveConfig() == True
    assert EventLogWorker.find_event_by_ID("ics_1160_1") == True
    
def test_role_0_success(clear_infinty_audit, get_ics_connect):
    assert get_ics_connect.Role() == 0

def test_empty_GetUserList_success(clear_infinty_audit, get_ics_connect):
    assert get_ics_connect.GetUserList() == (1,("Незарегистрированный",))

def test_add_user_test100_failure(clear_infinty_audit, get_ics_connect):
    assert get_ics_connect.AddUser("test_100","") == False
    assert EventLogWorker.find_event_by_ID("ics_1114") == True

def test_delete_user_test100_failed(clear_infinty_audit, get_ics_connect):
    assert get_ics_connect.DeleteUser("test_100") == False
    assert EventLogWorker.find_event_by_ID("ics_1118") == True

def test_delete_user_test100_to_group_failed(clear_infinty_audit, get_ics_connect):
    assert get_ics_connect.AddUserGroup("test_100","Администраторы") == False
    assert EventLogWorker.find_event_by_ID("ics_1100") == True

def test_add_user_test_1_success_1(clear_infinty_audit, get_ics_connect):
    assert get_ics_connect.AddUser("test_1","") == True
    assert EventLogWorker.find_event_by_ID("ics_1027_2") == True
    
def test_add_user_test_1_failed(clear_infinty_audit, get_ics_connect):
    assert get_ics_connect.AddUser("test_1","") == False
    assert EventLogWorker.find_event_by_ID("ics_1113") == True

def test_add_user_test_1_to_group_failed(clear_infinty_audit, get_ics_connect):
    assert get_ics_connect.AddUserGroup("test_1","Админы") == False
    assert EventLogWorker.find_event_by_ID("ics_1101") == True

def test_add_user_test_1_to_admins_success(clear_infinty_audit, get_ics_connect):
    assert get_ics_connect.AddUserGroup("test_1","Администраторы") == True
    assert EventLogWorker.find_event_by_ID("ics_1018_1") == True

def test_add_user_test_1_to_admins_failure(clear_infinty_audit, get_ics_connect):
    assert get_ics_connect.AddUserGroup("test_1","Администраторы") == False
    assert EventLogWorker.find_event_by_ID("ics_1102") == True

def test_delete_user_test_100_from_group_failed(clear_infinty_audit, get_ics_connect):
    assert get_ics_connect.DeleteUserGroup("test_100","Администраторы") == False
    assert EventLogWorker.find_event_by_ID("ics_1104") == True

def test_delete_user_test_1_from_group_failed(clear_infinty_audit, get_ics_connect):
    assert get_ics_connect.DeleteUserGroup("test_1","Админы") == False
    assert EventLogWorker.find_event_by_ID("ics_1105") == True

def test_empty_GetUserList2_success(clear_infinty_audit, get_ics_connect):
    get_ics_connect.SaveConfig()
    assert get_ics_connect.GetUserList() == (1,("test_1",))

def test_delete_user_test_1_from_group_success(clear_infinty_audit, get_ics_connect):
    assert get_ics_connect.DeleteUserGroup("test_1","Администраторы") == False
    assert EventLogWorker.find_event_by_ID("ics_1103") == True

def test_add_user_test_1_success_2(clear_infinty_audit, resetDB_unregUser, get_ics_connect):
    assert get_ics_connect.AddUser("test_1","") == True
    assert EventLogWorker.find_event_by_ID("ics_1027_2") == True
    assert get_ics_connect.AddUserGroup("test_1","Администраторы") == True
    assert EventLogWorker.find_event_by_ID("ics_1018_1") == True
    
#@pytest.mark.skip    
def test_add_user_test_2_success(clear_infinty_audit, get_ics_connect):
    assert get_ics_connect.AddUser("test_2","") == True
    assert EventLogWorker.find_event_by_ID("ics_1027_3") == True
    
#@pytest.mark.skip
def test_add_user_test_3_success(clear_infinty_audit, get_ics_connect):
    assert get_ics_connect.AddUser("test_3","") == True
    assert EventLogWorker.find_event_by_ID("ics_1027_4") == True
    get_ics_connect.SaveConfig()
    assert get_ics_connect.GetUserList() == (3,("test_1","test_2","test_3",))
    assert get_ics_connect.UserLogon("test_1","123") == True
    #assert EventLogWorker.find_event_by_ID("ics_1160_2") == True
    
def test_get_user_name_test_1(get_ics_connect):
    assert get_ics_connect.GetUserName() == 'test_1'

def test_login_current_user_success(clear_infinty_audit, get_ics_connect):
    try:
        get_ics_connect.UserLogon("test_1","123")
    except:
        pass
    assert EventLogWorker.find_event_by_ID("ics_1061") == True 
    
def test_delete_user_test_3_success(clear_infinty_audit, get_ics_connect):
    assert get_ics_connect.DeleteUser("test_3") == True
    assert EventLogWorker.find_event_by_ID("ics_1028") == True
    get_ics_connect.SaveConfig()
    assert get_ics_connect.GetUserList() == (2,("test_1","test_2",))
        
def test_check_user_test_1_success(clear_infinty_audit, get_ics_connect):
    assert get_ics_connect.CheckUser("test_1","123") == True

def test_check_user_test_1_failure(clear_infinty_audit, get_ics_connect):
    assert get_ics_connect.CheckUser("test_1","1234") == False

def test_check_user_test_3_success(clear_infinty_audit, get_ics_connect):
    assert get_ics_connect.CheckUser("test_3","123") == True

def test_check_user_test_3_failure(clear_infinty_audit, get_ics_connect):
    assert get_ics_connect.CheckUser("test_3","1234") == False
    
def test_get_user_rights_test_1_trends_success(clear_infinty_audit, get_ics_connect):
    assert get_ics_connect.GetUserRights("TREND_START","") == True

def test_get_user_rights_test_1_trends_failure(clear_infinty_audit, get_ics_connect):
    assert get_ics_connect.GetUserRights("TREND_START_qwe","") == False
    
def test_get_user_rights_test_1_trends_with_condition_success(clear_infinty_audit, get_ics_connect):
    assert get_ics_connect.GetUserRights("TREND_TAG","*") == True

def test_get_user_rights_test_1_trends_with_condition_failure(clear_infinty_audit, get_ics_connect):
    assert get_ics_connect.GetUserRights("TREND_TAG","qwe") == True
    
def test_get_user_rights_test_2_trends_with_condition_failure(clear_infinty_audit, get_ics_connect):
    assert get_ics_connect.GetUserRights("TREND_TAG","") == True

def test_wrong_password_success(clear_infinty_audit, get_ics_connect):
    try:
        get_ics_connect.UserLogon("test_2","1234")
    except:
        pass
    assert EventLogWorker.find_event_by_ID("ics_1022") == True    
    
def test_wrong_user_failure(clear_infinty_audit, get_ics_connect):
    try:
        get_ics_connect.UserLogon("test_222","123")
    except:
        pass
    assert EventLogWorker.find_event_by_ID("ics_1022") == True 
    assert EventLogWorker.find_event_by_ID("ics_1060") == True
    
@pytest.mark.skip
def test_delete_all_users(clear_infinty_audit, get_ics_connect):
    assert get_ics_connect.DeleteAllUsers() == True
    get_ics_connect.SaveConfig()

def test_list_blocked_users_success(get_ics_connect):
    sec_file_change(r'ICS\test_1_2_3_user_1_2_block_test.isam')
    get_ics_connect.UserLogon("test_1","123")
    
def test_list_groups_success(get_ics_connect):
    assert get_ics_connect.GetGroupList() == (3,("Администраторы","Test","Блокированные",))
    
def test_list_users_in_group_Test_success(get_ics_connect):
    assert get_ics_connect.GetGroupUsers("Test") == (2,("test_2","test_3",))
    
def test_list_users_in_group_Blocked_success(get_ics_connect):
    assert get_ics_connect.GetGroupUsers("Блокированные") == (0,("",))
   
def test_list_users_in_group_Administrators_success(get_ics_connect):
    assert get_ics_connect.GetGroupUsers("Администраторы") == (1,("test_1",))
    
def test_list_blocked_users_success_2(get_ics_connect):
    assert get_ics_connect.GetBlockedUserList() == (2,("user_1","user_2",))
    
@pytest.mark.skip    
def test_qq(get_ics_connect):
    assert get_ics_connect.GetBlockedUserList() == (1,("test_2",))
