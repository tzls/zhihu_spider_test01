import redis
class SimpleHash():
    def __init__(self,cap,seed):
        self.cap = cap
        self.seed =seed

    def hash(self, value):
        ret = 0
        for i in range(value.__len__()):
            ret += self.seed * ret + ord(value[i])
        return ((self.cap - 1) & ret)