from instagrapi import Client
import logging
import os
from dotenv import load_dotenv

logger = logging.getLogger()


def login_user():
    """
    Attempts to login to Instagram using either the provided session information
    or the provided username and password.
    """
    load_dotenv()
    USERNAME = os.getenv("INSTA_USER")
    PASSWORD = os.getenv("INSTA_PWD")
    cl = Client()
    cl.delay_range = [3, 5]
    session = None
    session_path = os.path.join(os.path.dirname(__file__), "session.json")
    if os.path.exists(session_path):
        session = cl.load_settings(session_path)

    login_via_session = False
    login_via_pw = False

    if session:
        try:
            cl.set_settings(session)
            cl.login(USERNAME, PASSWORD)

            # check if session is valid
            try:
                cl.get_timeline_feed()
            except Exception:
                logger.info(
                    "Session is invalid, need to login via username and password"
                )

                old_session = cl.get_settings()

                # use the same device uuids across logins
                cl.set_settings({})
                cl.set_uuids(old_session["uuids"])

                cl.login(USERNAME, PASSWORD)
            login_via_session = True
        except Exception as e:
            logger.info("Couldn't login user using session information: %s" % e)

    if not login_via_session:
        try:
            logger.info(
                "Attempting to login via username and password. username: %s" % USERNAME
            )
            if cl.login(USERNAME, PASSWORD):
                login_via_pw = True
                cl.dump_settings(session_path)
        except Exception as e:
            logger.info("Couldn't login user using username and password: %s" % e)

    if not login_via_pw and not login_via_session:
        raise Exception("Couldn't login user with either password or session")

    return cl
