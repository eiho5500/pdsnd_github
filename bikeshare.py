import time
import pandas as pd
import numpy as np
import calendar as cl
import datetime as dt

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

    print('Hello! Let\'s explore some US bikeshare data!\n')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = '0'
    month = ' '
    day = ' '
    city_select = ['c', 'n', 'w']
    month_select = ['all', '1', '2', '3', '4', '5', '6']
    day_select = ['all', '1', '2', '3', '4', '5', '6', '7']

    while city not in city_select:
        city = input('Please first select the city you want to investigate by entering the respective letter!\n C - Chicago\n N - New York City\n W - Washington\n\nEnter value: ').lower()
        if city not in city_select:
            print('This was no valid input, please try again!\n')
    for key in CITY_DATA.keys():
        if key[0] == city:
            city = key
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    while month not in month_select:
        try:
            month = input('\nPlease select a month between January and June you want to investigate by entering the respective number.\nTo select all at once, just press enter.\nEnter value:')
        except ValueError:
            print('This was no valid input, please try again!\n')
        finally:
            if not month:
                month = 'all'
            if month not in month_select:
                print('This was no valid input, please try again!\n')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while day not in day_select:
        try:
            day = input('Please select a weekday you want to investigate by entering the respective number (Monday = 1 to Sunday =7).\nTo select all at once, just press enter.\nEnter value:')
        except ValueError:
            print('This was no valid input, please try again!\n')
        finally:
            if not day:
                day = 'all'
            if day not in day_select:
                print('This was no valid input, please try again!\n')

    if month != 'all':
        month = cl.month_name[int(month)]
    if day != 'all':
        day = cl.day_name[int(day)-1]

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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1

        # filter by month to create the new dataframe
        df = df[df['Month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['Day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    But only displays statistics which make sense.
    Eg.g if just one weekday was selected to be displayed,
    the calculation of the most commmon day of the week for rentals will not be performed"""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    if df['Month'].nunique() > 1:
        most_common_month = int(df['Month'].mode()[0])
        print('Most trips have been booked in {}.'.format(cl.month_name[most_common_month]))

    # TO DO: display the most common day of week
    if df['Day_of_week'].nunique() > 1:
        most_common_day = df['Day_of_week'].mode()[0]
        print('Most trips have been booked on {}s.'.format(most_common_day))

    # TO DO: display the most common start hour
    most_common_hour = df['Start Time'].dt.hour.mode()[0]
    print('Most trips started between {}:00 and {}:00.'.format(most_common_hour, most_common_hour+1))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start = df['Start Station'].mode()[0]
    print('Most trips started at {}.'.format(most_common_start))

    # TO DO: display most commonly used end station
    most_common_end = df['End Station'].mode()[0]
    print('Most trips ended at {}.'.format(most_common_end))

    # TO DO: display most frequent combination of start station and end station trip
    df['Route'] = df['Start Station'] + ' to ' + df['End Station']
    most_common_route = df['Route'].mode()[0]
    print('Most common route is from {}.'.format(most_common_route))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time = str(dt.timedelta(seconds=int(total_travel_time)))
    print('The total time bikes were used sums up to {} of travel.'.format(total_travel_time))
    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time = str(dt.timedelta(seconds=int(mean_travel_time)))
    print('The average rental duration per trip was {}.'.format(mean_travel_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users.
    Only those statistics are evaluated where data is available.
    E.g. gender assessment is not possible for all data sets."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts().to_dict()
    for user_type in user_types:
        print('Users of the type {} rented bikes {} times.'.format(user_type, user_types[user_type]))

    # TO DO: Display counts of gender
    try:
        gender_split = df['Gender'].value_counts().to_dict()
        for gender in gender_split:
            print('{} users rented bikes {} times.'.format(gender, gender_split[gender]))
    # TO DO: Display earliest, most recent, and most common year of birth
        earliest_birth_year = int(df['Birth Year'].min())
        recent_birth_year = int(df['Birth Year'].max())
        common_birth_year = int(df['Birth Year'].mode()[0])
        print('Oldest users are born in {}.\nYoungest users are born in {}.\nMost users are born in {}.'.format(earliest_birth_year, recent_birth_year, common_birth_year))

    finally:
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

def task_loop(city, month, day):
    """Serves to confirm that user selection of data was correct.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter

    Returns:
        n as True/Fales to define if data selection will be repeated or not"""
    if month == 'all':
        month = 'all available months'
    if day == 'all':
        day = 'all day'
    n = input('You will be investigating on {} usage data for {}s in {}.\nIf this is correct, please press enter to continue or enter any value to repeat your data selection.' .format(city.title(), day, month))
    if n:
        n = True
    else:
        n = False
    return n

def analysis_selection(df):
    """Serves that the user can select which type of analysis he wants to conduct."""
    
    while True:
        try:
            analysis = int(input('Please select the analysis you want to run by entering the analysis number:\n1 - Rental Times\n2 - Stations and Routes\n3 - Rental duration\n4 - Users\n5 - quit analysis selection\nEnter value:'))
        except:
            print('No valid data entry, please try again!\n')
        else:
            if analysis == 1:
                time_stats(df)
            elif analysis == 2:
                station_stats(df)
            elif analysis == 3:
                trip_duration_stats(df)
            elif analysis == 4:
                user_stats(df)
            elif analysis == 5:
                break
            else:
                print('No valid data entry, please try again!\n')
                time.sleep(3)

def main():
    n = True
    while True:
        while n:
            city, month, day = get_filters()
            df = load_data(city, month, day)
            n = task_loop(city, month, day)
        analysis_selection(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() == 'yes':
            n = True
        else:
            break


if __name__ == "__main__":
	main()
