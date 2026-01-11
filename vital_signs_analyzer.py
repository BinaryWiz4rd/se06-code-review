"""
The vital_signs_analyzer script implements the following requirements:
1/ The system should accept heart rate (HR) and blood oxygen saturation (SpO2) readings. The values should be normalized into a 0-1 range using defined physiological limits.
2/ The system should detect the patient's status based on thresholds for normalized HR and SpO2.
3/ The user should be able to override the status with a manually set value.
4/ The system should support displaying the status (if enabled) and logging it to a file (if enabled).
"""

HR_MIN = 40
HR_MAX = 180
SPO2_MIN = 0
SPO2_MAX = 100

NORM_HR_CRITICAL_THRESHOLD = 0.7
NORM_SPO2_CRITICAL_THRESHOLD = 0.3
NORM_HR_WARNING_THRESHOLD = 0.4
SPO2_SEVERE_THRESHOLD = 88
HR_SEVERE_THRESHOLD = 200

class VitalSignsAnalyzer:
    def __init__(self, debug_mode=False):
        self.debug_mode = debug_mode
        self.status_message = None

    def normalize_hr(self, hr):
        return (hr - HR_MIN) / (HR_MAX - HR_MIN)

    def normalize_spo2(self, spo2):
        return spo2 / 100

    def determine_status(self, norm_hr, norm_spo2, hr, spo2):
        if norm_hr > NORM_HR_CRITICAL_THRESHOLD and norm_spo2 < NORM_SPO2_CRITICAL_THRESHOLD:
            return "CRITICAL"
        elif norm_hr > NORM_HR_WARNING_THRESHOLD:
            if spo2 < SPO2_SEVERE_THRESHOLD or hr > HR_SEVERE_THRESHOLD:
                return "SEVERE?"
            else:
                return "WARNING"
        else:
            return "OK"

    def log_vitals(self, hr, spo2, norm_hr, norm_spo2, status):
        try:
            with open("vitals_log.txt", "a") as f:
                f.write(
                    f"HR={hr}, SpO2={spo2}, NormHR={norm_hr:.2f}, NormSpO2={norm_spo2:.2f}, STATUS={status}\n"
                )
        except Exception as e:
            print(f"Error writing to log file: {e}")

    def display_output(self, status, verbose, hr, spo2, force):
        if verbose:
            print("Analyzing vital data:", hr, spo2, "force:", force)
            print("Status is:", status)

    def analyze(self, hr, spo2, log=True, override_status=None, verbose=0, force=None):
        if hr < 0 or hr > 300:
            raise ValueError(f"Invalid HR value: {hr}. Must be between 0 and 300.")

        if spo2 < 0 or spo2 > 100:
            raise ValueError(f"Invalid SpO2 value: {spo2}. Must be between 0 and 100.")

        norm_hr = self.normalize_hr(hr)
        norm_spo2 = self.normalize_spo2(spo2)

        if override_status:
            status = override_status
        else:
            status = self.determine_status(norm_hr, norm_spo2, hr, spo2)

        self.display_output(status, verbose, hr, spo2, force)

        self.status_message = f"Last status: {status}" + (" (DBG)" if self.debug_mode else "")

        if log:
            self.log_vitals(hr, spo2, norm_hr, norm_spo2, status)

        return self.status_message

if __name__ == "__main__":

    analyzer = VitalSignsAnalyzer(debug_mode=False)

    hr = 999
    spo2 = -3

    result = analyzer.analyze(hr, spo2, True, None, 3, True)

    print("Finished analysis, status_message:", analyzer.status_message)
