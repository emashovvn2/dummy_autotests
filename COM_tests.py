import win32com.client
import pytest
import EventLogWorker

ics = win32com.client.Dispatch("InfinitySecurity.Security")

@pytest.fixture
def clear_infinty_audit():
    EventLogWorker.clear_log(logtype = "InfinityAudit", server = 'localhost')
    
def test_load_default_DB(clear_infinty_audit):
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

def test_add_user_test_1_success(clear_infinty_audit):
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
