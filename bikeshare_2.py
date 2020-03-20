import time
import pandas as pd
import numpy as np
import datetime

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        (str) choice - what kind of filter to apply
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington).
    while True:
        city = input('Would you like to see data from Chicago, New York City, or Washington?\n')
        if city in ('Chicago', 'New York City', 'Washington'):
            print('You would like to look at the data from {}!\n'.format(city))
            break
        else:
            print('\nPlease enter a valid city!')
            continue
    # get user input for month (all, january, february, ... , june)
    # get user input for day of week (all, monday, tuesday, ... sunday)
    # get user input for filter both day and week
    day = 'all'
    month = 'all'
    while True:
        choice = input('Would you like to filter the data by month, day or both?\nEnter month, day or both.\n')
        if choice == 'month':
            month = input('Enter the month you would like to check:\nall, january, february, march, april, may, june\n')
            if month in ('all', 'january', 'february', 'march', 'april', 'may', 'june'):
                print('You would like to look at the data from {}!\n'.format(month))
                break
            else:
                print('\nPlease enter a valid month!')
                continue
        elif choice == 'day':
            day = input('Enter the day you would like to check:\nall, monday, tuesday, wednesday, thursday, friday, saturday, sunday\n')
            if day in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
                print('You would like to look at the data from {}!\n'.format(day))
                break
            else:
                print('\nPlease enter a valid day!')
                continue
        elif choice == 'both':
            month = input('Enter the month you would like to check:\nall, january, february, march, april, may, june\n')
            if month not in ('all', 'january', 'february', 'march', 'april', 'may', 'june'):
                print('\nPlease enter a valid month!')
                continue
            day = input('Enter the day you would like to check:\nall, monday, tuesday, wednesday, thursday, friday, saturday, sunday.\ny7t67')
            if day not in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
                print('\nPlease enter a valid month!')
                continue
        else:
            print('Please provide valid input')
        break

    print('-'*40)
    return city, month, day, choice

def load_data(city, month, day, choice):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        (str) choice - what kind of filter to apply
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday
    # filter by month if applicable
    if choice == 'month':
        if month != 'all':
            # use the index of the months list to get the corresponding int
            months = ['january', 'february', 'march', 'april', 'may', 'june']
            month = months.index(month) + 1

            # filter by month to create the new dataframe
            df = df[df['month'] == month]
    elif choice == 'day':
        # filter by day of week if applicable
        if day != 'all':
            days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
            # filter by day of week to create the new dataframe
            df = days.index(day)
            df = df[df['day_of_week'] == day]
    else:
        if month != 'all':
            months = ['january', 'february', 'march', 'april', 'may', 'june']
            month = months.index(month) + 1
            df = df[df['month'] == month]
        if day != 'all':
            days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
            day = days.index(day)
            df = df[df['day_of_week'] == day]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    Returns:
        The most common month, day of week and start hour for filtered df.
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].value_counts().idxmax()
    month_counts = df['month'].value_counts()
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    popular_month = months[popular_month - 1]
    print('Most Frequent month of travel: {}, count: {}\n'.format(popular_month.title(), month_counts))

    # display the most common day of week
    popular_dow = df['day_of_week'].value_counts().idxmax()
    dow_counts = df['day_of_week'].value_counts()
    days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    popular_dow = days[popular_dow]
    print('Most Frequent day of travel: {}, count: {}\n'.format(popular_dow.title(), dow_counts))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].value_counts().idxmax()
    hour_counts = df['hour'].value_counts()
    print('Most Frequent hour of travel: {}, count: {}\n'.format(popular_hour, hour_counts))

    # drop extra columns to decrease df size
    df.drop('month', axis=1, inplace=True)
    df.drop('day_of_week', axis=1, inplace=True)
    df.drop('hour', axis=1, inplace=True)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.
    Returns:
        The most common start, end and combination of stations for filtered df.
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].value_counts().idxmax()
    popular_start_counts = df['Start Station'].value_counts()
    print('Most commonly used start station: {}, count: {}\n'.format(popular_start_station, popular_start_counts))

    # display most commonly used end station
    popular_end_station = df['End Station'].value_counts().idxmax()
    popular_end_counts = df['End Station'].value_counts()
    print('Most commonly used end station: {}, count: {}\n'.format(popular_end_station, popular_end_counts))

    # display most frequent combination of start station and end station trip
    df['combination'] = df['Start Station'] + '-' + df['End Station']
    popular_combination = df['combination'].value_counts().idxmax().split('-')
    print('Most frequent combination of stations is from {} to {}\n'.format(*popular_combination))

    # drop extra columns to decrease df size
    df.drop('combination', axis=1, inplace=True)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def convert(sec):
    """ Convert seconds to HH:MM:SS format"""
    return str(datetime.timedelta(seconds = sec))

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.

   Returns:
       The total travel time and average travel time for filtered df.
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    total_travel = convert(int(total_travel))
    print('Total travel duration is: {}\n'.format(total_travel))

    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    mean_travel = convert(int(mean_travel))
    print('Mean travel duration is: {}\n'.format(mean_travel))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users.
    Attention: Chicago and New York City data contain gender and birth year infomation.
               Washington data does not contain gender and birth year information.
    Returns:
        Break down data of gender, birth year for filtered df if possible.
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_count = df['User Type'].value_counts()
    print('What\'s the break down of users types:\n{}'.format(user_count))

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print('What\'s the break down of gender:\n{}'.format(gender_count))
    else:
        print('There is no gender infomation for this filter.')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_bday = int(df['Birth Year'].min())
        recent_bday = int(df['Birth Year'].max())
        common_bday = int(df['Birth Year'].value_counts().idxmax())
        print('The ealiest year of birth is: {}\n The most recent year of birth is: {}\n The most common year of birth is: {}\n'.format(earliest_bday, recent_bday, common_bday))
    else:
        print('There is no statistics of birth year for this filter!')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Display 5 individual data in a row.
    Can be terminated by replying y/n while pop out option is displayed.
    """

    i_start = 0
    i_end = 5

    while True:
        answer = input('Do you want to view individual data? y/n\n')
        if answer == 'n':
            print('Come back whenever you need!\n')
            break
        elif answer == 'y':
            # Transform dataframe to dictionary
            print(df.iloc[i_start:i_end, 1:].to_dict('index'))
            while True:
                answer = input('Do you want to view more individual data? y/n\n')
                if answer == 'y':
                    i_start += 5
                    i_end += 5
                    display_dict = df.iloc[i_start:i_end, 1:].to_dict('index')
                    return display_dict
                elif answer == 'n':
                    break
                else:
                    print('Please enter y/n!\n')
                    continue
        else:
            print('Please enter y/n!\n')
            continue



def main():
    while True:
        city, month, day, choice = get_filters()
        df = load_data(city, month, day, choice)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
