import pandas as pd
from datetime import time

file_path = r'C:\Users\madel\Desktop\Data Portfolio\Labor Law Compliance\labor_law_01-2025.xlsx'
schedule_df = pd.read_excel(file_path, sheet_name='schedule_data')
employee_df = pd.read_excel(file_path, sheet_name='employee_data')

merged_df = pd.merge(schedule_df, employee_df, on='employee_id', how='left')

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

# --- Part 1: Identify missed break violations ---

daily_reports = []
grouped = merged_df.groupby(['employee_id', 'rendered_date'])

for (emp_id, date), group in grouped:
    group_sorted = group.sort_values('rendered_start_time')
    total_hours = group_sorted['duration_rendered_hours'].sum()
    if group_sorted.empty:
        continue
    first_start = group_sorted.iloc[0]['rendered_start_time']
    fifth_hour = first_start + pd.Timedelta(hours=5)

    breaks = []
    for i in range(len(group_sorted) - 1):
        end_time = group_sorted.iloc[i]['rendered_end_time']
        next_start = group_sorted.iloc[i + 1]['rendered_start_time']
        break_duration = next_start - end_time
        breaks.append({
            'break_duration': break_duration,
            'before_fifth_hour': end_time < fifth_hour
        })

    if breaks:
        max_break_before_fifth = max(
            [b['break_duration'] for b in breaks if b['before_fifth_hour']],
            default=pd.Timedelta(seconds=0)
        )
    else:
        max_break_before_fifth = pd.Timedelta(0)

    violation_flag = (total_hours > 5 and max_break_before_fifth < pd.Timedelta(minutes=30))
    violation = "Missed Break" if violation_flag else ""

    daily_reports.append({
        'employee_id': emp_id,
        'date': date,
        'violation': violation
    })

break_violations_df = pd.DataFrame(daily_reports)
break_violations_df = break_violations_df[break_violations_df['violation'] == 'Missed Break']

break_violations_df = break_violations_df.merge(employee_df[['employee_id', 'employee_zone']], on='employee_id', how='left')
break_violations_df.rename(columns={'employee_zone': 'zone'}, inplace=True)

# --- Part 2: Identify rendered as scheduled "violations" ---

def check_minute_for_minute(row):
    date_check = row['rendered_date'] == row['schedule_date']
    start_time_check = round(row['rendered_start_time'].total_seconds() / 60) == round(row['schedule_start_time'].total_seconds() / 60)
    end_time_check = round(row['rendered_end_time'].total_seconds() / 60) == round(row['schedule_end_time'].total_seconds() / 60)
    if date_check and start_time_check and end_time_check:
        return "Rendered Exactly"
    else:
        return "Minute for Minute"

merged_df['rendered_status'] = merged_df.apply(check_minute_for_minute, axis=1)

rendered_summary = merged_df.groupby('employee_id').agg(
    total_appointments=('rendered_status', 'count'),
    rendered_exactly_count=('rendered_status', lambda x: (x == "Rendered Exactly").sum())
).reset_index()

rendered_summary['rendered_exactly_pct'] = (rendered_summary['rendered_exactly_count'] / rendered_summary['total_appointments']) * 100

high_rendered_employees = rendered_summary[rendered_summary['rendered_exactly_pct'] > 50]['employee_id']


rendered_exact_df = merged_df[
    (merged_df['employee_id'].isin(high_rendered_employees)) &
    (merged_df['rendered_status'] == 'Rendered Exactly')
][['employee_id', 'rendered_date']]

rendered_exact_df = rendered_exact_df.rename(columns={'rendered_date': 'date'})
rendered_exact_df['violation'] = 'Rendered as Scheduled'

rendered_exact_df = rendered_exact_df.merge(employee_df[['employee_id', 'employee_zone']], on='employee_id', how='left')
rendered_exact_df.rename(columns={'employee_zone': 'zone'}, inplace=True)

combined_violations = pd.concat([break_violations_df, rendered_exact_df], ignore_index=True)

combined_violations = combined_violations.sort_values(['date', 'employee_id']).reset_index(drop=True)

output_path = r'C:\Users\madel\Desktop\Data Portfolio\Labor Law Compliance\labor_law_violations_combined.xlsx'
combined_violations.to_excel(output_path, index=False, sheet_name='Violations')

print(f"Combined violations data exported with {len(combined_violations)} records to:\n{output_path}")
