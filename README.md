# Labor Law Compliance Analysis for Healthcare Company
This project analyzes synthetic employee timecard data to track compliance with key labor laws, focusing on minimum breaks taken before the fifth hour of work and adherence to scheduled work times.

## Executive Summary
To help ensure labor law compliance, this project analyzes employee work data to confirm that schedules are followed accurately and mandatory breaks are taken before the fifth hour of the employee's day. By highlighting scheduling deviations, missed breaks, and inaccurate time reporting, this solution reduces legal risks, improves operational oversight, and supports fair workplace practices. It equips leadership with the insights needed to manage their workforce effectively and maintain compliance with labor regulations.

## Business Impact
Correctly rendered schedules and mandatory breaks are hallmarks of labor law compliance. Incorrectly recorded time or insufficient breaks can lead to legal risks, employee dissatisfaction, and operational inefficiencies. How can we identify employees who have missed their break or rendered time inaccurately? Proper analysis of schedule and timecard data helps prevent potential employee legal actions by ensuring compliance with labor laws. This project aims to highlight potential labor law compliance risks for executive level and scheduling teams by providing a list of employees and high-level overviews of the entire workforce.

## Methodology
Starting with a synthetic excel file from a scheduling system as well as a randomized employee demographics dataset, the project approach involves: <br>
  **Data Integration:** Combining schedule details with actual worked hours for each employee. <br>
  **Time Conversion:** Standardizing time values into a consistent format for easy comparison. <br>
  **Session Analysis:** Grouping daily work sessions to calculate total hours worked, count breaks, and measure break durations. <br>
  **Compliance Checks:** Identifying if employees took mandatory breaks before their fifth hour of work and if their rendered times match their scheduled times. <br>
  **Flagging Violations:** Highlighting employees or days where the rules were not followed, enabling proactive corrections. <br>

## Skills
Excel: Data cleaning through de-duplication, preliminary analysis using pivot tables. <br>
Python: Pandas, datetime module, print to excel. <br>
Tableau: Heatmap, Bar Chart, dashboard design. <br>

## Results and Business Recommendations
Over a two-week pay period, more than 1 in 5 employees (21.4%) missed a legally required break, with 144 violations spread across 72 individuals. These findings suggest systemic scheduling or time reporting issues that could lead to labor law exposure (fines, lawsuits, etc.). Broken down by employee_zone, SD North Coastal saw the highest rate of employees with violations (44.4%) despite having much fewer staff than SD South (18.2%). Five regions showed greater than average rates (IE Temecula, LA, OC Capistrano, SD North Coastal, and SD North Inland), implying the possibilty for targeted audits or coaching sessions in those particular zones, though it would be prudent to examine a much larger dataset to establish trends over time versus a single spike.  

When evaluating how accurately employees recorded their time, the analysis revealed that 76% of the workforce (256 employees) had more than half of their appointments rendered exactly as scheduled. On average, each zone as about 83.8% of their total employees rendered with high noncompliance. Inland and LA regions inparticular have 100% of their employees render exactly as scheduled. This suggests that many employees may not be clocking in and out minute-for-minute, but rather entering time that matches their schedule. While this might appear compliant on paper, it likely masks the true time worked and may expose the organization to labor compliance risks. Accurate, minute-for-minute timekeeping is critical to meeting labor law standards and ensuring employees are compensated fairly for their actual work time.

## Next Steps
1. Repeat process across multiple pay periods.
2. Create updating dashboard to share with payroll and compliance departments.
3. Identify root causes through targeted analysis of individuals with high rates. 
