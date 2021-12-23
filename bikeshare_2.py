import time
import pandas as pd
# import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
cities = list(CITY_DATA.keys())
months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

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
    while True:
        try:
            city_choice = int(input(
            "Which city's data would you like to see?\n\
            (Select your choice with the corresponding numbers)\n\
            [1] {}\n[2] {}\n[3] {}\n"
            .format(cities[0].title(), cities[1].title(), cities[2].title()).replace('    ', '')
            ))
        except ValueError:
            print("\nERROR!\nYour input was not accepted.\nTry again!")
        
        finally:
            try:
                if 0 < city_choice < 4:
                    city = cities[city_choice - 1].lower()
                    print("\nYou have selected {}.".format(city.title()))
                    break
                else:
                    print("ERROR! INVALID SELECTION!\nEnsure your choice is 1 or 2 or 3 ONLY!.")
                
                del(city_choice)
            except NameError:
                print("Ensure your choice is 1 or 2 or 3 ONLY!.\n")

    # get user input for time filter type (month, day, both or none)
    while True:
        try:
            time_choice = int(input(
            "\nBy what time basis would you like to filter the data?\n\
            (Select your choice with the corresponding numbers)\n\
            [0] {3}\n[1] {0}\n[2] {1}\n[3] {2}\n"
            .format('Monthly', 'Daily', 'Monthly and Daily', 'None').replace('    ', '')
            ))
        except ValueError:
            print("ERROR!\nYour input was not accepted.\nTry again!")
        
        finally:
            try:
                if 0 <= time_choice < 4:
                    if time_choice == 0:
                        month, day = 'all', 'all'
                    elif time_choice == 1:
                        month, day = get_month(), 'all'
                    elif time_choice == 2:
                        month, day = 'all', get_day()
                    elif time_choice == 3:
                        month, day = get_month(), get_day()

                    break
                else:
                    print("ERROR! INVALID SELECTION!\nEnsure your choice is 1 or 2 or 3 ONLY!.")
                
                del(time_choice)
            except NameError:
                print("Ensure your choice is 1 or 2 or 3 ONLY!.")

    print('-'*40)
    return city, month, day


def get_month():
    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month_choice = int(input(
            "\nWhich month's data would you like to see?\n\
            (Select your choice with the corresponding numbers)\n\
            [1] January\n[2] February\n[3] March\n[4] April\n[5] May\n[6] June\n[7] All\n"
            .replace('    ', '')
            ))
        except ValueError:
            print("ERROR!\nYour input was not accepted.\nTry again!")
        
        finally:
            try:
                if 0 < month_choice <= 7:
                    if month_choice != 7:
                        month = months[month_choice - 1]
                    else:
                        month = 'all'
                    
                    print("\nYou chose {}".format(month).title())
                    break

                else:
                    print("ERROR! INVALID SELECTION!\nEnsure your choice is between 1 to 7 ONLY!.")
                    del(month_choice)

            except NameError:
                print("Ensure your choice is 1 or 2 or 3 ONLY!.")

    return month


