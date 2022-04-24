#cd /Users/kellydowd/Documents/Udacity/Programming for Data Science with Python/Python Project

import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    cities = ["chicago", "new york city", "washington"]
    while city not in cities:
        city = input("Please choose either Chicago, New York City, or Washington: ").lower()

    # get user input for month (all, january, february, ... , june)
    month = ''
    months = ["january", "february", "march", "april", "may", "june", "all"]
    while month not in months:
        month = input("Please choose a month by entering either January, February, March, April, May, June, or All: ").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    days = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "all"]
    while day not in days:
        day = input("Please choose a day of the week by entering either Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or All: ").lower()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_popular_month = df['month'].mode()[0]
    print("\nMost popular month: ",most_popular_month)

    # display the most common day of week
    most_popular_day = df['day_of_week'].mode()[0]
    print("\nMost popular day: ",most_popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_popular_hour = df['hour'].mode()[0]
    print("\nMost common start hour: ",most_popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("\nMost popular start station: ",popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("\nMost popular end station: ",popular_end_station)

    # display most frequent combination of start station and end station trip
    df['Start & End'] = df['Start Station'].str.cat(df['End Station'], sep=' - ')
    popular_combo_stations = df['Start & End'].mode()[0]
    print("\nMost popular combination of stations: ",popular_combo_stations)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    ttl_travel_time = df['Trip Duration'].sum()
    print("\nTotal travel time: ",ttl_travel_time)

    # display mean travel time
    avg_travel_time = df['Trip Duration'].mean()
    print("\nAverage travel time: ",avg_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user_type = df['User Type'].value_counts()
    print(count_user_type)

    #only show the gender & birth data for chicago & NYC -- washington does not have the data.
    # Display counts of gender
    try:
        count_gender = df['Gender'].value_counts()
        print(count_gender)
    except:
        print("\nThere is no gender data to display.")

    try:
        # Display earliest, most recent, and most common year of birth
        earliest_byear = df['Birth Year'].min()
        print("\nEarliest birth year: ",earliest_byear)

        recent_byear = df['Birth Year'].max()
        print("\nMost recent birth year: ",recent_byear)

        common_byear = df['Birth Year'].mode()[0]
        print("\nMost common birth year: ",common_byear)
    except:
        print("\nThere is no birth year data to display.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
#take user input if they would like to see 5 lines of raw data
#keep presenting 5 more lines until they say no
user_choice = ''
row = 0
user_choice = input("Would you like to see 5 lines of raw data? Please enter either yes or no: ").lower()
while user_choice == 'yes':
    print(df[row:row+5])
    user_choice = input("Would you like to see 5 more lines of raw data? Please enter either yes or no: ").lower()
    row += 5


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
