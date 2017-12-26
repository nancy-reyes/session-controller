from datetime import datetime, timedelta
import time


class SessionController(object):

    event_data = {}
    check_count = 0

    def event(self, event_type):
        """ Simulation of a swipe, touch or check event """

        # Records first event
        if self.event_data == {}:
            self.event_data['session_start'] = datetime.now()

        # Keep track of check event count
        if event_type == 'check':
            self.check_count += 1

        self.event_data[event_type] = datetime.now()

    def times(self):
        """ If valid session, prints session start & end times """

        now = datetime.now()
        swipe_timeout = 3
        touch_timeout = 1

        if (('swipe' in self.event_data and (now - self.event_data['swipe']) < timedelta(seconds=swipe_timeout)) or
            ('touch' in self.event_data and (now - self.event_data['touch']) < timedelta(seconds=touch_timeout)) or
            ('check' in self.event_data and self.check_count % 2 != 0)):

            return 'Session still active'

        start = min(self.event_data.values())
        end = max(self.event_data.values())

        print("Session start: {}".format(str(start)))
        print("Session end: {}".format(str(end)))

        return start, end
