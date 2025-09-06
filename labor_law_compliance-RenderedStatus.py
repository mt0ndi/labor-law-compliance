import pandas as pd

file_path = r'C:\Users\madel\Documents\labor_law_01-2025.xlsx'
schedule_df = pd.read_excel(file_path, sheet_name='schedule_data')
employee_df = pd.read_excel(file_path, sheet_name='employee_data')

merged_df = pd.merge(schedule_df, employee_df, on = 'employee_id', how = 'left')

from datetime import time

def convert_to_timedelta(val):
    if isinstance(val, pd.Timestamp):
        val = val.time()
    if isinstance(val, time):
        return pd.Timedelta(hours=val.hour, minutes=val.minute, seconds=val.second)
    elif pd.isna(val):
        return pd.NaT
    else:
        try:
            t = pd.to_datetime(val).time()
            return pd.Timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
        except Exception:
            return pd.NaT

for col in ['rendered_start_time', 'rendered_end_time', 'schedule_start_time', 'schedule_end_time']:
    merged_df[col] = merged_df[col].apply(convert_to_timedelta)


def check_minute_for_minute(row):
    dateCheck = row['rendered_date'] == row['schedule_date']

    startTime = round(row['rendered_start_time'].total_seconds()/60) == round(row['schedule_start_time'].total_seconds()/60)
    endTime = round(row['rendered_end_time'].total_seconds()/60) == round(row['schedule_end_time'].total_seconds()/60)

    if dateCheck and startTime and endTime: return "Rendered Exactly"
    else: return "Minute for Minute"

merged_df['rendered_status'] = merged_df.apply(check_minute_for_minute, axis=1)

summary = merged_df.groupby('employee_id').agg(
    total_appointments=('rendered_status', 'count'),
    rendered_exactly_count=('rendered_status', lambda x: (x == "Rendered Exactly").sum())
)

summary['rendered_exactly_pct'] = (summary['rendered_exactly_count'] / summary['total_appointments']) * 100

summary = summary.reset_index()

print(summary)
