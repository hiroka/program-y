"""
Copyright (c) 2016-2018 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import logging
import time

from programy.dialog.storage.base import ConversationStorage
import redis

class ConversationRedisStorage(ConversationStorage):

    def __init__(self, config):
        ConversationStorage.__init__(self, config)
        self._redis = redis.StrictRedis(host=config.host, port=config.port, db=0)

    def empty(self):
        pass

    def save_conversation(self, conversation, clientid):
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("Saving conversation to Redis for %s"%clientid)
        print("Writing to redis for %s"%clientid)
        self._redis.hmset(clientid, conversation._properties)

    def load_conversation(self, conversation, clientid, restore_last_topic=False):
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("Loading Conversation from file for %s"%clientid)

        print("Reading from redis for %s"%clientid)
        result = self._redis.hgetall(clientid)
        if result is not None:
            conversation._properties = result

    def remove_conversation(self, clientid):
        pass
