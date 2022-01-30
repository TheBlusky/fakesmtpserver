from asyncio import sleep, get_running_loop, CancelledError
from aiosmtpd.controller import Controller
from database import Database
from logger import log


class SMTPHandler:
    async def handle_DATA(self, server, session, envelope):
        for email_to in envelope.rcpt_tos:
            Database.instance.add_email(
                email_to, envelope.content.decode("utf8", errors="replace")
            )
            log(f"Message received from {email_to}")
        return "250 Message accepted for delivery"


class SMTPServer:
    instance = None

    def __init__(self):
        if not SMTPServer.instance:
            SMTPServer.instance = self
        else:
            raise Exception("SMTPServer already created")
        self.started = False
        self.controller = None
        self.self_stop_task = None

    async def start(self):
        loop = get_running_loop()
        if self.self_stop_task:
            self.self_stop_task.cancel()
        self.self_stop_task = loop.create_task(self.self_stop())
        if not self.started:
            log("Starting SMTP Server")
            self.controller = Controller(SMTPHandler(), hostname="", port=2525)
            self.controller.start()
            self.started = True

    async def stop(self):
        if self.self_stop_task:
            self.self_stop_task.cancel()
        if self.started:
            log("Stopping SMTP Server")
            self.controller.stop()
            self.started = False

    def status(self):
        return self.started

    async def self_stop(self):
        try:
            log("Autostop scheduled in 3600s")
            await sleep(3600)
            log("Stopping SMTP Server (Autostop)")
            loop = get_running_loop()
            self.self_stop_task = None
            loop.create_task(self.stop())
        except CancelledError:
            log("Autostop cancelled")


SMTPServer()