def get_day():
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day_choice = int(input(
            "\nWhich day's data would you like to see?\n\
            (Select your choice with the corresponding numbers)\n\
            [1] Sunday\n[2] Monday\n[3] Tuesday\n[4] Wednesday\n[5] Thursday\n[6] Friday\n[7] Saturday\n[8] All\n"
            .replace('    ', '')
            ))

        except ValueError:
            print("ERROR!\nYour input was not accepted.\nTry again!")
        
        finally:
            try:
                if 0 < day_choice <= 7:
                    if day_choice != 7:
                        day = days[day_choice - 1]
                    else:
                        day = 'all'

                    print('\nYou chose {}'.format(day.title()))
                    break
                
                else:
                    print("ERROR! INVALID SELECTION!\nEnsure your choice is between 1 to 7 ONLY!.")
                    del(day)

            except NameError:
                print("Ensure your choice is 1 or 2 or 3 ONLY!.")

    return day


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
    if city != 'washington':
        df = pd.read_csv(CITY_DATA[city], usecols=[1, 2, 3, 4, 5, 6, 7, 8])
    else:
        df = pd.read_csv(CITY_DATA[city], usecols=[1, 2, 3, 4, 5, 6])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Start Month'] = df['Start Time'].dt.month_name()
    df['Start Day'] = df['Start Time'].dt.day_name()
    df['Start Hour'] = df['Start Time'].dt.hour

    if month != 'all':
        df = df[df['Start Month'] == month.title()]
        print('NOTE: Only data for the month of {} will be analysed.'.format(month.title()))
    else:
        print('Data for ALL months from January to June will be analysed.')
    
    if day != 'all':
        df = df[df['Start Day'] == day.title()]
        print('NOTE: Only data for {} will be analysed.'.format(day.title()))
    else:
        print('Data for ALL days from Sunday to Saturday will be analysed.')

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['Start Month'].mode()[0]
    popular_month_count = df['Start Month'].value_counts()[popular_month]
    print("The service is mostly used around: {} ({} counts).".format(popular_month, popular_month_count))
   
    # display the most common day of week
    popular_day = df['Start Day'].mode()[0]
    popular_day_count = df['Start Day'].value_counts()[popular_day]
    print("People ride mostly on: {}s ({} counts)".format(popular_day, popular_day_count))

    # display the most common start hour
    popular_hour = df['Start Hour'].mode()[0]
    popular_hour_count = df['Start Hour'].value_counts()[popular_hour]
    add_sentence = ''
    if popular_hour > 12:
        if 12 <= popular_hour <= 17:
            add_sentence = 'during the day'
        elif 17 < popular_hour <= 20:
            add_sentence = 'in the evening'
        else:
            add_sentence = 'at night'

        popular_hour = str(popular_hour % 12) + ' p.m'

    elif popular_hour == 0:
        popular_hour = '12 a.m'
    else:
        popular_hour = "{} a.m".format(popular_hour)
    if 'a.m' in add_sentence:
        add_sentence = 'in the morning'
    print("People ride more commonly around {} {}. ({} counts).".format(popular_hour, add_sentence, popular_hour_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    popular_start_station_count = df['Start Station'].value_counts()[popular_start_station]
    print('Most trips start from {} ({} counts).'.format(popular_start_station, popular_start_station_count))

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    popular_end_station_count = df['End Station'].value_counts()[popular_end_station]
    print('Most riders stop at {} ({} counts).\n'.format(popular_end_station, popular_end_station_count))

    # display most frequent combination of start station and end station trip
    routes_count = df.groupby(['Start Station', 'End Station'])['End Station'].count()
    popular_route = routes_count[routes_count == routes_count.max()]
    print('The most popular start and end station combination is the trip: \
        \nFROM: {}\nTO: {} \n\nThese stations have shared {} bike rides between them.'
        .format(popular_route.index[0][0], popular_route.index[0][1], routes_count.max()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('In total, all trips have taken: {}.'.format(format_time(total_travel_time)))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The average riding time is {}'.format(format_time(mean_travel_time)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def format_time(time_sec):
    """
    Returns the number of years, days, hours, minutes and seconds contained within time_sec.
    Args:
    (int) time_sec: the number of seconds to be split into other time units.
    """
    HOUR_SEC = 60 * 60
    DAY_SEC = 24 * HOUR_SEC
    YEAR_SEC = 365.25 * DAY_SEC

    time_str = ''
    remainder = time_sec
    if (time_sec >  YEAR_SEC) or (time_sec > DAY_SEC) or (time_sec > HOUR_SEC) or (time_sec >= 60):
        if remainder >= YEAR_SEC:
            time_str += '{} years, '.format(int(remainder // YEAR_SEC))
            remainder %= YEAR_SEC
        
        if remainder >= DAY_SEC:
            time_str += '{} days, '.format(int(remainder // DAY_SEC))
            remainder %= DAY_SEC
        
        if remainder >= HOUR_SEC:
            time_str += '{} hours, '.format(int(remainder // HOUR_SEC))
            remainder %= HOUR_SEC
        
        if remainder >= 60:
            time_str += '{} minutes, '.format(int(remainder // 60))
            remainder %= 60

        if remainder < 60:
            time_str += 'and {} seconds'.format(round(remainder, 2))
    
    else:
        time_str = '{} seconds'.format(round(remainder, 2))

    return time_str


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('\n', df['User Type'].value_counts())

    # Display counts of gender
    if 'Gender' in df:
        print('\n', df['Gender'].value_counts())
    else:
        print('\nGender data not available.\n')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_birth_year = df['Birth Year'].min()
        recent_birth_year = df['Birth Year'].max()
        popular_birth_year = df['Birth Year'].mode()[0]
        popular_birth_year_users_count = df['Birth Year'].value_counts()[popular_birth_year]

        print('\nOldest User: {0}\nYoungest User: {1}\nMost users ({3} users) were born in {2}.'
        .format(earliest_birth_year, recent_birth_year, popular_birth_year, popular_birth_year_users_count))
    else:
        print('Birth year data not available')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def show_raw_data(df):
    """
    Asks the user if they want to view the data as is in the DataFrame
    Displays the data frame in a tabular data if the user selects 'yes'
    """
    index_tracker = 0

    while True:
            see_individual_trips = input('\nWould you like to view individual trip data?\n \
                [Y]es \t [N]o\n')
            if see_individual_trips.lower() in ('yes', 'y'):
                individual_trips = df.iloc[index_tracker : index_tracker + 5, 2 : ]
                print(individual_trips)
                index_tracker += 5
            else:
                break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        show_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
