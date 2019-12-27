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
    print('Hello! Let\'s explore some US bikeshare data!\n{}'.format('*'*50))
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities='chicago','new york city','washington','all'
    months='january','february','march','april','may','june','all'
    days='monday','tuesday','wednesday','thursday','fridays','saturday','sunday','all'
    
    while True:
        try:
            print('\nAvailable Cities are: {}\nChoose a city to explore or ALL to explore all the cities combined:'.format(cities))
            city=(input()).lower()
            if city in cities:
                print('\nOK {} it is!!!!\n'.format(city))
                break
            else:
                print('\n{} is not an available City.\nSelect from available cities listed above'.format(city))
                continue
        except Exception as e:
            print('\nException occured: {}\n'.format(e))
            
    while True:
        # get user input for month (all, january, february, ... , june)
        try:
            print('\nGreat!!! Now select a specific month to analyse or ALL to analyse all the months combined.\nAvailable months are {}'.format(months))
            month=(input()).lower()
            if month in months:
                print('\nOK {} it is!!!!\n'.format(month))
                break
            else:
                print('\n{} is not an available month.\nSelect from available months listed above'.format(city))
                continue
        except Exception as e:
            print('\nException occured: {}\nEnter correct value'.format(e))
            continue
    while True:
        # get user input for day of week (all, monday, tuesday, ... sunday)
        try:
            print('Finally!!! Enter day of week to analyse or select ALL to analyse all the days of the week combined.\nDays of week are {}'.format(days))
            day=(input()).lower()
            if day in days:
                print('\nOK {} it is!!!!\n'.format(day))
                break
            else:
                print('\n{} is not an available day of week.\nSelect from available days of week listed above'.format(city))
                continue
        except Exception as e:
            print('Exception occured: {}\nEnter correct value'.format(e))   

    print('-'*40)
    return city,month,day


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
    if city=='all':
        data1=pd.read_csv('chicago.csv')
        data2=pd.read_csv('new_york_city.csv')
        data3=pd.read_csv('washington.csv')
        
        bd=data1.append(data2, ignore_index=True)
        df=bd.append(data3,ignore_index=True)
    else:
        #load data file into dataframe
        df=pd.read_csv(CITY_DATA[city])
    df=df.fillna(0)
    #convert start time column into datetime
    df['Start Time']=pd.to_datetime(df['Start Time'])
    
    #extract month and day of week from start time to create new column
    df['month']=df['Start Time'].dt.month
    df['day_of_week']=df['Start Time'].dt.weekday_name
    
    if month != 'all':
        months=['january', 'february', 'march', 'april', 'may', 'june']
        imonth=months.index(month)+1
        
        df=df[df['month']==imonth]
              
    if day != 'all':
        df=df[df['day_of_week']==day.title()]
       
    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    count=dict()
    month=df['month']
    for i in month:
        count[i]=count.get(i,0)+1
    maxm=max(count)
    months=['january', 'february', 'march', 'april', 'may', 'june']
    print('\nMost common month is: {}\n'.format(months[maxm-1]))
    
    # display the most common day of week
    week=df['day_of_week']
    maxw=week.mode().values
    print('\nMost common week is: {}\n'.format(maxw))
        
    # display the most common start hour
    df['hour']=df['Start Time'].dt.hour
    hr=df['hour']
    maxh=hr.mode().values
    print('\nMost common start hour: {}\n'.format(maxh))    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    ss=df['Start Station']
    maxss=ss.mode().values
    print('\nThe commonly used start station is: {}\n'.format(maxss))
        
    # display most commonly used end station
    es=df['End Station']
    maxes=es.mode().values
    print('\nThe commonly used end station is: {}\n'.format(maxes))
        
    # display most frequent combination of start station and end station trip
    df['Start stop and end station']=df['Start Station']+' to '+df['End Station']
    sses=df['Start stop and end station']
    maxsses=sses.mode().values
    print('\nStart stop and end station: {}\n'.format(maxsses))
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel=sum(df['Trip Duration'])
    print('\nTotal travel time is: {}\n'.format(total_travel))

    #display mean travel time
    print('\nMean travel time is: {}\n'.format(np.mean(df['Trip Duration'])))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    ut=df['User Type']
    ut=ut[ut!=0]
    countut=dict()
    for i in ut:
        countut[i]=countut.get(i,0)+1
    print('\nDisplaying count of user types: {}\n'.format(countut))
    
    # Display counts of gender
    try:
        g=df['Gender']
        g=g[g!=0]
        countg=dict()
        for i in g:
            countg[i]=countg.get(i,0)+1
        print('\nDisplaying count of gender: {}\n'.format(countg))
    except Exception as e:
        print('{} information is not avaliable for {}\n'.format(e,city))

    # Display earliest, most recent, and most common year of birth
    try:
        year=df['Birth Year']
        #taking out all zero values
        year=year[year!=0]

        earliest=year.min()
        print('Earliest year of birth is {}\n'.format(earliest))

        recent=year.max()
        print('Most recent year of birth is {}\n'.format(recent))
        
        common=year.mode().values
        print('Most common year of birth is {}\n'.format(common))
    except Exception as e:
        print('{} information is not available for {}'.format(e,city))
    
    
    n=5
    while True:
        print('\nDo you want to see Raw data? \n Enter Yes or No?')
        response=(input('')).lower()
        if response == 'yes':
            print('Okay!! coming right up!!')
            print(df.head(n))
            while True:
                n+=5
                print('wanna see more? Yes or No ?')
                response2=(input()).lower()
                if response2 == 'yes':
                    print(df.head(n))
                    continue
                elif response2 == 'no':
                    break
                else:            
                    print('{} is invalid response. Choose Yes or No\n'.format(response2))
                    continue
            break
        if response == 'no':
            break
        else:
            print('{} is invalid response. Choose Yes or No\n'.format(response))
            continue
            
            
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('Good Bye')
            break

if __name__ == "__main__":
	main()
