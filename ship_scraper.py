from bs4 import BeautifulSoup
import requests
import unicodedata
import pandas as pd


def get_pages(data):
    print('Getting pages...')
    pages = {}
    soup = BeautifulSoup(data, 'lxml')
    group_divs = soup.find_all('div', {'class': 'mw-category-group'})
    for div in group_divs:
        links = div.find_all('a')
        for link in links:
            title = link.get('title')
            href = link.get('href')
            pages[title] = 'https://en.wikipedia.org' + href
    print(f'Total pages (pre-processing): {len(pages)}')
    return pages


def get_infobox(data):
    soup = BeautifulSoup(data, 'lxml')
    parser_output = soup.find('div', {'class': 'mw-parser-output'})
    table = soup.find('table', {'class': 'infobox'}).find_all('td')
    return [t.getText() for t in table][1:]


def parse_results(results):
    return {
        row_name.replace(':', ''): unicodedata.normalize('NFKD', row_data).strip()
        for row_name, row_data in zip(results[::2], results[1::2])
    }


def process_pages(pages):
    result = {}
    count = 0
    for title, link in pages.items():
        print(f'Processing: {title}, from: {link}')
        data = requests.get(link).content
        info = get_infobox(data)
        result[title] = parse_results(info)
        count += 1
    print(f'Pages processed: {count}')
    return result


def clean_pages(pages):
    return {k: v for k, v in pages.items() if 'Category' not in k and
            'Template' not in k and 
            'List' not in k and 
            'liner' not in k and
            'Big Four' not in k and
            'unfinished' not in k}


def clean_dict(result):
    result['SS Bardic'] = {'Name': 'War Priam (1918-1919), Bardic (1919-1925), Hostilius (1925-1926), Horatius (1926-1933), Kumara (1933-1937), Marathon (1937-1941)',
                          'Owner': 'White Star Line (1919-1925), Aberdeen Line (1925-1933), Shaw, Savill & Albion Co. Ltd. (1933-1937), Fatsis M. (1937-1941)',
                          'Port of registry': 'Piraeus, Greece', 'Builder': 'Harland & Wolff Ltd.', 'Yard Number': '542', 
                           'Launched': '19 December 1918', 'Completed': '13 March 1919', 
                           'Identification': 'SVVL IMO/Off. no.: 904', 'Fate': 'Shelled and sunk 9 March 1941',
                          'Type': 'Cargo ship', 'Tonnage': '8,010 GRT', 'Length': '137.3 metres (450 ft 6 in)',
                          'Beam': '17.8 metres (58 ft 5 in)', 'Depth':'11.3 metres (37 ft 1 in)', 'Installed power': '2 x Triple expansion engines',
                          'Propulsion': 'Two screw propellers', 'Sail plan': 'Liverpool - New York City', 'Speed': '11 knots'}
    result['SS Germanic (1874)'] = {'Name': 'Germanic (1874-1905), Ottawa (1905-1910)', 
                                    'Operator': 'White Star Line (1874-1904), American Line (1904-1905), Dominion Line (1905-1910)',
                                   'Port of registry': 'Liverpool, England', 'Builder': 'Harland & Wolff Ltd.', 'Yard Number': '85',
                                   'Launched': '15 July 1874', 'Completed': '24 April 1875', 'In service': '20 May 1875', 
                                    'Out of service': '1910', 'Fate': 'Sold to Ottoman Empire, 1910', 'Class': 'Britannic class',
                                   'Type': 'Ocean liner', 'Tonnage': '5,008 GRT', 'Length': '455 ft (139 m)', 
                                    'Beam': '45 ft 2 in (13.77 m)', 'Propulsion': 'As built: 8 × boilers, 2 × 2-cylinder compound steam engines, 1 screw propeller, From 1895: Triple-expansion steam engines',
                                   'Speed': '16 knots', 'Capacity': '1,720 passengers: 220 x 1st class, 1500 x 3rd class'}
    
    '''           
    print()
    for key, value in result.items():
        print(key, '--')
        for a, b in value.items():
            print(a, ': ', b)
        print()
    '''
    return result


