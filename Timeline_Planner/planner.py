from datetime import datetime, timedelta
import holidays
import pandas as pd


class TimelinePlanner:
    def __init__(self, country_code='ZA', years=None, dec_shutdown=None, extra_holidays=None):
        # Load holidays
        self.holidays = set(holidays.country_holidays(country_code, years=years).keys())
        if extra_holidays is not None:
            self.holidays.update(pd.to_datetime(extra_holidays).dt.date.tolist())

        # December shutdown override
        self.dec_shutdown = dec_shutdown  # tuple of (start_date, end_date)

    def is_working_day(self, day):
        if day.weekday() >= 5:  # weekends
            return False
        if day in self.holidays:  # public holidays
            return False
        if self.dec_shutdown:
            if self.dec_shutdown[0] <= day < self.dec_shutdown[1]:
                return False
        return True

    def parse_duration_to_days(self, duration: int, unit: str) -> int:
        """Convert duration with unit (days/weeks) into working days."""
        if str(unit).lower().startswith("week"):
            return int(duration) * 5
        elif str(unit).lower().startswith("day"):
            return int(duration)
        return 0

    def add_working_days(self, start_date: datetime, num_days: int) -> datetime:
        """Add working days to a start date, skipping weekends, holidays, shutdowns."""
        current_date = start_date
        added_days = 0
        while added_days < num_days:
            current_date += timedelta(days=1)
            if self.is_working_day(current_date.date()):
                added_days += 1
        return current_date

    def calculate_timeline(self, modules: pd.DataFrame):
        """Generate full timeline from template CSV format."""

        # Get program start date from first row
        start_date_str = str(modules.loc[0, "program_start_date"])
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")

        # Get shutdown dates
        dec_shutdown_start = pd.to_datetime(modules.loc[0, "dec_shutdown_start"]).date()
        dec_shutdown_end = pd.to_datetime(modules.loc[0, "dec_shutdown_end"]).date()

        self.dec_shutdown = (dec_shutdown_start, dec_shutdown_end)

        # Build timeline
        timeline = []
        current_date = start_date

        for _, row in modules.iterrows():
            module_name = row["block/module_name"]
            duration = row["duration"]
            unit = row["unit"]

            # Convert to working days
            duration_days = self.parse_duration_to_days(duration, unit)

             # Automatically calculate display unit
            if duration_days % 5 == 0:
                display_unit = f"{duration_days // 5} week(s)"
            else:
                display_unit = f"{duration_days} day(s)"

            # End date
            end_date = self.add_working_days(current_date, duration_days - 1)

            timeline.append({
                "Module": module_name,
                "Start Date": current_date.strftime("%Y-%m-%d"),
                "End Date": end_date.strftime("%Y-%m-%d"),
                "Duration (days)": duration_days,
                "Unit": display_unit
            })

            # Next module starts after end_date
            current_date = self.add_working_days(end_date, 1)

        return pd.DataFrame(timeline)