class AccountManager(object):

    def get_uid(self, username):
        raise NotImplementedError()

    def get_user(self, uid):
        raise NotImplementedError()
