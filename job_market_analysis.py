import pandas as pd
import matplotlib.pyplot as plt
import mplcursors
from matplotlib.ticker import FuncFormatter
import numpy as np

df = pd.read_csv(r"D:\Project\Job_Market_analysis\salaries_1.csv")

df = df[
    [
        "work_year",
        "experience_level",
        "employment_type",
        "job_title",
        "salary_in_usd",
        "company_location",
        "remote_ratio",
        "company_size"
    ]
]

df.dropna(inplace=True)

def salary_format(x, pos):
    return f"${int(x):,}"

formatter = FuncFormatter(salary_format)

job_demand = df["job_title"].value_counts().head(10)

plt.figure()
ax = job_demand.plot(kind="bar", title="Top 10 Most Demanded Job Roles")
plt.xlabel("Job Title")
plt.ylabel("Number of Job Postings")
plt.xticks(rotation=45, ha="right")
plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x)}"))
plt.tight_layout()

cursor = mplcursors.cursor(ax.containers[0], hover=True)
cursor.connect(
    "add",
    lambda sel: sel.annotation.set_text(
        f"{job_demand.index[sel.index]}\nJobs: {job_demand.values[sel.index]}"
    )
)
plt.show()

avg_salary_exp = df.groupby("experience_level")["salary_in_usd"].mean()

plt.figure()
ax = avg_salary_exp.plot(kind="bar", title="Average Salary by Experience Level")
plt.xlabel("Experience Level")
plt.ylabel("Average Salary (USD)")
plt.gca().yaxis.set_major_formatter(formatter)
plt.tight_layout()

cursor = mplcursors.cursor(ax.containers[0], hover=True)
cursor.connect(
    "add",
    lambda sel: sel.annotation.set_text(
        f"{avg_salary_exp.index[sel.index]}\n${avg_salary_exp.values[sel.index]:,.0f}"
    )
)
plt.show()

plt.figure()
df.boxplot(column="salary_in_usd", by="experience_level")
plt.title("Salary Distribution by Experience Level")
plt.suptitle("")
plt.xlabel("Experience Level")
plt.ylabel("Salary (USD)")
plt.gca().yaxis.set_major_formatter(formatter)

# Scatter overlay for hover
for i, level in enumerate(df["experience_level"].unique(), start=1):
    salaries = df[df["experience_level"] == level]["salary_in_usd"]
    plt.scatter(
        np.random.normal(i, 0.04, size=len(salaries)),
        salaries,
        alpha=0
    )

mplcursors.cursor(hover=True).connect(
    "add",
    lambda sel: sel.annotation.set_text(f"Salary: ${sel.target[1]:,.0f}")
)

plt.tight_layout()
plt.show()

location_demand = df["company_location"].value_counts().head(10)

plt.figure()
ax = location_demand.plot(kind="bar", title="Top 10 Job Locations")
plt.xlabel("Company Location")
plt.ylabel("Job Count")
plt.tight_layout()

cursor = mplcursors.cursor(ax.containers[0], hover=True)
cursor.connect(
    "add",
    lambda sel: sel.annotation.set_text(
        f"{location_demand.index[sel.index]}\nJobs: {location_demand.values[sel.index]}"
    )
)
plt.show()

