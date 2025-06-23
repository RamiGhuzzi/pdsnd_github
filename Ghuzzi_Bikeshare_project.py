import time
import pandas as pd
import sys
import calendar
import numpy as np


CITY_DATA = { 
    'chicago': 'chicago.csv',
    'new york': 'new_york_city.csv',
    'washington': 'washington.csv' }

def CMD_Data():
    """
    Asks user to specify a city, month, and day to analyze with robust input handling.
    Allows exiting at any prompt.
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    print('Type "exit" at any time to quit the program.\n')

    # Get city input 
    while True:
        city = input('Would you like to see data for Chicago, New York, or Washington?\n').lower().strip()
        if city == 'exit':
            sys.exit("Goodbye! Thanks for using the bikeshare analysis.")
        elif city in CITY_DATA:
            break
        else:
            print("Sorry, we currently only have data for Chicago. Please try again.")

    # Get month input with validation
    while True:
        month = input("\nWhich month? (all, january, february, march, april, may, june)\n"
                     "Enter 'all' for no month filter: ").lower()
        if month == 'exit':
            sys.exit("Goodbye! Thanks for using the bikeshare analysis.")
        elif month in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            break
        else:
            print("That's not a valid month option. Please try again.")

    # Get day input with validation
    while True:
        day = input("\nWhich day? (all, monday, tuesday, wednesday, thursday, friday, saturday, sunday)\n"
                   "Enter 'all' for no day filter: ").lower()
        if day == 'exit':
            sys.exit("Goodbye! Thanks for using the bikeshare analysis.")
        elif day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            break
        else:
            print("That's not a valid day option. Please try again.")

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """Loads and filters data with error handling."""
    try:
        df = pd.read_csv(f"./{CITY_DATA[city]}")
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['month'] = df['Start Time'].dt.month
        df['day_of_week'] = df['Start Time'].dt.day_name()

        if month != 'all':
            months = ['january', 'february', 'march', 'april', 'may', 'june']
            month = months.index(month) + 1
            df = df[df['month'] == month]

        if day != 'all':
            df = df[df['day_of_week'] == day.title()]

        return df
    except Exception as e:
        print(f"\nError loading data: {e}")
        sys.exit("Program terminated due to data loading error.")

def display_data(df):
    """Displays raw data with exit option."""
    start_loc = 0
    while True:
        view_data = input("\nWould you like to view 5 rows of individual trip data? (yes/no/exit): ").lower()
        
        if view_data == 'exit':
            sys.exit("Goodbye! Thanks for using the bikeshare analysis.")
        elif view_data == 'no':
            break
        elif view_data == 'yes':
            print(df.iloc[start_loc:start_loc+5])
            start_loc += 5
        else:
            print("Invalid input. Please enter 'yes', 'no', or 'exit'.")

def time_stats(df):
    """Displays time statistics with error handling."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    try:
        # Most common month
        if 'month' in df:
            popular_month = df['month'].mode()[0]
            months = ['January', 'February', 'March', 'April', 'May', 'June']
            print('Most common month:', months[popular_month-1])
        
        # Most common day of week
        if 'day_of_week' in df:
            popular_day = df['day_of_week'].mode()[0]
            print('Most common day of week:', popular_day)
        
        # Most common start hour
        df['hour'] = df['Start Time'].dt.hour
        popular_hour = df['hour'].mode()[0]
        print('Most common start hour:', popular_hour)
    except Exception as e:
        print(f"Error calculating time stats: {e}")

    print("\nThis took %.2f seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays station statistics with error handling."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    try:
        # Most common start station
        popular_start = df['Start Station'].mode()[0]
        print('Most commonly used start station:', popular_start)
        
        # Most common end station
        popular_end = df['End Station'].mode()[0]
        print('Most commonly used end station:', popular_end)
        
        # Most common trip
        df['Trip'] = df['Start Station'] + ' to ' + df['End Station']
        popular_trip = df['Trip'].mode()[0]
        print('Most frequent trip:', popular_trip)
    except Exception as e:
        print(f"Error calculating station stats: {e}")

    print("\nThis took %.2f seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays trip duration statistics with error handling."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    try:
        # Total travel time
        total_time = df['Trip Duration'].sum()
        print('Total travel time: %.2f seconds (%.2f hours)' % (total_time, total_time/3600))
        
        # Mean travel time
        mean_time = df['Trip Duration'].mean()
        print('Mean travel time: %.2f seconds (%.2f minutes)' % (mean_time, mean_time/60))
    except Exception as e:
        print(f"Error calculating duration stats: {e}")

    print("\nThis took %.2f seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays user statistics with error handling."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    try:
        # User types
        user_types = df['User Type'].value_counts()
        print('User types:\n', user_types)
        
        # Gender data (if available)
        if 'Gender' in df:
            gender_counts = df['Gender'].value_counts()
            print('\nGender counts:\n', gender_counts)
        else:
            print("\nGender information not available.")
        
        # Birth year data (if available)
        if 'Birth Year' in df:
            print('\nBirth Year statistics:')
            print('Earliest:', int(df['Birth Year'].min()))
            print('Most recent:', int(df['Birth Year'].max()))
            print('Most common:', int(df['Birth Year'].mode()[0]))
        else:
            print("\nBirth year information not available.")
    except Exception as e:
        print(f"Error calculating user stats: {e}")

    print("\nThis took %.2f seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        try:
            city, month, day = CMD_Data()
            df = load_data(city, month, day)
            #Clean data by dropping the null values
            df.dropna(inplace=True) 
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            display_data(df)

            while True:
                restart = input('\nWould you like to restart? (yes/no/exit): ').lower()
                if restart == 'exit':
                    sys.exit("Goodbye! Thanks for using the bikeshare analysis.")
                elif restart in ['yes', 'no']:
                    break
                else:
                    print("Invalid input. Please enter 'yes', 'no', or 'exit'.")
            
            if restart != 'yes':
                print("Goodbye! Thanks for using the bikeshare analysis.")
                break

        except KeyboardInterrupt:
            sys.exit("\nProgram terminated by user.")
        # Error Handling
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            print("Restarting the program...\n")

if __name__ == "__main__":
    main()