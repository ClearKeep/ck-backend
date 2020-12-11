# -*- coding: utf-8 -*-

from libsignal.groups.state.senderkeystore import SenderKeyStore
from libsignal.groups.state.senderkeyrecord import SenderKeyRecord


class MySenderKeyStore(SenderKeyStore):
    def __init__(self):
        self.store = {}

    def storeSenderKey(self, senderKeyName, senderKeyRecord):
        self.store[senderKeyName] = senderKeyRecord

    def loadSenderKey(self, senderKeyName):
        if senderKeyName in self.store:
            return SenderKeyRecord(serialized=self.store[senderKeyName].serialize())

        return SenderKeyRecord()
