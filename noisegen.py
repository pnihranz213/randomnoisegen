import pandas as pd
import random
import argparse

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

#function determines if there is a percentage in the string
def percent_in_string(string):
    if "%" in string:
        return True
    else:
        return False

#function finds all the columns in vegtables df that do not have the % character in them
def find_columns_without_percent(data: pd.DataFrame):
    return [columns for columns in data.columns if not percent_in_string(columns)]

#function adds new columns to dataframe based on a list
def add_columns(dataframe, columns):
    for column in columns:
        dataframe[column] = None
    return dataframe    

#using the function random_item, create a dataframe the length of the people dictionary that contains the random item from the vegtables dictionary and has headers equal to the keys in the vegtables dictionary that do not have the % character in them
def create_random_dataframe(people, vegtables):
    random_data = []
    for i in range(len(people['Name'])):
        random_data.append(random_item(vegtables))
    return pd.DataFrame(random_data, columns=find_keys_without_percent(vegtables))

#merge the two dataframes with people appearing on the left
def merge_dataframes(left, right):
    return pd.concat([left, right], axis=1)

#read in csv files and turn them into dictionaries in which the keys are the column names and their values are put into lists
def read_csv(file):
    data = pd.read_csv(file)
    return data.to_dict()

#delete any columns with unnamed in the title
def delete_unnamed_columns(data):
    for key in data:
        if 'Unnamed' in key:
            del data[key]
            break
    return data

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--m", help="csv file containing main dataframe")
    parser.add_argument("--n", help="csv file containing noise dataframe")
    parser.add_argument("--o", help="output file")
    args = parser.parse_args()
    if args.m:
        master = read_csv(args.m)
        delete_unnamed_columns(master)
    else:
        master = read_csv('people.csv')
        delete_unnamed_columns(master)
    master_df = create_dataframe(master)
    if args.n:
        noise = read_csv(args.n)
        delete_unnamed_columns(noise)
    else:
        noise = read_csv('vegtables.csv')
        delete_unnamed_columns(noise)
        print(noise)
    noise_cum = make_cumulative(noise)
    print(noise_cum)
    generated_data = create_random_dataframe(master_df, noise_cum)
    print(generated_data)
    final_df = merge_dataframes(master_df, generated_data)
    print(final_df)
    if args.o:
        final_df.to_csv(args.o)
    else:
        final_df.to_csv('final.csv')


if __name__ == "__main__":
    main()