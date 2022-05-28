# SPDX-License-Identifier: MY-LICENSE
# Copyright (C) YEAR(S), AUTHOR

# import wasp
#
# class HelloApp():
#     """A hello world application for wasp-os."""
#     NAME = "Hello"
#
#     def __init__(self, msg="Hello, world!"):
#         self.msg = msg
#
#     def foreground(self):
#         self._draw()
#
#     def _draw(self):
#         draw = wasp.watch.drawable
#         draw.fill()
#         draw.string(self.msg, 0, 108, width=240)


import wasp
import machine
import ppg
import fonts
import icons
import time
import watch
from enum import Enum
from collections import Counter

feet = (
    b'\x02'
    b'00'
    b'\x13\xc1-\xc4+\xc6*\xc6*\xc6&\xc3\x01\xc6\t\xc2'
    b'\x1b\xc3\x02\xc5\x08\xc4\x1a\xc4\x01\xc5\x08\xc5\x19\xc4\x02\xc3'
    b'\x08\xc6\x17\xc1\x02\xc3\x02\xc3\x08\xc6\x16\xc3\x02\xc1\x0e\xc6'
    b'\x01\xc3\x12\xc3\x11\xc6\x01\xc3\x13\xc2\x05\xc2\n\xc5\x02\xc3'
    b'\x10\xc2\x01\xc2\x02\xc6\n\xc4\x01\xc4\x10\xc2\x04\xc7\x0b\xc1'
    b'\x03\xc3\x11\xc3\x02\xc8\x10\xc2\x01\xc3\r\xc2\x02\xc9\x13\xc3'
    b'\x0b\xc1\x05\xc9\x0c\xc2\x05\xc3\x0b\xc2\x03\xc9\x0c\xc5\x03\xc2'
    b'\x0c\xc2\x02\xca\x0c\xc6\x05\xc2\t\xc2\x02\xca\x0c\xc7\x03\xc3'
    b'\r\xca\x0c\xc8\x02\xc3\x0c\xca\r\xc9\x02\xc1\r\xca\r\xc9'
    b'\x04\xc2\n\xca\x0e\xc9\x02\xc3\n\xca\x0e\xc9\x02\xc2\x0b\xca'
    b'\x0e\xca\x0e\xca\x0e\xca\x0f\xc9\x0e\xca\x0f\xca\r\xca\x0f\xca'
    b'\r\xca\x10\xcb\x0b\xca\x10\xcc\n\xca\x10\xcd\t\xca\x11\xcc'
    b'\x08\xca\x12\xcc\x07\xcb\x13\xcb\x06\xcb\x14\xcb\x05\xcc\x15\xca'
    b'\x04\xcc\x16\xc9\x05\xcc\x17\xc7\x05\xcd\x17\xc7\x05\xcc\x1a\xc4'
    b"\x07\xcb%\xca&\xca'\xc8)\xc6+\xc4\x0e"
)

