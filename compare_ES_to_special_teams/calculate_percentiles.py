import pandas as pd

"""
The purpose of the script is to read the three csv files and generate a dictionary which, for each player season, 
contains the following:
{
    'player_season': {
        'position': _,
        'EV_xGF': _,
        'EV_xGA': _,
        'PP_xGF': _,
        'SH_xGA': _
    }
}
where each value corresponds to the players percentile in that specific metric, in that season, if the TOI cutoff is 
met. After this dict is fully constructed, the results will be read into a final csv containing all of the percentile 
data.
"""

DATA_PATH = '..\\data\\evolving_hockey\\{}_RAPM_2009_2020.csv'

GAMESTATE_USECOLS_MAPPING = {  # Just do we don't read unnecessary columns
    'EV': ['EH_ID', 'Season', 'Position', 'Birthday', 'xGF/60', 'xGA/60'],
    'PP': ['EH_ID', 'Season', 'Position', 'Birthday', 'xGF/60'],
    'SH': ['EH_ID', 'Season', 'Position', 'Birthday', 'xGA/60']
}


def add_to_dict(dictionary, dict_value, dataframe, column, ascending=True):
    total = float(len(dataframe))
    for index, row in dataframe.sort_values(column, axis=0, ascending=ascending).reset_index().iterrows():
        # Use a combination of player name, birth year, and season to make sure each player_season is unique
        player_season = '{}_{}_{}'.format(row['EH_ID'], row['Birthday'].split('-')[0], row['Season'])
        if dictionary.get(player_season, None):
            dictionary[player_season][dict_value] = (float(index) / total) * 100.0
        else:
            dictionary[player_season] = {
                'position': row['Position'],
                dict_value: float(index) / total
            }

    return dictionary


def create_dict():
    master_dict = dict()
    for game_state in ['EV', 'PP', 'SH']:
        df = pd.read_csv(DATA_PATH.format(game_state), usecols=GAMESTATE_USECOLS_MAPPING[game_state])
        if game_state == 'EV':
            master_dict = add_to_dict(master_dict, 'EV_xGF', df, 'xGF/60', ascending=False)
            master_dict = add_to_dict(master_dict, 'EV_xGA', df, 'xGA/60', ascending=True)
        elif game_state == 'PP':
            master_dict = add_to_dict(master_dict, 'PP_xGF', df, 'xGF/60', ascending=False)
        elif game_state == 'SH':
            master_dict = add_to_dict(master_dict, 'SH_xGA', df, 'xGA/60', ascending=True)

    return master_dict


def write_csv_from_dict(dictionary):
    from csv import DictWriter
    with open('percentile_results.csv', 'w', newline='') as csv_output:
        fieldnames = ['player_season', 'player', 'position', 'EV_xGF', 'EV_xGA', 'PP_xGF', 'SH_xGA', 'xGF_diff',
                      'xGA_diff']
        writer = DictWriter(csv_output, fieldnames=fieldnames)
        writer.writeheader()
        for player_season in dictionary.keys():
            if not(dictionary[player_season].get('EV_xGF', False) and dictionary[player_season].get('EV_xGA', False)):
                continue
            if dictionary[player_season].get('PP_xGF', False):
                xGF_diff = dictionary[player_season].get('EV_xGF', '') - dictionary[player_season].get('PP_xGF', '')
            else:
                xGF_diff = ''
            if dictionary[player_season].get('SH_xGA', False):
                xGA_diff = dictionary[player_season].get('EV_xGA', '') - dictionary[player_season].get('SH_xGA', '')
            else:
                xGA_diff = ''
            writer.writerow({
                'player_season': player_season,
                'player': player_season.split('_')[0] + player_season.split('_')[2],
                'position': dictionary[player_season]['position'],
                'EV_xGF': dictionary[player_season].get('EV_xGF', ''),
                'EV_xGA': dictionary[player_season].get('EV_xGA', ''),
                'PP_xGF': dictionary[player_season].get('PP_xGF', ''),
                'SH_xGA': dictionary[player_season].get('SH_xGA', ''),
                'xGF_diff': xGF_diff,
                'xGA_diff': xGA_diff
            })


if __name__ == '__main__':
    print("Let's get started")
    master_dictionary = create_dict()
    print("Dictionary created, writing to csv...")
    write_csv_from_dict(master_dictionary)
    print('All done')