def generate_df(result):
    df = pd.DataFrame.from_dict(result, orient = 'index')
    df.index.names = ['Ship Name']
    return df


def clean_df(df):
    
    # Rename and remove whitespace from column names
    for col in df.columns:
        if '\n' in col:
            new_col = col.replace('\n', '')
            df.rename(columns = {col: new_col}, inplace = True)

    df.rename(columns = {'Class and type':'Classtype', 'Beam':'Beam (ft)', 'Depth':'Depth (ft)', 
                         'Tonnage':'Tonnage (GRT)', 'Length':'Length (ft)', 'Speed':'Speed (kn)'}, 
                         inplace = True)
    # Remove some of the original variables; may re-add 'Capacity', 'Crew', and 'Fate' later
    new_cols = ['Builder', 'Classtype', 'Class', 'Type', 'Length (ft)', 'Beam (ft)', 'Depth (ft)', 
                'Tonnage (GRT)', 'Speed (kn)', 'Launched', 'Completed', 'Maiden voyage']
    df = df[new_cols]
    
    # Strip whitespace and add spaces in all column values
    for col in df.columns:
        df[col] = df[col].str.replace('\n\n', ' ')
        df[col] = df[col].str.replace('\n', ', ')
        df[col] = df[col].str.replace(r'\[.*\]','', regex=True)
        df[col] = df[col].str.replace(r'\)(?=[a-zA-Z])', '), ', regex=True)
        df[col] = df[col].str.replace(r'(?=[A-Z])(?<=[a-z])', ', ', regex=True)

    # Rename 'Titanic' to 'RMS Titanic'
    df.rename(index={'Titanic': 'RMS Titanic'}, inplace=True)

    # Standardize 'Builder' entries that are Harland & Wolff
    df.Builder[df['Builder'].str.contains('Harland', na=False)] = 'Harland & Wolff, Belfast'
    
    # Standardize 'Tonnage' in Gross Register Tons (GRT)
    df['Tonnage (GRT)'] = df['Tonnage (GRT)'].str.replace(r'(.*):', '', regex=True)
    df['Tonnage (GRT)'] = df['Tonnage (GRT)'].str.replace(r',+', '', regex=True)
    df['Tonnage (GRT)'] = df['Tonnage (GRT)'].str.replace(r'[-]|[–]', ' ', regex=True)
    df['Tonnage (GRT)'] = df['Tonnage (GRT)'].str.replace(r'(?<=[0-9])\s(.*)', '', regex=True)
    #df['Tonnage (GRT)'] = df['Tonnage (GRT)'].astype('int32')
    
    # Standardize 'Speed' in nautical knots
    df['Speed (kn)'] = df['Speed (kn)'].str.replace(r'(.*):', '', regex=True)
    df['Speed (kn)'] = df['Speed (kn)'].str.replace(r'[-]|[–]', ' ', regex=True)
    df['Speed (kn)'] = df['Speed (kn)'].str.replace(r'(?<=[0-9])\s(.*)', '', regex=True)
    #df['Speed (kn)'] = df['Speed (kn)'].astype('int32')

    # Clean and standardize 'Length' in feet
    df['Length (ft)'] = df['Length (ft)'].str.replace('feet', 'ft')
    df['Length (ft)'] = df['Length (ft)'].str.replace('ft.', 'ft', regex=False)
    df['Length (ft)'] = df['Length (ft)'].str.replace('inches', 'in')
    df['Length (ft)'] = df['Length (ft)'].str.replace('in.', 'in', regex=False)
    df['Length (ft)'] = df['Length (ft)'].str.replace(r'(?<=[0-9])\s(?=[ft|in]*)', '', regex=True)
    df['Length (ft)'] = df['Length (ft)'].str.replace(r'(?<=[ft|in])\s\((.*)', '', regex=True)
    df['Length (ft)'] = df['Length (ft)'].str.replace(r'(\d+(?:\.\d+)?)(m)\s', '', regex=True)
    df['Length (ft)'] = df['Length (ft)'].str.replace(r'(\d+(?:\.\d+)?)(metres)\s', '', regex=True)
    df['Length (ft)'] = df['Length (ft)'].str.replace(r'(to)(.*)(?=(ft))', '', regex=True)
    df['Length (ft)'] = df['Length (ft)'].str.replace(r'\(', '', regex=True)
    df['Length (ft)'] = df['Length (ft)'].str.replace(r'\)', '', regex=True)
    df[['Length_ft', 'Length_in']] = df['Length (ft)'].str.extract(r'(?:(\d+(?:\.\d+)?)ft)?\s*(?:(\d+)in)?').fillna(0).astype('float') # If no value given, filled with zero
    df['Length (ft)'] = round(((df['Length_ft'] * 12) + df['Length_in'])/12, 1)
    df = df.drop(columns=['Length_ft', 'Length_in'])
    
    # Clean and standardize 'Beam' in feet
    df['Beam (ft)'] = df['Beam (ft)'].str.replace('feet', 'ft')
    df['Beam (ft)'] = df['Beam (ft)'].str.replace('ft.', 'ft', regex=False)
    df['Beam (ft)'] = df['Beam (ft)'].str.replace('inches', 'in')
    df['Beam (ft)'] = df['Beam (ft)'].str.replace('in.', 'in', regex=False)
    df['Beam (ft)'] = df['Beam (ft)'].str.replace(r'(?<=[0-9])\s(?=[ft|in]*)', '', regex=True)
    df['Beam (ft)'] = df['Beam (ft)'].str.replace(r'(?<=[ft|in])\s\((.*)', '', regex=True)
    df['Beam (ft)'] = df['Beam (ft)'].str.replace(r'(\d+(?:\.\d+)?)(m)\s', '', regex=True)
    df['Beam (ft)'] = df['Beam (ft)'].str.replace(r'(\d+(?:\.\d+)?)(metres)\s', '', regex=True)
    df['Beam (ft)'] = df['Beam (ft)'].str.replace(r'(to)(.*)(?=(ft))', '', regex=True)
    df['Beam (ft)'] = df['Beam (ft)'].str.replace(r'\(', '', regex=True)
    df['Beam (ft)'] = df['Beam (ft)'].str.replace(r'\)', '', regex=True)
    df[['Beam_ft', 'Beam_in']] = df['Beam (ft)'].str.extract(r'(?:(\d+(?:\.\d+)?)ft)?\s*(?:(\d+)in)?').fillna(0).astype('float') # If no value given, filled with zero
    df['Beam (ft)'] = round(((df['Beam_ft'] * 12) + df['Beam_in'])/12, 1)
    df = df.drop(columns=['Beam_ft', 'Beam_in'])
    
    # Clean and standardize 'Depth' in feet
    df['Depth (ft)'] = df['Depth (ft)'].str.replace('feet', 'ft')
    df['Depth (ft)'] = df['Depth (ft)'].str.replace('ft.', 'ft', regex=False)
    df['Depth (ft)'] = df['Depth (ft)'].str.replace('inches', 'in')
    df['Depth (ft)'] = df['Depth (ft)'].str.replace('in.', 'in', regex=False)
    df['Depth (ft)'] = df['Depth (ft)'].str.replace(r'(?<=[0-9])\s(?=[ft|in]*)', '', regex=True)
    df['Depth (ft)'] = df['Depth (ft)'].str.replace(r'(?<=[ft|in])\s\((.*)', '', regex=True)
    df['Depth (ft)'] = df['Depth (ft)'].str.replace(r'(\d+(?:\.\d+)?)(m)\s', '', regex=True)
    df['Depth (ft)'] = df['Depth (ft)'].str.replace(r'(\d+(?:\.\d+)?)(metres)\s', '', regex=True)
    df['Depth (ft)'] = df['Depth (ft)'].str.replace(r'(to)(.*)(?=(ft))', '', regex=True)
    df['Depth (ft)'] = df['Depth (ft)'].str.replace(r'\(', '', regex=True)
    df['Depth (ft)'] = df['Depth (ft)'].str.replace(r'\)', '', regex=True)
    df[['Depth_ft', 'Depth_in']] = df['Depth (ft)'].str.extract(r'(?:(\d+(?:\.\d+)?)ft)?\s*(?:(\d+)in)?').fillna(0).astype('float') # If no value given, filled with zero
    df['Depth (ft)'] = round(((df['Depth_ft'] * 12) + df['Depth_in'])/12, 1)
    df = df.drop(columns=['Depth_ft', 'Depth_in'])

    # Strip any characters after year in 'Launched'
    df['Launched'] = df['Launched'].str.replace(r'(?<=[0-9]{4}).*$', '', regex=True)
    
    # Remove ports of departure and arrival from 'Maiden voyage'
    df['Maiden voyage'] = df['Maiden voyage'].str.replace(r'([a-zA-Z]+)[^\w\s]([a-zA-Z]+(?:\s*[a-zA-Z]+)),\s(?=([0-9].*))', '', regex=True)
    df['Maiden voyage'] = df['Maiden voyage'].str.replace(r'(?<=[0-9]{4}).*$', '', regex=True)

    # Combine 'Class' and 'Type' into 'Classtype'
    df['Type'] = df['Type'].str.lower()
    
    cols = ['Classtype', 'Class', 'Type']
    df['Check1'] = df.apply(lambda x: str(x.Class) in str(x.Classtype), axis=1)
    df['Check2'] = df.apply(lambda x: str(x.Type) in str(x.Classtype), axis=1)
    pd.options.mode.chained_assignment = None
    for x in range(0, len(df['Check1'])):
        if df['Check1'][x] == True:
            df['Class'][x] = '' # If 'Class' value already included in 'Classtype' value, delete 'Class' value
        if df['Check2'][x] == True:
            df['Type'][x] = '' # If 'Type' value already included in 'Classtype' value, delete 'Type' value
    df['Classtype']=df[cols].fillna('').apply(pd.unique,1).apply(' '.join).str.rstrip(' ')
    
    df['Classtype'] = df['Classtype'].str.replace('  ', ' ')
    df['Classtype'] = df['Classtype'].str.replace('Class', 'class')
    df['Classtype'] = df['Classtype'].str.replace(' class', '-class')
    df['Classtype'] = df['Classtype'].str.replace(r'^\s', '', regex=True)
    df['Classtype'] = df['Classtype'].str.replace(r',.*', '', regex=True)
    df['Classtype'] = df['Classtype'].apply(lambda x: x[0].upper() + x[1:] if len(x) != 0 else '')
    df = df.drop(columns=['Check1', 'Check2', 'Class', 'Type'])
    df.rename(columns = {'Classtype':'Class/type'}, inplace = True)

    # Abbreviate month names
    months = {'January': 'Jan', 'February': 'Feb', 'March': 'Mar', 'April': 'Apr', 'May': 'May',
              'June': 'Jun', 'July': 'Jul', 'August': 'Aug', 'September': 'Sep', 'October': 'Oct',
              'November': 'Nov', 'December': 'Dec'}
    for col in df.columns[7:10]:
        for key in months:
            df[col] = df[col].str.replace(key, months[key])

    return df


def main():
    url = 'https://en.wikipedia.org/wiki/Category:Ships_of_the_White_Star_Line'
    data_pages = requests.get(url).content
    pages = get_pages(data_pages)
    pages = clean_pages(pages)
    result = process_pages(pages)
    result_dict = clean_dict(result)
    result_df = generate_df(result_dict)
    final_df = clean_df(result_df)
    final_df.to_csv('ships.csv', encoding='utf-8-sig')


if __name__ == "__main__":
    main()
