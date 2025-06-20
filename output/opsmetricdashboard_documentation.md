# OpsMetricDashboard Documentation

## Overview

The OpsMetricDashboard is a comprehensive business intelligence tool designed to provide insights into various operational metrics within an organization. It leverages data from multiple sources to present key performance indicators (KPIs) and trends that help in making informed decisions. The dashboard is highly interactive, allowing users to filter and drill down into specific data points.

## Key Performance Indicators (KPIs) and Charts

### 1. Lots Assigned
   - **Description**: Displays the total number of lots assigned within the selected date range.
   - **Purpose**: Helps in tracking the workload and distribution of tasks within the facility.

### 2. Transport
   - **Description**: Shows the number of transports arranged for lots.
   - **Purpose**: Useful for logistics and planning, ensuring efficient movement of goods.

### 3. Owner Retained
   - **Description**: Indicates the number of lots retained by the owner.
   - **Purpose**: Important for understanding customer retention and satisfaction.

### 4. Lots Cancelled
   - **Description**: Counts the lots that have been cancelled.
   - **Purpose**: Assists in identifying issues in operations that may lead to cancellations.

### 5. DOL to Assigned Avg Bus Days
   - **Description**: Average business days from Date of Loss to assignment.
   - **Purpose**: Measures efficiency in the assignment process post-incident reporting.

### 6. Assigned to First Contact Avg Bus Hours
   - **Description**: Average business hours taken to make the first contact after assignment.
   - **Purpose**: Helps in evaluating the responsiveness of the team.

### 7. Assigned to Cleared Avg Bus Days
   - **Description**: Average business days taken from assignment to clearance of lots.
   - **Purpose**: Critical for assessing the speed of operations and clearance rates.

### 8. Gross Assignments
   - **Description**: Total assignments handled, irrespective of their current status.
   - **Purpose**: Provides a gross overview of operational volume.

## Filters and Their Usage

### Date Range
   - **Description**: Allows selection of start and end dates to focus the dashboard data on a specific period.
   - **Purpose**: Tailors the displayed data to the time frame of interest for better decision-making.

### Yard ID, Country ID, Division ID, Region ID
   - **Description**: Filters to narrow down data based on specific yards, countries, divisions, or regions.
   - **Purpose**: Useful for regional managers or specific yard analysis to localize the data insights.

### Additional Filters
   - **Segment, Division, Region, State, Facility Name, Virtual Sale Location, Business Unit, Lot Type, Loss Type, Tow Type, Seller Company Code, Seller Type, Category Type**
   - **Purpose**: These filters provide more granular control over the data, allowing users to drill down into very specific areas of interest.

## Data Source and Logic

### General Structure
   - **Source**: Data is primarily pulled from the `cprtpr-dataplatform-sp1.usmart` database using SQL queries.
   - **Integration**: Data is fetched and processed through SQL queries embedded within the dashboard components. These queries often include parameters linked to the dashboard filters to provide dynamic data retrieval based on user input.

### Example Query
   - **Purpose**: Fetch the number of lots assigned.
   - **Query**:
     ```sql
     SELECT SUM(lots_assigned) AS col1
     FROM `cprtpr-dataplatform-sp1`.usmart.fact_lots_ops_opt
     WHERE assg_dt BETWEEN ${startDate} AND ${endDate}
     ```
   - **Description**: This query calculates the total lots assigned between user-specified start and end dates.

This documentation should assist users in navigating and utilizing the OpsMetricDashboard effectively to analyze operational data and derive actionable insights.
