import tkinter as tk
from tkinter import messagebox
import random


# Function to create a camp schedule with variable activities per day
def create_camp_schedule(num_groups, group_rankings, group_activities_per_day):
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Initialize the schedule with empty lists for each day of the week
    schedule = {day: [[] for _ in range(num_groups)] for day in days_of_week}

    # Track which activities are used by each cabin to avoid repetition
    used_activities_by_cabin = [set() for _ in range(num_groups)]

    # Assign activities to the schedule, respecting preferences and avoiding repetition
    for day in days_of_week:
        used_activities_per_day = set()  # Ensure activities are unique across all groups on each day

        for group in range(num_groups):
            if day not in group_activities_per_day[group]:
                continue  # Skip groups not scheduled for this day

            activities_per_day = group_activities_per_day[group][day]
            group_ranking = group_rankings[group]
            assigned_activities = []
            
            # Find unique activities not used by this cabin and not used on this day
            for activity in group_ranking:
                if activity not in used_activities_per_day and activity not in used_activities_by_cabin[group]:
                    assigned_activities.append(activity)
                    used_activities_per_day.add(activity)
                    used_activities_by_cabin[group].add(activity)
                    if len(assigned_activities) == activities_per_day:
                        break

            # Assign these activities to the cabin's schedule for the current day
            schedule[day][group] = assigned_activities

    return schedule


# Function to handle form submission and generate the schedule
def submit_preferences():
    try:
        num_groups = int(groups_entry.get())
        
        group_rankings = []
        # Collect activity rankings from the text entries
        for group_entry in group_rankings_entries:
            ranking_text = group_entry.get()
            group_rankings.append([item.strip() for item in ranking_text.split(",")])
        
        group_activities_per_day = []
        # Collect the specified days and number of activities per day for each group
        for group_activities_per_day_entry in group_activities_per_day_entries:
            activities_per_day_by_day = {}
            activities_per_day_text = group_activities_per_day_entry.get()
            if activities_per_day_text:
                activities_per_day_pairs = activities_per_day_text.split(",")
                for pair in activities_per_day_pairs:
                    try:
                        day, count = pair.split(":")
                        day = day.strip().capitalize()
                        count = int(count.strip())
                        if day not in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
                            raise ValueError("Invalid day specified")
                        activities_per_day_by_day[day] = count
                    except (ValueError, IndexError):
                        raise ValueError("Invalid format. Use 'Day: Number' format, e.g., 'Monday: 2'.")
            group_activities_per_day.append(activities_per_day_by_day)
        
        # Validate that each group has at least one valid day specified
        if any(not activities_per_day for activities_per_day in group_activities_per_day):
            raise ValueError("Each group must have at least one specified day.")

        # Generate the camp schedule based on the group activities per day
        camp_schedule = create_camp_schedule(
            num_groups, group_rankings, group_activities_per_day
        )

        # Display the generated camp schedule
        schedule_text = "Camp Schedule:\n"
        for day, daily_schedule in camp_schedule.items():
            if any(daily_schedule):
                schedule_text += f"{day}:\n"
                for group, activities in enumerate(daily_schedule):
                    if activities:
                        activities_str = ", ".join(activities)
                        schedule_text += f"  Cabin {group + 1}: {activities_str}\n"
        
        messagebox.showinfo("Camp Schedule", schedule_text)
    
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# Create the main GUI window
root = tk.Tk()
root.title("Camp Activity Schedule Generator")

# Main frame for layout organization
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

# Frame to hold input fields for the number of groups
top_frame = tk.Frame(main_frame)
top_frame.pack()

# Input field for the number of groups
tk.Label(top_frame, text="Number of groups (cabins):").pack()
groups_entry = tk.Entry(top_frame)
groups_entry.pack()

# Create a canvas with a scrollbar for group entries
canvas = tk.Canvas(main_frame)
scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

# Configure the canvas to use the scrollbar
canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(fill="both", expand=True)

# Create a frame inside the canvas to hold the group entries
group_entries_frame = tk.Frame(canvas)

# Bind the frame to the canvas
canvas.create_window((0, 0), window=group_entries_frame, anchor="nw")

# Ensure the canvas scroll region updates when new content is added
def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

group_entries_frame.bind("<Configure>", on_frame_configure)

# Button to create group entries
def create_group_entries():
    # Clear existing entries in the group_entries_frame
    for widget in group_entries_frame.winfo_children():
        widget.destroy()

    num_groups = int(groups_entry.get())
    
    global group_rankings_entries
    group_rankings_entries = []

    global group_activities_per_day_entries
    group_activities_per_day_entries = []

    # Create text entry fields for each group's activity preferences and specified days with activities per day
    for i in range(num_groups):
        tk.Label(group_entries_frame, text=f"Group {i + 1} activity preferences (comma-separated):").pack()
        group_ranking_entry = tk.Entry(group_entries_frame)
        group_ranking_entry.pack()
        group_rankings_entries.append(group_ranking_entry)

        tk.Label(group_entries_frame, text=f"Group {i + 1} specified days and activities (e.g., Monday: 2, Wednesday: 3):").pack()
        group_activities_per_day_entry = tk.Entry(group_entries_frame)
        group_activities_per_day_entry.pack()
        group_activities_per_day_entries.append(group_activities_per_day_entry)


# Button to create group entries
create_entries_button = tk.Button(top_frame, text="Create Group Entries", command=create_group_entries)
create_entries_button.pack()

# Button to submit the preferences and generate the schedule
submit_button = tk.Button(main_frame, text="Generate Schedule", command=submit_preferences)
submit_button.pack(pady=10)

# Start the main event loop
root.mainloop()
