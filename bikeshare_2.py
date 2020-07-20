import time
import pandas as pd
import numpy as np

cities = ['chicago', 'new york', 'washington', 'all']
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all' ]

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Which city would you like to learn about? We have data for New York, Washington, and Chicago.\n>').lower()
        if city not in cities:
            print('We do not have that data. Try looking for data for New York, Washington, or Chicago.')
            continue
        else:
            break
    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input('Which month would you like to focus on? We have data between January and June.\n>').lower()
        if month not in months:
            print('We do not have that data. Try looking for any month from January to June.')
            continue
        else:
            break
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Finally, which specific day are you most interested in?\n>').lower()
        if day not in days:
            print('I am not sure I undestand that. Try typing out the full title of the day.')
            continue
        else:
            break
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

    print(df.head())
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

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

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print('The most common month within your specified query is', popular_month)

    # TO DO: display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]
    print('The most common day of the week within your specified query is',popular_day_of_week)

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('The most common hour within your specified query is',popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start_station = df['Start Station'].value_counts().index[0]
    print('The most commonly used start station within your specified query is', most_common_start_station)
    # TO DO: display most commonly used end station
    most_common_end_station = df['End Station'].value_counts().index[0]
    print('The most commonly used end station within your specified query is\n', most_common_start_station)
    # TO DO: display most frequent combination of start station and end station trip
    most_common_both = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False).nlargest(n=1)
    print('The most commonly used start and end station combination is\n', most_common_both)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_time = df['Trip Duration'].sum()
    print('Total travel time is', int(total_time / 60 / 60 / 24), 'days and', int(total_time / 60 / 60 % 24), 'hours.')
    # TO DO: display mean travel time
    mean_time = df['Trip Duration'].mean()
    print('Mean travel time is', int(total_time / 60 / 60 / 24), 'days and', int(total_time / 60 / 60 % 24), 'hours.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Counts by user types for your query are\n',user_types)

    # TO DO: Display counts of gender

    if 'Gender' in df.columns:
        user_gender = df['Gender'].value_counts()
        print('Counts by user types for your query are\n',user_gender)
    else:
        print('Gender information is not available for the selected city.')

    # TO DO: Display earliest, most recent, and most common year of birth

    if 'Birth Year' in df.columns:
        earliest_birth = df['Birth Year'].min()
        recent_birth = df['Birth Year'].max()
        common_birth = df['Birth Year'].mode()[0]
        print('The oldest member(s) were born in',int(earliest_birth),', the youngest rider(s) were born in',int(recent_birth),', and the most common birth year for our members is',int(common_birth))
    else:
        print('Birth year information is not available for the selected city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
