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

## Findings and Recommendations 
In the first iteration of this project, we only used one pay period's worth of data. The dataset has been artificially expanded to include a full 6 months. Accurate, minute-for-minute timekeeping is essential for labor law compliance and fair compensation. 
### Overall

#### ADD CHART
Labor Law noncompliance, specifically with missed break periods, is a problem in this healthcare company.
The missed breaks are constant but show variation across regions.
Investment in law labor compliance coaching will address the problem and is actually cheaper than the cost of a major law suit.

### Over the initial two-week pay period (Jan 1–15):
- 21.4% of employees (72 individuals) missed a legally required break, totaling 144 violations.
These findings suggest systemic scheduling or time reporting issues that could expose the company to labor law risks (e.g., fines or lawsuits).
- By employee_zone, SD North Coastal had the highest violation rate (44.4%), despite having significantly fewer staff than SD South (18.2%).
- Five of the twelve regions showed above-average violation rates:
  - IE Temecula
  - LA
  - OC Capistrano
  - SD North Coastal
  - SD North Inland <br>
- These zones may warrant targeted audits or training, though further analysis across multiple pay periods is recommended to confirm persistent trends.
- 76% of the workforce (256 employees) rendered more than half of their appointments exactly as scheduled — rather than clocking in minute-for-minute.
While this may look compliant on paper, it can mask the actual time worked and expose the company to labor law risks.
- On average, 83.8% of employees per zone showed high levels of noncompliance with minute-for-minute accuracy.
  - Notably, the Inland and LA regions had 100% of employees rendering time exactly as scheduled.
- This suggests a cultural or operational habit of recording expected time rather than actual time worked.

## Next Steps
1. Repeat process across multiple pay periods.
2. Create updating dashboard to share with payroll and compliance departments.
3. Identify root causes through targeted analysis of individuals with high rates. 
