# -*- encoding: utf-8 -*-
"""
tests.peer.test_exchanging module

"""

from hio.base import doing

from keri.app import keeping, habbing
from keri.core import coring, parsing, eventing
from keri.db import basing
from keri.help import decking
from keri.peer import exchanging


def test_exchanger():
    sidSalt = coring.Salter(raw=b'0123456789abcdef').qb64

    with basing.openDB(name="sid") as sidDB, \
            keeping.openKS(name="sid") as sidKS, \
            basing.openDB(name="red") as redDB, \
            keeping.openKS(name="red") as redKS:

        limit = 1.0
        tock = 0.03125
        doist = doing.Doist(limit=limit, tock=tock)

        # Init key pair managers
        sidMgr = keeping.Manager(ks=sidKS, salt=sidSalt)

        # Init Keverys
        sidKvy = eventing.Kevery(db=sidDB)
        redHab = habbing.Habitat(ks=redKS, db=redDB, temp=True)
        redKvy = eventing.Kevery(db=redDB)

        # Setup sid by creating inception event
        verfers, digers, cst, nst = sidMgr.incept(stem='sid', temp=True)  # algo default salty and rooted
        sidSrdr = eventing.incept(keys=[verfer.qb64 for verfer in verfers],
                                  nxt=coring.Nexter(digs=[diger.qb64 for diger in digers]).qb64,
                                  code=coring.MtrDex.Blake3_256)

        sidPre = sidSrdr.ked["i"]

        sidMgr.move(old=verfers[0].qb64, new=sidPre)  # move key pair label to prefix

        sigers = sidMgr.sign(ser=sidSrdr.raw, verfers=verfers)

        excMsg = bytearray(sidSrdr.raw)
        counter = coring.Counter(code=coring.CtrDex.ControllerIdxSigs,
                                 count=len(sigers))
        excMsg.extend(counter.qb64b)
        for siger in sigers:
            excMsg.extend(siger.qb64b)

        sidIcpMsg = excMsg  # save for later

        parsing.Parser().parse(ims=bytearray(sidIcpMsg), kvy=redKvy)
        assert redKvy.kevers[sidPre].sn == 0  # accepted event

        echo = EchoDoer(tymth=doist.tymen())
        redExc = exchanging.Exchanger(hab=redHab, tymth=doist.tymen(), handlers=[echo])

        pl = dict(x="y")
        sidExcSrdr = exchanging.exchange(route="/test/message", payload=pl)

        # Create exn message, sign it and attack Signer Seal
        sigers = sidMgr.sign(ser=sidExcSrdr.raw, verfers=verfers)

        excMsg = bytearray(sidExcSrdr.raw)
        excMsg.extend(coring.Counter(coring.CtrDex.SignerSealCouples, count=1).qb64b)
        excMsg.extend(sidPre.encode("utf-8"))

        counter = coring.Counter(code=coring.CtrDex.ControllerIdxSigs,
                                 count=len(sigers))
        excMsg.extend(counter.qb64b)
        for siger in sigers:
            excMsg.extend(siger.qb64b)

        parsing.Parser().parse(ims=bytearray(excMsg), kvy=redKvy, exc=redExc)

        doist.do(doers=[redExc])
        assert doist.tyme == limit

        resp = echo.cues.popleft()
        respSer = coring.Serder(raw=resp.raw)
        assert respSer.ked['t'] == coring.Ilks.exn
        assert respSer.ked['r'] == "/test/messageResp"
        assert respSer.ked['q'] == dict(req=pl)


class EchoDoer(doing.Doer):

    resource = "/test/message"

    def __init__(self, **kwa):

        self.msgs = decking.Deck()
        self.cues = decking.Deck()

        super(EchoDoer, self).__init__(**kwa)

    def do(self, tymth, tock=0.0, **opts):
        while True:
            while self.msgs:
                msg = self.msgs.popleft()
                payload = msg["payload"]
                pre = msg["pre"]
                verfers = msg["verfers"]
                sigers = msg["sigers"]

                assert payload == dict(x="y")
                assert pre.qb64 == "ELfzj-TkiKYWsNKk2WE8F8VEgbu3P-_HComVHcKrvGmY"
                assert len(verfers) == 1
                assert verfers[0].qb64 == "Djy1swBRlUIR5m16EUkc-Aj_WFCzAEbs0YpOh5IWt7kM"
                assert len(sigers) == 1

                self.cues.append(exchanging.exchange(route="/test/messageResp", payload=dict(req=payload)))
                yield
            yield


if __name__ == "__main__":
    test_exchanger()