heart = (
    b'\x02'
    b'\x1e\x1c'
    b'\x03\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x02\x01\x01\x01'
    b'\x01\x01\x01\x01\x01\x01\x01\x01\x04\x01\x01@$AA\x80'
    b'H\x81\x81\x81\x81\x81\x81\x81A\x81\x02\x81A\x81\x81\x81'
    b'\x81\x81\x81\x81AA\x02\x02\x01\x01A\x01\xc0l\xc1@'
    b'\xb4AAAAA\xc1\x01\x80$\x81\x02\x81\x01\xc1A'
    b'AAAA\xc1\x01\x01\x01\x01\x01\x01\x81\x81\xc0H\xc1'
    b'@lA\x80\x97\x81\xc0\xbb\xc1@\xc2AA\xc1\xc1\x80'
    b'\x90\x81\xc0H\xc1\xc1@$AA\xc1\x80l\x81\x81\xc0'
    b'\xb4\xc1\xc1\xc1\xc1\xc1@\x90A\x80H\x81\x81\x01\xc0$'
    b'\xc1\x01\x01\xc1\x01\x81@\xb4A\x80\xbb\x81A\xc0\xc9\xc1'
    b'@\xfbA\xc1\x81\x81\x80\xb4\x81\xc0H\xc1\x01\x01\xc1\x81'
    b'\x81\x82\x81\x81\x81\x81\x81@lA\x01\x80$\x81\x01\x01'
    b'\xc1A\xc0\x97\xc1@\xbbA\x80\xc2\x81\xc0\xc9\xc1\xc1@'
    b'\xf7A\x80\xf3\x81\xc0\xbb\xc1\xc1@\xb4A\x80\x90\x81\xc0'
    b'l\xc1\xc1\x81AFAA\xc1@HAA\x01\x01A'
    b'\x80\xb4\x81\xc0\xbb\xc1\x81@\xc9A\x80\xfb\x81A\xc0\xb4'
    b'\xc1\xc1\xc2\xc1\xc1\xc2\xc8\xc1\xc1@\x90AA\x80H\x81'
    b'\x01\x01\x81\xc1\xc0\xc2\xc1@\xc9AAA\xc1\x80\xb4\x81'
    b'\x81\x82\x81\x84\x87\x81\x81\xc0\x90\xc1\xc1@HA\x01\x01'
    b'A\x81\x80\xc2\x81\xc0\xfb\xc1@\xf7A\x80\xb4\x82\x81\x8f'
    b'\x81\x81\xc0\x90\xc1\xc1@HA\x01\x01A\x81\x80\xbb\x81'
    b'\xc0\xc9\xc1@\xc2A\x80\xb4\x81\x81\x81\x81\x8e\x81\x81\xc0'
    b'\x90\xc1\xc1@HA\x01\x01A\x81\x80\xbb\x81\x81\x81\xc0'
    b'\xb4\xc1\xc1\xd0\xc1\xc1@\x90AA\x80H\x81\x01\x01\x81'
    b'\xc1\xc1\xc0\xbb\xc1\xc1@\xb4AAPAA\x80\x90\x81'
    b'\x81\xc0H\xc1\x01\x01\xc1AAAQAAAA\x81'
    b'\x81\xc1\x01\x01\xc1\xc1@lA\x80\xb4\x81\x81\x90\x81\x81'
    b'\xc0\x90\xc1\xc1@HA\x80$\x81\x81\x01\x01\x81\x01\xc0'
    b'l\xc1@\xb4AAPAA\x80\x90\x81\x81\xc0H\xc1'
    b'\x01@$A\x02\xc1\x01\x80l\x81\xc0\xb4\xc1\xd1\xc1\xc1'
    b'@\x90AA\x80H\x81\x01\xc0$\xc1\x02\x81\x01@l'
    b'A\x80\x90\x81\xc0\xb4\xc1\xc1\xc1\xcc\xc1\xc1\xc1\x81\x81A'
    b'@HA\x01\x80$\x81\x02\x01\x01\x81\x01\xc0l\xc1@'
    b'\xb4AMAA\x80\x90\x81\x81\xc1\x01\xc0$\xc1\x01\x01'
    b'\x02\x01\x01\xc1\x01@lA\x81\x80\xb4\x81\x81\x81\x88\x81'
    b'\x81\x81\xc0\x90\xc1\xc1A@HA\x01\x80$\x81\x01\x01'
    b'\x03\x01\x01\x01\x81\x01\xc1\xc0\xb4\xc1\xc9\xc1\xc1@\x90A'
    b'A\x80l\x81\x01\x01\x01\x01\x01\x05\x01\x01\xc0$\xc1\x01'
    b'\x81AA@\xb4AADAAA\x80\x90\x81\x81\xc0'
    b'l\xc1\xc1\x01@$A\x01\x01\x07\x01\x02\x01\x01\x81\x80'
    b'\xb4\x81\x81\x84\x81\x81\xc0\x90\xc1\xc1@lA\x01\x01\x02'
    b'\x01\tA\x01\x80$\x81\x01AA\xc0\xb4\xc1\xc1\xc2\xc1'
    b'\xc1@\x90AA\x80l\x81\xc0H\xc1\x01@$A\x01'
    b'\x01\x0b\x01\x02\x01\x01\x80\x90\x81\xc0\xb4\xc1\xc1\xc1\xc1\x81'
    b'\x81@lA\x01\x01\x02\x01\r\x01\x01\x80$\x81\x81A'
    b'A\xc0\x90\xc1@\xb4A\xc1\xc1\x80H\x81\x81\xc0$\xc1'
    b'\xc1\x01\x01\x0f\x01\x02\x01\x01@\x90A\x80\xb4\x81AA'
    b'\x01\x01\x02\x01\x11\x01\x01\xc0H\xc1\xc1\xc1\xc1\xc1\xc1@'
    b'$AA\x01\x01\x13\x01\x02\x01\x01\x01\x01\x02\x01\n'
)


