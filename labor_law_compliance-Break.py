import pandas as pd

file_path = r'C:\Users\madel\Desktop\Data Portfolio\Labor Law Compliance\labor_law_01-2025.xlsx'

schedule_df = pd.read_excel(file_path, sheet_name='schedule_data')
employee_df = pd.read_excel(file_path, sheet_name='employee_data')

merged_df = pd.merge(schedule_df, employee_df, on='employee_id', how='left')

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

for col in ['rendered_start_time', 'rendered_end_time']:
    merged_df[col] = merged_df[col].apply(convert_to_timedelta)

daily_reports = []

grouped = merged_df.groupby(['employee_id', 'rendered_date'])

for (emp_id, date), group in grouped:
    group_sorted = group.sort_values('rendered_start_time')
    total_hours = group_sorted['duration_rendered_hours'].sum()
    num_sessions = len(group_sorted)

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
        max_break_all = max([b['break_duration'] for b in breaks])
    else:
        max_break_before_fifth = pd.Timedelta(0)
        max_break_all = pd.Timedelta(0)


    violation = "Violation" if (total_hours > 5 and max_break_before_fifth < pd.Timedelta(minutes=30)) else ""

    daily_reports.append({
        'employee_id': emp_id,
        'rendered_date': date,
        'num_sessions': num_sessions,
        'total_hours': round(total_hours, 2),
        'start_time': first_start,
        'fifth_hour': fifth_hour,
        'max_break_before_fifth_hour': max_break_before_fifth,
        'max_break_all_day': max_break_all,
        'violation': violation
    })

def format_timedelta(td):
    if pd.isnull(td):
        return ""
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    return f"{hours:02}:{minutes:02}"

def format_time_only(td):
    if pd.isnull(td):
        return ""
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    return f"{hours:02}:{minutes:02}"

summary_df = pd.DataFrame(daily_reports)
summary_df['max_break_before_fifth_hour'] = summary_df['max_break_before_fifth_hour'].apply(format_timedelta)
summary_df['max_break_all_day'] = summary_df['max_break_all_day'].apply(format_timedelta)
summary_df['start_time'] = summary_df['start_time'].apply(format_time_only)
summary_df['fifth_hour'] = summary_df['fifth_hour'].apply(format_time_only)

total_employees_by_zone = employee_df.groupby('employee_zone')['employee_id'].nunique().reset_index()
total_employees_by_zone.columns = ['employee_zone', 'total_employees']
violations_only = summary_df[summary_df['violation'] == 'Violation']
employees_with_violations = summary_df[summary_df['violation'] == 'Violation']['employee_id'].nunique()

violations_with_zone = pd.merge(violations_only, employee_df[['employee_id', 'employee_zone']], on='employee_id', how='left')
employees_with_violations_by_zone = violations_with_zone.groupby('employee_zone')['employee_id'].nunique().reset_index()
employees_with_violations_by_zone.columns = ['employee_zone', 'employees_with_violations']
zone_compliance = pd.merge(total_employees_by_zone, employees_with_violations_by_zone, on='employee_zone', how='left')
zone_compliance['employees_with_violations'] = zone_compliance['employees_with_violations'].fillna(0)
zone_compliance['violation_pct'] = (zone_compliance['employees_with_violations'] / zone_compliance['total_employees']) * 100
zone_compliance['violation_pct'] = zone_compliance['violation_pct'].round(2)

print(violations_only.head())
print("Total Violations Found:", len(violations_only))
print(f"Total employees with violations: {employees_with_violations}")
print("\nPercentage of employees with violations by zone:")
print(zone_compliance[['employee_zone', 'employees_with_violations', 'total_employees', 'violation_pct']])

output_path = r'C:\Users\madel\Desktop\Data Portfolio\Labor Law Compliance\break_violation_summary.xlsx'
with pd.ExcelWriter(output_path) as writer:
    summary_df.to_excel(writer, sheet_name='Daily Summary', index=False)
    violations_only.to_excel(writer, sheet_name='Violations Only', index=False)
    zone_compliance.to_excel(writer, sheet_name='Zone Compliance', index=False)

