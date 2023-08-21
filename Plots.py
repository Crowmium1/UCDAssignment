import matplotlib.pyplot as plt

# Calculate summary statistics
temp_mean = combined_data['avgtemp_c'].mean()
pm25_mean = combined_data['pm2.5'].mean()
pm10_mean = combined_data['pm10'].mean()

temp_std = combined_data['avgtemp_c'].std()
pm25_std = combined_data['pm2.5'].std()
pm10_std = combined_data['pm10'].std()

# Create the figure and axis objects
fig, ax1 = plt.subplots(figsize=(10, 6))

# Set the title and axis labels
ax1.set_title("Weather and Pollutant Trends over Time")
ax1.set_xlabel("Time (Days)")
ax1.set_ylabel("Degrees Celsius")

# Add a grid
ax1.grid(True)

# Create a line plot for avg_temp
ax1.plot(combined_data.index, combined_data['avgtemp_c'], color="g", marker="o", linestyle="-", label='Avg_Temp')

# Add a legend for avg_temp
ax1.legend(loc="upper right")

# Create a second y-axis for pollutants
ax2 = ax1.twinx()
ax2.set_ylabel("Pollutant Quantity")

# Create a line plot for pm2.5
ax2.plot(combined_data.index, combined_data['pm2.5'], marker="^", linestyle=":", label="PM2.5")

# Create a line plot for pm10
ax2.plot(combined_data.index, combined_data['pm10'], marker="v", linestyle=":", label="PM10")

# Add a legend for pollutants
ax2.legend(loc="upper right", bbox_to_anchor=(1.0, 0.94))

# Add summary statistics to the plot
summary = f"Temp Mean: {temp_mean:.2f} \nTemp Std: {temp_std:.2f} \nPM2.5 Mean: {pm25_mean:.2f} " \
          f"\nPM2.5 Std: {pm25_std:.2f} \nPM10 Mean: {pm10_mean:.2f} \nPM10 Std: {pm10_std:.2f}"
ax1.text(0.005, 0.78, summary, transform=ax1.transAxes, bbox=dict(facecolor='white', alpha=0.5))

# Show the plot
plt.show()

# Create the figure and axis objects
fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))

# Set the title and axis labels for each subplot
axs[0, 0].set_title("Pollutants Vs. Time")
axs[0, 0].set_xlabel("Time (days)")
axs[0, 0].set_ylabel("Pollutants (ppm)")

axs[0, 1].set_title("Wind Speed vs. PM2.5")
axs[0, 1].set_xlabel("Time (days)")
axs[0, 1].set_ylabel("Wind Speed (m/s)")
axs[0, 1].twinx().set_ylabel("PM2.5 (ppm)")

axs[1, 0].set_title("Temperature vs. PM10")
axs[1, 0].set_xlabel("Time (days)")
axs[1, 0].set_ylabel("Temperature (C)")
axs[1, 0].twinx().set_ylabel("PM10 (ppm)")

axs[1, 1].set_title("Humidity vs. NO3")
axs[1, 1].set_xlabel("Time (days)")
axs[1, 1].set_ylabel("Humidity (%)")
axs[1, 1].twinx().set_ylabel("NO3 (ppm)")

# Plot the data on each subplot
combined_data.plot(ax=axs[0, 0], x="day", y=["pm2.5", "pm10", "NO3"], color=["purple", "orange", "red"])
combined_data.plot(ax=axs[0, 1], x="day", y="maxwind_kph", color="green")
combined_data.plot(ax=axs[1, 0], x="day", y="avgtemp_c", color="green")
combined_data.plot(ax=axs[1, 1], x="day", y="avghumidity", color="green")

# Add extra lines corresponding to the secondary y-axis
combined_data.plot(ax=axs[0, 1].twinx(), x="day", y="pm2.5", color="purple")
combined_data.plot(ax=axs[1, 0].twinx(), x="day", y="pm10", color="orange")
combined_data.plot(ax=axs[1, 1].twinx(), x="day", y="NO3", color="red")

# Set the legend position and color for each subplot
axs[0, 0].legend(loc="upper left", bbox_to_anchor=(0.5, 1.05), ncol=2)
axs[0, 1].legend(loc="upper left", bbox_to_anchor=(0, 1.05), ncol=2)
axs[1, 0].legend(loc="upper left", bbox_to_anchor=(0.5, 1.05), ncol=2)
axs[1, 1].legend(loc="upper left", bbox_to_anchor=(0.5, 1.05), ncol=2)

# Add space between subplots
fig.tight_layout()

# Display the plot
plt.show()

