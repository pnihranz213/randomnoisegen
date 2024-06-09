import pandas as pd
import random

#Create a dictionary with people containing keys of their names
#The dictionary should contain at least ten people.

people = {
    "Name": ['Patrick', 'Tara', 'John', 'Jane', 'Mary', 'Peter', 'Paul', 'James', 'Lucy', 'Grace']
}

#The next dictionary contains 4 keys, vegtable, vegtable % (which incdicates the percentage rate that this particular vegtable is written in the data we are generating)
#servings, and serving %
vegtables = {
    "vegtable": ['Carrot', 'Broccoli', 'Peas', 'Corn'],
    "vegtable %": [0.1, 0.4, 0.4, 0.1],
    "servings": [1, 2, 3, 4],
    "servings %": [0.25, 0.25, 0.25, 0.25]
}

#timer decorator
def timer(func):
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Function {func.__name__} took {end - start} seconds to complete")
        return result
    return wrapper

#function turns dictionary into a dataframe
def create_dataframe(data):
    return pd.DataFrame(data)

#function finds all the keys in vegtables that do not have the % character in them
def find_keys_without_percent(data):
    return [key for key in data if "%" not in key]

#function adds new columns to dataframe based on a list
def add_columns(dataframe, columns):
    for column in columns:
        dataframe[column] = None
    return dataframe

#for the percentage columns, the function should make the data cumulative
@timer
def make_cumulative(data):
    for key in data:
        if "%" in key:
            cumsum = 0
            cumsum_values = []
            for value in data[key]:
                cumsum += int(value*100)
                cumsum_values.append(cumsum)
            data[key] = cumsum_values
    return data

#gives a number from 1 to 100
def generate_random_percent():
    return random.randint(1, 100)

def random_item(data):
    new_values = []
    for key in data:
        if "%" in key:
            for index, value in enumerate(data[key]):
                num = generate_random_percent()
                if index == 0:
                    if num >= 0 and num <= value:
                        new_values.append(data[key.replace(' %','')][index])
                        break
                if num >0 and data[key][index-1] and num <= value:
                    new_values.append(data[key.replace(' %','')][index])
                    break
                else:
                    continue
    return new_values     

#using the function random_item, create a dataframe the length of the people dictionary that contains the random item from the vegtables dictionary and has headers equal to the keys in the vegtables dictionary that do not have the % character in them
def create_random_dataframe(people, vegtables):
    random_data = []
    for i in range(len(people['Name'])):
        random_data.append(random_item(vegtables))
    return pd.DataFrame(random_data, columns=find_keys_without_percent(vegtables))

#merge the two dataframes with people appearing on the left
def merge_dataframes(left, right):
    return pd.concat([left, right], axis=1)

def main():
    #convert both dictionaries to csv files
    people_df = create_dataframe(people)
    vegtables_df = create_dataframe(vegtables)
    people_df.to_csv('people.csv')
    vegtables_df.to_csv('vegtables.csv')
    print(people_df)
    vegtables_cum = make_cumulative(vegtables)
    print(random_item(vegtables_cum))
    generated_data = create_random_dataframe(people, vegtables_cum)
    final_df = merge_dataframes(people_df, generated_data)
    print(final_df)


if __name__ == "__main__":
    main()