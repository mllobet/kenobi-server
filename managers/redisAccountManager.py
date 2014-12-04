import random
import redis

from accountManager import AccountManager

class RedisAccountManager(AccountManager):
    
    def __init__(self):
        self.r_server = redis.Redis('localhost')
        
    def get_uid(self, username):
        """ Gets uid of a given username, if no uid exists returns None"""
        uid = self.r_server.get(username)
        if uid is None:
            return None
        print "user: {0} uid: {1}".format(username, uid)
        return uid
    

    def get_user(self, uid):
        """ Gets user for a give uid, if none is found, None is returned """
        return self.r_server.get(uid)
    
    def gen_uid(self, username):
        """ Generates and assigns a random uid for a user, checks for collision """
        # randomly generate uid, avoid collision
        uid = '%030x' % random.randrange(16**30)
        redis_uid = self.r_server.get(uid)
        while redis_uid is not None:
            uid = '%030x' % random.randrange(16**30)
            redis_uid = self.r_server.get(uid)

        self.set_uid(uid, username)
        return uid

    def set_uid(self, uid, username):
        """ Sets a given uid to a username for debug purpuses """
        self.r_server.set(username,uid)
        self.r_server.set(uid,username)

    def set_secret(self, uid, secret):
        print "setting secret for"
        print uid
        print "secret is"
        print secret
        self.r_server.set("secret_" + uid, secret)

    def get_secret(self, uid):
        print "retrieving secret for"
        print uid
        return self.r_server.get("secret_" + uid)
