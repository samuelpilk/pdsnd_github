import time
import pandas as pd
import numpy as np

CITY_DATA = { 'ch': 'chicago.csv',
              'ny': 'new_york_city.csv',
              'wa': 'washington.csv' }

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
        city = str(input("Input a city, CH for Chicago, NY for New York City or WA for Washington: \n")).lower()
        if city.lower() not in ('ch', 'ny', 'wa'):
            print("Please check your input.")
        else:
            break


    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = str(input("Input a month, or 'all', eg. all, january, february, march, april, may or june: \n")).lower()
        if month.lower() not in ('all', 'january', 'february', 'march', 'april', 'may', 'june'):
            print("Please check your input.")
        else:
            break


    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = str(input("Input a day, or 'all', eg. all, monday, tuesday, wednesday, thursday, friday, saturday or sunday: \n")).lower()
        if day.lower() not in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
            print("Please check your input.")
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
        df = df.loc[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    #Ask the user if they want to see raw data, and if so how many lines
    show_raw_data = input('\nWould you like to see the raw data? Enter yes or no.\n')

    if show_raw_data.lower() == 'yes':
        while True:
            num_data = input('How many lines would you like to see? Enter a number 1-10.\n')
            try:
                num_data = int(num_data)
                if num_data <= 10 and num_data >= 1:
                    print('Displaying raw data....')
                    pd.options.display.max_columns = None
                    print('\n',df.head(num_data))
                    break
                else:
                    print('Please check your input is whole number between 1-10!')

            except:
                print('Please check your input is whole number between 1-10!')

    print('\n')
    print('-'*40)

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['January', 'February', 'March', 'April', 'May', 'June']

    common_month = months[df['month'].value_counts().idxmax()-1]
    print("The most common month is: ", common_month)

    # display the most common day of week
    common_day = df['day_of_week'].value_counts().idxmax()
    print("The most common day of the week is: ", common_day)


    # display the most common start hour
    df['Start Time 2'] = df['Start Time'].dt.floor('h')
    df['hour'] = df['Start Time 2'].dt.time
    common_hour = df['hour'].value_counts().idxmax()
    print("The most common start hour is: ", common_hour)

    #Removing created columns above to keep df clean
    df.drop(['Start Time 2', 'hour'], axis=1, inplace=True)
    #Make sure they are gone...
    #print(df.head(1))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].value_counts().idxmax()
    print("The most common Start Station is: ", common_start_station)
    #Used the below to check that the correct station is displayed
    #print(df.groupby('Start Station').count().sort_values(['Start Time'], ascending=False).head(5))


    # display most commonly used end station
    common_end_station = df['End Station'].value_counts().idxmax()
    print("The most common End Station is: ", common_end_station)
    #Used the below to check that the correct station is displayed
    #print(df.groupby('End Station').count().sort_values(['Start Time'], ascending=False).head(5))


    # display most frequent combination of start station and end station trip
    station_combination = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print("The most frequent Start and End Station combination are: {} and {}".format(station_combination[0],station_combination[1]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #Used to check the data type
    #print(df.dtypes)

    #Converting End Time column from an object to datetime64[ns] data type
    df['End Time'] = pd.to_datetime(df['End Time'], format= '%Y/%m/%d')

    #Some of the data had End times that where before Start Times. It was decided to clean up the data by removing these rows with the code below.
    #Placed code here as not to impact on results of other functions that have valid data.
    df['Check Time'] = np.where(df['End Time'] > df['Start Time'], True, False)
    df.drop(df[df['Check Time'] == False].index, inplace=True)

    #Used to check that only the rows we wanted remained in the dataframe
    #check_time = df["Check Time"].value_counts().to_string()
    #print("Test column results:\n", check_time)

    #Remove the new column created above
    df.drop(['Check Time'], axis=1, inplace=True)


    #Creating a new cloumn to display the time difference between Start Time and End Time
    df['Time Diff'] = df['End Time'].subtract(df['Start Time'])

    # display total travel time
    total_travel_time = df['Time Diff'].sum()
    print("The total travel time is: ", total_travel_time)


    # display mean travel time
    mean_travel_time = df['Time Diff'].mean()
    print("The mean travel time is: ", mean_travel_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df["User Type"].value_counts().to_string()
    print("User Type counts are:\n", user_types)


    # Display counts of gender
    if 'Gender' in df:
        gender_counts = df["Gender"].value_counts().to_string()
        print("\nGender counts are: \n", gender_counts)
    else:
        print("\nThere is no gender information to display!")


    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print("\n")

        earliest_year = df.loc[df['Birth Year'].idxmax()]
        earliest_year = earliest_year['Birth Year']
        print("The earliest year of birth is: ", int(earliest_year))

        most_recent_year = df.loc[df['Birth Year'].idxmin()]
        most_recent_year = most_recent_year['Birth Year']
        print("Most recent year of birth is: ", int(most_recent_year))

        common_year = df['Birth Year'].value_counts().idxmax()
        print("Most common year of birth is: ", int(common_year))

    else:
        print("\nThere is no Birth Year information to display!")



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
