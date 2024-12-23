#!/usr/bin/env bash

# Function to check if the current time is between the given start and end hours in the specified timezone
is_time_in_range() {
    local start_hour=$1
    local end_hour=$2
    local timezone=$3
    local current_hour=$(TZ="$timezone" date +%H)

    if [ "$current_hour" -ge "$start_hour" ] && [ "$current_hour" -lt "$end_hour" ]; then
        return 0
    else
        return 1
    fi
}

# Infinite loop to keep repeating the script execution
while true; do
    # Check if current time is within the specified range for either Eastern or West Coast time
    if is_time_in_range 1 24 "America/New_York" || is_time_in_range 1 24 "America/Los_Angeles"; then
        # Run the Python scripts in the specified order

        # Array of Python script paths (replace with the actual paths to your scripts)
        PYTHON_SCRIPTS=(
            "./coromoto/v_wp_agent.py"
            
        )

        # Log directory
        LOG_DIR="./logs"
        mkdir -p "$LOG_DIR"

        # Loop through each Python script and execute it sequentially
        for script in "${PYTHON_SCRIPTS[@]}"
        do
            if [ -f "$script" ]; then
                echo "Running $script..."
                python3 "$script" &> "$LOG_DIR/$(basename $script).log"
                if [ $? -ne 0 ]; then
                    echo "Error: Script $script failed. Check log at $LOG_DIR/$(basename $script).log"
                    exit 1
                fi
            else
                echo "Warning: Script $script not found. Skipping."
            fi
        done

        echo "All scripts completed successfully."
    else
        echo "Current time is not within the allowed range. Waiting..."
    fi

    # Wait for a random time between 1 and 3 minutes before the next cycle
    RANDOM_WAIT=$(( (RANDOM % 60 + 30) * 60 ))
    echo "Waiting for $((RANDOM_WAIT / 60)) minutes before the next cycle..."
    sleep $RANDOM_WAIT
done
