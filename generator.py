import os

def generate_examples(directory):
    event_log_command = '!R!KCFG"ELOG";EXIT;'
    tiered_color_on_command = '!R!KCFG"TCCM",1;\nKCFG"STCT",1,20;\nKCFG"STCT",2,50;EXIT;'
    tiered_color_off_command = '!R!KCFG"TCCM",0;EXIT;'
    line_mode_60_command = '!R! FRPO U0,6; FRPO U1,60; EXIT;'
    line_mode_66_command = '!R! FRPO U0,6; FRPO U1,66; EXIT;'
    tray_switch_on_command = '!R! FRPO X9,9; FRPO R2,0; EXIT;'
    tray_switch_off_command = '!R! FRPO X9,0; FRPO R2,0; EXIT;'
    sleep_timer_on_command = '!R! FRPO N5,1; EXIT;'
    sleep_timer_off_command = '!R! FRPO N5,0; EXIT;'
    backup_FRPO_command = '!R! STAT,1; EXIT;'
    init_FRPO_command = '!R! FRPO INIT; EXIT;'

    examples = {
        "event_log": event_log_command,
        "3_tiered_color_on": tiered_color_on_command,
        "3_tiered_color_off": tiered_color_off_command,
        "60_line_mode": line_mode_60_command,
        "66_line_mode": line_mode_66_command,
        "tray_switch_on": tray_switch_on_command,
        "tray_switch_off": tray_switch_off_command,
        "sleep_timer_on": sleep_timer_on_command,
        "sleep_timer_off": sleep_timer_off_command,
        "backup_FRPO": backup_FRPO_command,
        "init_FRPO": init_FRPO_command,
    }

    for file, text in examples.items():
        file_name = os.path.join(directory, f"{file}.txt")
        if not os.path.exists(file_name):
            with open(file_name, "w") as f:
                f.write(text)