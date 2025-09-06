import pandas as pd

file_path = r'C:\Users\madel\Desktop\Data Portfolio\Labor Law Compliance\labor_law_01-2025.xlsx'
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
high_noncompliance_count = (summary['rendered_exactly_pct'] > 50).sum()

summary_with_zone = pd.merge(summary, employee_df[['employee_id', 'employee_zone']], on='employee_id', how='left')

total_employees_zone = employee_df.groupby('employee_zone')['employee_id'].nunique().reset_index()
total_employees_zone.columns = ['employee_zone', 'total_employees']

high_noncomp_zone = summary_with_zone[summary_with_zone['rendered_exactly_pct'] > 50].groupby('employee_zone')['employee_id'].nunique().reset_index()
high_noncomp_zone.columns = ['employee_zone', 'employees_with_high_noncompliance']

zone_summary = pd.merge(total_employees_zone, high_noncomp_zone, on='employee_zone', how='left').fillna(0)

zone_summary['high_noncompliance_pct'] = (zone_summary['employees_with_high_noncompliance'] / zone_summary['total_employees']) * 100
zone_summary['high_noncompliance_pct'] = zone_summary['high_noncompliance_pct'].round(2)

print(f"\nNumber of employees with >50% rendered exactly: {high_noncompliance_count}")
print(summary)
print("\nRendered Exactly >50% by Employee Zone:")
print(zone_summary)


output_path = r'C:\Users\madel\Desktop\Data Portfolio\Labor Law Compliance\labor_law_compliance_report.xlsx'

with pd.ExcelWriter(output_path) as writer:
    summary.to_excel(writer, sheet_name='Employee Rendered Summary', index=False)
    zone_summary.to_excel(writer, sheet_name='Zone Rendered Compliance', index=False)

print(f"Exported results to {output_path}")
