# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-08-18
# @Filename: lvm_actors.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

import asyncio
import sys
import uuid

from logging import DEBUG

from sdsstools.logger import StreamFormatter  
from sdsstools import get_logger, read_yaml_file
from sdsstools.logger import SDSSLogger

from clu import AMQPClient, CommandStatus

from cluplus.proxy import Proxy, invoke, unpack

lvm_amqpc = AMQPClient(name=f"{sys.argv[0]}.proxy-{uuid.uuid4().hex[:8]}")
logger = lvm_amqpc.log

class lvm:
    def execute(foo, *args, verbose=None, **kwargs):
        async def start(coro):
            await coro.start()
        if verbose:
           logger.sh.setLevel(DEBUG)
           #logger.sh.formatter = StreamFormatter(fmt='%(asctime)s %(name)s %(levelname)s %(filename)s:%(lineno)d: \033[1m%(message)s\033[21m') 
        lvm_amqpc.loop.run_until_complete(start(args[0]))
        return lvm_amqpc.loop.run_until_complete(foo(*args, **kwargs))

    class sci:
        foc = Proxy(lvm_amqpc, "lvm.sci.foc")
        km = Proxy(lvm_amqpc, "lvm.sci.km")
        pwi = Proxy(lvm_amqpc, "lvm.sci.pwi")
        agc = Proxy(lvm_amqpc, "lvm.sci.agcam")
        async def start():
            await lvm_amqpc.start()
            await lvm.sci.foc.start()
            await lvm.sci.km.start()
            await lvm.sci.pwi.start()
            await lvm.sci.agc.start()
            return lvm.sci

    def from_string(subsys: str):
        if subsys == 'sci': return lvm.sci