class StressLevel(Enum):
    GREEN = 0
    YELLOW = 1
    RED = 2


class Screen(Enum):
    MAIN = 0
    PULSE_SETTINGS = 1
    ACTIVITY_SETTINGS = 2
    DIAGRAM_MIN = 3
    DIAGRAM_HOUR = 4


class HelloApp():
    """Heart rate monitor application."""
    NAME = 'Heart'

    def __init__(self):
        self._debug = False
        self._hrdata = None
        watch.accel.reset()
        self._scroll = wasp.widgets.ScrollIndicator()
        self._wake = 0
        self.tick_counter = 0
        self.steps_count = 0
        self.prev_steps_count = 0
        self.bpm = 0
        self.max_bpm = wasp.widgets.Spinner(90, 30, 60, 99, 2)
        self._scroll = wasp.widgets.ScrollIndicator()
        self.active_screen_index = 0
        self.active_screen = Screen.MAIN
        self.is_workout_checkbox = wasp.widgets.Checkbox(4, 54, 'Workouts')
        self.is_stress = False
        self.bpm_graph_sec = []
        self.bpm_graph_min = []
        self.bpm_graph_hour = []
        self.step_delta = 10
        self.stress_level = StressLevel.GREEN

    def foreground(self):
        """Activate the application."""
        wasp.watch.hrs.enable()

        # There is no delay after the enable because the redraw should
        # take long enough it is not needed
        draw = wasp.watch.drawable
        draw.fill()
        draw.set_color(wasp.system.theme('bright'))
        # draw.string('PPG graph', 0, 6, width=240)
        wasp.system.request_event(wasp.EventMask.TOUCH)
        wasp.system.request_event(wasp.EventMask.SWIPE_UPDOWN)
        wasp.system.request_tick(1000 // 8)

        self._hrdata = ppg.PPG(10)
        if self._debug:
            self._hrdata.enable_debug()
        self._x = 0

        wasp.system.cancel_alarm(self._wake, self._reset)
        self._page = -1
        self._draw()
        # wasp.system.request_event(wasp.EventMask.SWIPE_UPDOWN)
        # wasp.system.request_tick(1000)

    def background(self):
        wasp.watch.hrs.disable()
        self._hrdata = None

        now = watch.rtc.get_localtime()
        yyyy = now[0]
        mm = now[1]
        dd = now[2]
        then = (yyyy, mm, dd+1, 0, 0, 0, 0, 0, 0)

        self._wake = time.mktime(then)
        wasp.system.set_alarm(self._wake, self._reset)

    def touch(self, event):
        if self.active_screen == Screen.PULSE_SETTINGS:
            self.max_bpm.touch(event)

        elif self.active_screen == Screen.ACTIVITY_SETTINGS:
            self.is_workout_checkbox.touch(event)

    def swipe(self, event):
        if event[0] == wasp.EventType.UP:
            self.active_screen_index += 1
        elif event[0] == wasp.EventType.DOWN:
            self.active_screen_index -= 1
        self._draw()

    def _reset(self):
        """"Reset the step counter and re-arm the alarm."""
        watch.accel.steps = 0
        self._wake += 24 * 60 * 60
        wasp.system.set_alarm(self._wake, self._reset)

    def _update_stress(self):
        step_difference = self.steps_count - self.prev_steps_count
        high_pulse_is_workout = self.is_workout_checkbox.state

        stress_level = StressLevel.GREEN

        if self.bpm > self.max_bpm.value:
            stress_level = StressLevel.RED
            if high_pulse_is_workout and step_difference > self.step_delta:
                stress_level = StressLevel.YELLOW

        self.stress_level = stress_level
        self.is_stress = stress_level == StressLevel.RED

    def _average_bpm(self, bpm_graph):
        return int(sum([value['bpm'] for value in bpm_graph]) / len(bpm_graph))

    def _average_stress(self, bpm_graph, delta=1):
        c = Counter([data['stress_level'] for data in bpm_graph])
        red = c[StressLevel.RED]
        yellow = c[StressLevel.YELLOW]

        if red > delta:
            return StressLevel.RED
        elif yellow > delta:
            return StressLevel.YELLOW

        return StressLevel.GREEN

    def _update_graph(self):
        """Should be called every second"""
        if self.bpm == 0:
            return

        self.bpm_graph_sec.append({"bpm": self.bpm, "stress_level": self.stress_level})

        if len(self.bpm_graph_sec) % 60 == 0:
            self.bpm_graph_min.append({
                "bpm": self._average_bpm(self.bpm_graph_sec[-60:]),
                "stress_level": self._average_stress(self.bpm_graph_sec[-60:], delta=10)
            })
            self.bpm_graph_sec.clear()

            if len(self.bpm_graph_min) % 60 == 0:
                self.bpm_graph_hour.append({
                    "bpm": self._average_bpm(self.bpm_graph_min[-60:]),
                    "stress_level": self._average_stress(self.bpm_graph_min[-60:], delta=5)
                })

    def _draw_stress(self):
        draw = wasp.watch.drawable
        draw.set_font(fonts.sans24)
        if self.is_stress:
            wasp.watch.drawable.string("High stress.", 54, 24 + 150)
        else:
            wasp.watch.drawable.string("Low stress.", 54, 24 + 150)

    def _update_bpm(self):
        self._hrdata.preprocess(wasp.watch.hrs.read_hrs())
        if len(self._hrdata.data) >= 240:
            self.bpm = self._hrdata.get_heart_rate()

    def tick(self, ticks):
        """This is an outrageous hack but, at present, the RTC can only
        wake us up every 125ms so we implement sub-ticks using a regular
        timer to ensure we can read the sensor at 24Hz.
        """

        self.tick_counter += 1
        if self.tick_counter == 8:
            self.tick_counter = 0
            self._update_steps()
            self._update_stress()
            # self._update_graph()
            self._draw()

        self._update_graph()
        t = machine.Timer(id=1, period=8000000)
        t.start()
        self._update_bpm()
        wasp.system.keep_awake()

        while t.time() < 41666:
            pass
        self._update_bpm()

        while t.time() < 83332:
            pass
        self._update_bpm()

        t.stop()
        del t

    def _draw_bpm(self):
        draw = wasp.watch.drawable
        draw.set_color(wasp.system.theme('bright'))
        draw.string('{}'.format(self.bpm),
                    0, 48, width=210)
        draw.blit(heart, 130, 46)

    def _draw_diagram_min(self):
        draw = wasp.watch.drawable
        x = 0
        draw.string('Minute graph', 0, 6, width=240)
        draw.string('{}'.format(self.max_bpm.value), 0, 215 - self.max_bpm.value)
        draw.string('120', 0, 90)
        draw.line(0, 237, 237, 237, 2, 0xffff)
        draw.line(0, 240 - self.max_bpm.value, 237, 240 - self.max_bpm.value, 2, 0xffff)
        for bpm in self.bpm_graph_min[-60:]:
            current_bpm = bpm['bpm']
            stress = bpm['stress_level']
            if stress == StressLevel.GREEN:
                color_graph = 0x07c0
            elif stress == StressLevel.YELLOW:
                color_graph = 0xffe0
            elif stress == StressLevel.RED:
                color_graph = 0xf800
            draw.line(1 + x, 237 - current_bpm, 1 + x, 237, 2, color_graph)
            x += 4

    def _draw_diagram_hour(self):
        draw = wasp.watch.drawable
        x = 0
        draw.string('Hour graph', 0, 6, width=240)
        draw.string('{}'.format(self.max_bpm.value), 0, 215 - self.max_bpm.value)
        draw.string('120', 0, 90)
        draw.line(0, 237, 237, 237, 2, 0xffff)
        draw.line(0, 240 - self.max_bpm.value, 237, 240 - self.max_bpm.value, 2, 0xffff)
        for bpm in self.bpm_graph_hour[-60:]:
            current_bpm = bpm['bpm']
            stress = bpm['stress_level']
            if stress == StressLevel.GREEN:
                color_graph = 0x07c0
            elif stress == StressLevel.YELLOW:
                color_graph = 0xffe0
            elif stress == StressLevel.RED:
                color_graph = 0xf800
            draw.line(1 + x, 237 - current_bpm, 1 + x, 237, 2, color_graph)
            x += 4

    def _draw_bar(self):
        wasp.system.bar.clock = True
        wasp.system.bar.update()
        wasp.system.bar.draw()

    def _draw(self):
        """Draw the display from scratch."""
        draw = wasp.watch.drawable
        mute = wasp.watch.display.mute
        self.active_screen = Screen(self.active_screen_index % len(Screen))
        mute(True)
        draw.fill()

        if self.active_screen == Screen.MAIN:
            self._draw_bar()
            self._draw_stress()
            self._draw_steps()
            self._draw_bpm()

        elif self.active_screen == Screen.PULSE_SETTINGS:
            self._draw_pulse_settings()

        elif self.active_screen == Screen.ACTIVITY_SETTINGS:
            self._draw_activity_settings()

        elif self.active_screen == Screen.DIAGRAM_MIN:
            self._draw_diagram_min()

        elif self.active_screen == Screen.DIAGRAM_HOUR:
            self._draw_diagram_hour()

        mute(False)

    def _draw_activity_settings(self):
        draw = wasp.watch.drawable
        draw.set_font(fonts.sans24)
        draw.string('Activity settings', 0, 6, width=240)
        self.is_workout_checkbox.draw()
        s = 'If set, high pulse during active movements is treated as workouts'
        chunks = draw.wrap(s, 240)
        for i in range(len(chunks) - 1):
            sub = s[chunks[i]:chunks[i + 1]].rstrip()
            draw.string(sub, 5, 118 + 24 * i)

    def _draw_pulse_settings(self):
        draw = wasp.watch.drawable
        draw.set_font(fonts.sans24)
        draw.string('Pulse threshold', 0, 6, width=240)
        s = 'If the pulse value is higher, stress will be determined'
        chunks = draw.wrap(s, 240)
        for i in range(len(chunks) - 1):
            sub = s[chunks[i]:chunks[i + 1]].rstrip()
            draw.string(sub, 10, 145 + 24 * i)
        prev_bpm = self.max_bpm.value
        self.max_bpm.value = prev_bpm
        self.max_bpm.draw()

    def _draw_steps(self):
        draw = wasp.watch.drawable
        t = str(self.steps_count)
        draw.blit(feet, 12, 132 - 24)
        w = fonts.width(fonts.sans24, t)
        draw.set_font(fonts.sans24)
        draw.set_color(draw.lighten(wasp.system.theme('spot1'), wasp.system.theme('contrast')))
        draw.string(t, 228 - w, 132 - 18)

    def _update_steps(self):
        self.prev_steps_count = self.steps_count
        self.steps_count = watch.accel.steps

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, value):
        self._debug = value
        if value and self._hrdata:
            self._hrdata.enable_debug()