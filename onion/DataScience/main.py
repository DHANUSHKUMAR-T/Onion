import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns

# ThingSpeak API URL (Ensure the API Key is correct)
url = "https://thingspeak.mathworks.com/channels/2864954/feed.json?api_key=2QHEX8CPIVDRY0WN"

# Make the API request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    try:
        data = response.json()
        
        # Validate the presence of 'feeds'
        if "feeds" in data and data["feeds"]:
            feeds = data["feeds"]
            
            # Convert to DataFrame
            df = pd.DataFrame(feeds)

            # Convert 'created_at' to datetime
            df['created_at'] = pd.to_datetime(df['created_at'])
            df.set_index('created_at', inplace=True)

            # Convert numerical fields to float
            for col in df.columns:
                if col.startswith("field"):  
                    df[col] = pd.to_numeric(df[col], errors='coerce')

            # Print DataFrame summary
            print("✅ Data Loaded Successfully!\n")
            print(df.info())  # Print DataFrame structure
            print(df.head())  # Print first few rows
            
        else:
            print("❌ Error: 'feeds' key is missing or empty in the response.")
    
    except ValueError:
        print("❌ Error: Failed to parse JSON response.")
else:
    print(f"❌ API request failed with status code {response.status_code}.")
    print("Response Text:", response.text)  # Debugging output

plt.style.use('ggplot')  # Alternative built-in Matplotlib style


# Plot Time Series Data (Field1 over time)
plt.figure(figsize=(12, 6))
for col in df.columns:
    if col.startswith("field"):  
        plt.plot(df.index, df[col], label=col)

plt.xlabel("Timestamp")
plt.ylabel("Sensor Values")
plt.title("Sensor Data Over Time")
plt.legend()
plt.xticks(rotation=45)
plt.show()

# Scatter Plot (Example: Field1 vs Field2)
plt.figure(figsize=(8, 5))
sns.scatterplot(x=df["field1"], y=df["field2"])
plt.xlabel("Field1")
plt.ylabel("Field2")
plt.title("Scatter Plot: Field1 vs Field2")
plt.show()

# Bar Chart (Mean values of each field)
df.mean().plot(kind="bar", figsize=(10, 6), color="skyblue", edgecolor="black")
plt.title("Average Sensor Values")
plt.ylabel("Mean Value")
plt.xticks(rotation=45)
plt.show()