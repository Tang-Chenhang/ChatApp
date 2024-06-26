import bcrypt
import time

class Utils:
    def is_valid_username(username):
        '''用户名合法性检测：
        检查用户名长度和字符范围
        用户名长度3-20，以字母起始，仅允许包括可打印的ascii字符
        返回布尔值以及一个报错信息,可以根据这些信息给出对应的处理或者反馈
        '''
        minlen = 3
        maxlen = 20
        if len(username) < minlen:
            return False, 'Username is too short'
        elif len(username) > maxlen:
            return False, 'Username is too long'
        if not username[0].isalpha():
            return False, 'The first character of username should be a letter'
        if not all(ord(char) >= 32 and ord(char) < 127 for char in username):
            return False, 'Username has invald characters'
        return True, 'OK'
    
    def hash_password(password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')
    
    def is_valid_password(password):
        minlen = 3
        maxlen = 16
        if len(password) < minlen:
            return False, 'Password is too short'
        elif len(password) > maxlen:
            return False, 'Password is too long'
        return True, 'OK'
    
    def is_valid_username_then_password(username, password):
        success, message = Utils.is_valid_username(username)
        if success:
            success, message = Utils.is_valid_password(password)
        return success, message 

class MessageBuilder:
    
    # 生成响应信息
    @staticmethod
    def build_response(success, message):
        message_data = {
                'type': 'response',
                'success': success,
                'message': message
            }
        return message_data
    
    # 生成心跳包
    @staticmethod
    def build_heartbeat(who):
        message_data = {
                'type': 'heartbeat',
                'who': who,
                'timestamp': time.time()
            }
        return message_data
    
    # region 生成请求消息
    # 根据请求内容生成请求
    @staticmethod
    def __build_request(action, request_data):
        message_data = {
                'type': 'request',
                'action': action,
                'request_data': request_data
            }
        return message_data
    
    # 根据请求类型地不同生成不同的请求内容对象，然后生成请求信息，下同
    @staticmethod
    def build_login_request(username, password):
        request_data = {
            'username' : username,
            'password' : password
        }
        return MessageBuilder.__build_request('login', request_data)
    
    @staticmethod
    def build_register_request(username, password):
        request_data = {
            'username' : username,
            'password' : password
        }
        return MessageBuilder.__build_request('register', request_data)
    
    @staticmethod
    def build_delete_request(username, password):
        request_data = {
            'username' : username,
            'password' : password
        }
        return MessageBuilder.__build_request('delete', request_data)
    
    @staticmethod
    def build_send_personal_message_request(sender, receiver, content):
        message_data = {
            'type' : 'personal_message',
            'sender': sender,
            'receiver' : receiver,
            'content' : content,
            'timestamp' : time.time()
        }
        return MessageBuilder.__build_request('send_personal_message', message_data)
    
    @staticmethod
    def build_send_group_message_request(sender, group, content):
        message_data = {
            'type' : 'group_message',
            'sender': sender,
            'group' : group,
            'content' : content,
            'timestamp' : time.time()
        }
        return MessageBuilder.__build_request('send_group_messager', message_data)
    # endregion