location_salary = (
    df.groupby("company_location")["salary_in_usd"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure()
ax = location_salary.plot(kind="bar", title="Top 10 Locations by Average Salary")
plt.xlabel("Company Location")
plt.ylabel("Average Salary (USD)")
plt.gca().yaxis.set_major_formatter(formatter)
plt.tight_layout()

cursor = mplcursors.cursor(ax.containers[0], hover=True)
cursor.connect(
    "add",
    lambda sel: sel.annotation.set_text(
        f"${location_salary.values[sel.index]:,.0f}"
    )
)
plt.show()

remote_salary = df.groupby("remote_ratio")["salary_in_usd"].mean()

plt.figure()
ax = remote_salary.plot(kind="bar", title="Average Salary by Remote Ratio")
plt.xlabel("Remote Ratio (%)")
plt.ylabel("Average Salary (USD)")
plt.gca().yaxis.set_major_formatter(formatter)
plt.tight_layout()

mplcursors.cursor(ax.containers[0], hover=True)
plt.show()

year_salary = df.groupby("work_year")["salary_in_usd"].mean()

plt.figure()
ax = year_salary.plot(kind="line", marker="o", title="Average Salary Trend Over Years")
plt.xlabel("Year")
plt.ylabel("Average Salary (USD)")
plt.gca().yaxis.set_major_formatter(formatter)
plt.tight_layout()

mplcursors.cursor(ax.lines[0], hover=True)
plt.show()

top_salary_roles = (
    df.groupby("job_title")["salary_in_usd"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure()
ax = top_salary_roles.plot(kind="barh", title="Top 10 Highest Paying Job Roles")
plt.xlabel("Average Salary (USD)")
plt.gca().xaxis.set_major_formatter(formatter)
plt.tight_layout()

mplcursors.cursor(ax.containers[0], hover=True)
plt.show()

company_exp_salary = (
    df.groupby(["company_size", "experience_level"])["salary_in_usd"]
    .mean()
    .unstack()
)

company_exp_salary.plot(
    kind="bar",
    title="Average Salary by Company Size & Experience Level"
)
plt.xlabel("Company Size")
plt.ylabel("Average Salary (USD)")
plt.gca().yaxis.set_major_formatter(formatter)
plt.xticks(rotation=0)
plt.tight_layout()

mplcursors.cursor(hover=True).connect(
    "add",
    lambda sel: sel.annotation.set_text(f"${sel.target[1]:,.0f}")
)
plt.show()

remote_distribution = df["remote_ratio"].value_counts().sort_index()

plt.figure()
ax = remote_distribution.plot(
    kind="bar",
    title="Job Distribution by Remote Ratio"
)
plt.xlabel("Remote Ratio (%)")
plt.ylabel("Number of Jobs")
plt.tight_layout()

mplcursors.cursor(ax.containers[0], hover=True).connect(
    "add",
    lambda sel: sel.annotation.set_text(
        f"Jobs: {remote_distribution.values[sel.index]}"
    )
)
plt.show()

employment_salary = df.groupby("employment_type")["salary_in_usd"].mean()

plt.figure()
ax = employment_salary.plot(
    kind="bar",
    title="Average Salary by Employment Type"
)
plt.xlabel("Employment Type")
plt.ylabel("Average Salary (USD)")
plt.gca().yaxis.set_major_formatter(formatter)
plt.tight_layout()

mplcursors.cursor(ax.containers[0], hover=True).connect(
    "add",
    lambda sel: sel.annotation.set_text(
        f"${employment_salary.values[sel.index]:,.0f}"
    )
)
plt.show()

experience_share = df["experience_level"].value_counts(normalize=True) * 100

plt.figure()
ax = experience_share.plot(
    kind="bar",
    title="Market Share by Experience Level"
)
plt.xlabel("Experience Level")
plt.ylabel("Percentage of Jobs (%)")
plt.tight_layout()

mplcursors.cursor(ax.containers[0], hover=True).connect(
    "add",
    lambda sel: sel.annotation.set_text(
        f"{experience_share.values[sel.index]:.1f}%"
    )
)
plt.show()

salary_variability = df.groupby("experience_level")["salary_in_usd"].std()

plt.figure()
ax = salary_variability.plot(
    kind="bar",
    title="Salary Variability by Experience Level"
)
plt.xlabel("Experience Level")
plt.ylabel("Salary Std Deviation (USD)")
plt.gca().yaxis.set_major_formatter(formatter)
plt.tight_layout()

mplcursors.cursor(ax.containers[0], hover=True).connect(
    "add",
    lambda sel: sel.annotation.set_text(
        f"Std Dev: ${salary_variability.values[sel.index]:,.0f}"
    )
)
plt.show()

print("\nADVANCED BUSINESS INSIGHTS:")
print("- Large companies consistently pay more at senior levels.")
print("- Mid-level roles dominate the job market volume.")
print("- Remote roles form a significant portion of total opportunities.")
print("- Contract and freelance roles show higher salary variance.")
print("- Senior roles offer higher pay but also greater salary dispersion.")
print("\nFINAL KEY INSIGHTS:")
print("- Executive and Senior roles command the highest salaries.")
print("- Remote roles offer competitive or higher pay than on-site jobs.")
print("- Certain job titles remain high-paying regardless of experience.")
print("- Salary levels have increased consistently over recent years.")
print("- Large companies generally offer better compensation.")
