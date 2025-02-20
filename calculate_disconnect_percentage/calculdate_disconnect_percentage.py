import re
import os
from datetime import datetime, timedelta
import traceback
import matplotlib.pyplot as plt

def parse_data_file(file_path):
    data_by_date = {}
    current_date = None
    current_region = None
    seen_regions = set()

    try:
        with open(file_path, 'r', encoding='utf8') as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("05:00") or "LINE Notify" in line or "WiSleep" in line:
                    continue  # Ignore empty or dummy lines
                
                # Parse date lines and adjust to the previous day
                date_match = re.match(r'^(\d{4})/(\d{1,2})/(\d{1,2})', line)
                if date_match:
                    year, month, day = map(int, date_match.groups())
                    current_date = datetime(year, month, day) - timedelta(days=1)  # Subtract 1 day
                    current_date = current_date.strftime('%Y-%m-%d')  # Format as 'YYYY-MM-DD'
                    seen_regions = set()  # Reset for the new date
                    if current_date not in data_by_date:
                        data_by_date[current_date] = {}
                    continue  # Move to next line

                if line.startswith("場域:"):
                    current_region = line.split("場域:")[1].strip()
                    if current_region in seen_regions:
                        current_region = None  # Ignore duplicate regions
                    else:
                        seen_regions.add(current_region)
                        if current_date is not None and current_region is not None:
                            data_by_date[current_date][current_region] = []
                elif current_date is not None and current_region is not None:
                    try:
                        match = re.match(r'([\w\d]+)\/([\w\d]+)\/(\w+)\/([\d\.]+)%\/(\d+)次', line)
                        if match:
                            device, location1, location2, uptime_percentage, events_count = match.groups()
                            uptime_percentage = float(uptime_percentage)
                            events_count = int(events_count)
                            date_ranges = []
                            for _ in range(events_count):
                                date_line = next(file).strip()
                                date_match = re.match(
                                    r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) ~ (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})$', date_line)
                                if date_match:
                                    start_date, end_date = date_match.groups()
                                    date_ranges.append((start_date, end_date))
                            data_by_date[current_date][current_region].append(
                                (device, location1, location2, uptime_percentage, date_ranges))
                    except StopIteration:
                        print(f"Parsing error in region {current_region}, line: {line}")
    except FileNotFoundError:
        print("The specified file was not found.")
    except Exception:
        traceback.print_exc()

    return data_by_date

def calculate_disconnect_percentage_per_hour(data):
    output = {}

    for date, regions in data.items():
        output[date] = {}
        for region, devices in regions.items():
            for device_info in devices:
                device, location1, location2, uptime_percentage, date_ranges = device_info

                if uptime_percentage == 0.0:  # (1) Case where entire day is disconnected
                    for date_range in date_ranges:
                        start_datetime = datetime.strptime(date_range[0], '%Y-%m-%d %H:%M:%S')
                        end_datetime = datetime.strptime(date_range[1], '%Y-%m-%d %H:%M:%S')
                        current_datetime = start_datetime
                        while current_datetime < end_datetime:
                            date_key = current_datetime.date()
                            hour_key = current_datetime.hour

                            if date_key not in output[date]:
                                output[date][date_key] = {}
                            if region not in output[date][date_key]:
                                output[date][date_key][region] = {}
                            if device not in output[date][date_key][region]:
                                output[date][date_key][region][device] = {}
                            if location2 not in output[date][date_key][region][device]:
                                output[date][date_key][region][device][location2] = [0] * 24

                            output[date][date_key][region][device][location2][hour_key] += 60  # full hour disconnected
                            current_datetime += timedelta(hours=1)
                else:  # (2) Case with specific disconnection intervals
                    for start_date, end_date in date_ranges:
                        start_datetime = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
                        end_datetime = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')

                        current_datetime = start_datetime
                        while current_datetime < end_datetime:
                            next_datetime = min(current_datetime + timedelta(hours=1), end_datetime)
                            date_key = current_datetime.date()
                            hour_key = current_datetime.hour

                            if date_key not in output[date]:
                                output[date][date_key] = {}
                            if region not in output[date][date_key]:
                                output[date][date_key][region] = {}
                            if device not in output[date][date_key][region]:
                                output[date][date_key][region][device] = {}
                            if location2 not in output[date][date_key][region][device]:
                                output[date][date_key][region][device][location2] = [0] * 24

                            disconnect_minutes = (next_datetime - current_datetime).total_seconds() / 60
                            output[date][date_key][region][device][location2][hour_key] += disconnect_minutes
                            current_datetime = next_datetime

    return output


def print_report(result):
    for date, regions in sorted(result.items()):
        directory = f'reports/{date}'
        os.makedirs(directory, exist_ok=True)
        report_path = os.path.join(directory, f'report_{date}.txt')
        with open(report_path, 'w', encoding='utf8') as report_file:
            report_file.write(f"日期: {date}\n")
            for region, machines in regions.items():
                for date_key, daily_machines in machines.items():
                    report_file.write(f"日期: {date_key}\n")
                    report_file.write(f"場域: {region}\n")
                    for device, locations in daily_machines.items():
                        for location, hourly_disconnect in locations.items():
                            for hour in range(24):
                                disconnect_minutes = hourly_disconnect[hour]
                                disconnect_percentage = (disconnect_minutes / 60) * 100
                                report_file.write(
                                    f"機台: {device}, 地點: {location}, 時間: {hour}:00 ~ {hour + 1}:00, 斷線時間（分鐘）：{disconnect_minutes:.2f}, 斷線比例：{disconnect_percentage:.2f}%\n")
            report_file.write("\n")


def visualize_report(result):
    for date, regions in sorted(result.items()):
        directory = f'reports/{date}'
        os.makedirs(directory, exist_ok=True)
        for region, machines in regions.items():
            for date_key, daily_machines in machines.items():
                for device, locations in daily_machines.items():
                    for location, hourly_disconnect in locations.items():
                        hours = list(range(24))
                        disconnect_percentages = [(min / 60) * 100 for min in hourly_disconnect]
                        plt.figure(figsize=(10, 6))
                        plt.bar(hours, disconnect_percentages, align='center', alpha=0.7)
                        plt.xlabel('Hour of the Day')
                        plt.ylabel('Disconnect Percentage (%)')
                        plt.title(f'Device {device} at {location} on {date_key} - {region}')
                        plt.xticks(hours)
                        plt.grid(True)
                        plt.savefig(
                            os.path.join(directory, f'report_{region}_{device}_{location}_{date_key}.png'),
                            bbox_inches='tight')
                        plt.close()


# Read and parse data
file_path = 'data.txt'
data_by_date = parse_data_file(file_path)

# Calculate disconnect percentage per hour
result = calculate_disconnect_percentage_per_hour(data_by_date)

# Print a text report
print_report(result)

# Generate visual reports
visualize_report(result)
