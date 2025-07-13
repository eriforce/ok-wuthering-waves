import time

from src.char.BaseChar import BaseChar, Priority

class LingYang(BaseChar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.intro_motion_freeze_duration = 1.07

    def still_in_liberation(self):
        return self.time_elapsed_accounting_for_freeze(self.last_liberation) < 13.0

    def do_perform(self):
        if self.has_intro:
            self.continues_normal_attack(self.intro_motion_freeze_duration)

        if self.liberation_available():
            self.click_liberation()

        if self.still_in_liberation():
            self.heavy_click_forte()

        while self.still_in_liberation():
            self.continues_normal_attack(2.4)
            self.send_resonance_key()
            self.sleep(0.05)

        if self.echo_available():
            self.click_echo(duration=1.6)

        self.switch_next_char()

    def switch_next_char(self, post_action=None, free_intro=False, target_low_con=False):
        self.get_current_con()
        super().switch_next_char(post_action=post_action, free_intro=free_intro, target_low_con=target_low_con)

    def do_get_switch_priority(self, current_char: BaseChar, has_intro=False, target_low_con=False):
        if self.still_in_liberation():
            return Priority.MAX

        if has_intro and self.current_con >= 0.6:
            return Priority.FAST_SWITCH

        if self.liberation_available() and self.current_con >= 0.4:
            return Priority.FAST_SWITCH

        return super().do_get_switch_priority(current_char, has_intro, target_low_con)
