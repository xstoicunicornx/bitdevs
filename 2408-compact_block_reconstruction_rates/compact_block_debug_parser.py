import re
from datetime import datetime
import pandas as pd

unhanded_lines = []

def parse_datetime(datetime_string):
    if '.' not in datetime_string:
        datetime_string = datetime_string.replace('Z', '.0Z')
    return datetime.strptime(datetime_string, '%Y-%m-%dT%H:%M:%S.%fZ')

def parse(debug_file_location, num_of_blocks):
    with open(debug_file_location) as f:
        # cache will hold block until update tip message is read
        # cache entries should be structured as: 
        #   {
        #       'block': <blockhash>,
        #       'height': <blockheight>,
        #       'initialized': <timestamp of cmpctblock initialized>,
        #       'reconstructed': <timestamp of cmpctblock reconstructed>,
        #       'tip_updated': <timestamp of update tip>,
        #       'prefilled': <number of prefilled txs>,
        #       'mempool': <number of txs taken from mempool>,
        #       'extrapool': <number of txs taken from extra pool>,
        #       'requested': <number of txs requested from peer>
        #   }
        #   
        #   all fields are optional except for block
        cache = []
        for line in f:
            entry = {}
    
            if re.search(r'^.*\[cmpctblock\] Initialized PartiallyDownloadedBlock.*$', line):
                words = line.split(' ')
                entry['initialized'] = parse_datetime(words[0])
                entry['block'] = words[6]
            elif re.search('Saw new cmpctblock header', line):
                words = line.split(' ')
                entry['initialized'] = parse_datetime(words[0])
                entry['block'] = words[5].replace('hash=', '')
            elif re.search(r'^.*\[cmpctblock\] Successfully reconstructed.*$', line):
    
                words = line.split(' ')
                entry['reconstructed'] = parse_datetime(words[0])
                entry['block'] = words[5]
                entry['prefilled'] = int(words[7])
                entry['mempool'] = int(words[10])
                entry['extrapool'] = int(words[17])
                entry['requested'] = int(words[22])
            # this message seems to log individual txs that were needed so ignore 
            elif re.search(r'^.*\[cmpctblock\] Reconstructed.*$', line):
                # words = line.split(' ')
                # entry['reconstructed'] = datetime.strptime(words[0], '%Y-%m-%dT%H:%M:%SZ')
                # entry['block'] = words[4]
                continue
            elif re.search('^.*UpdateTip.*$', line):
                words = line.split(' ')
                entry['tip_updated'] = parse_datetime(words[0])
                entry['block'] = words[3].replace('best=', '')
                entry['height'] = int(words[4].replace('height=', ''))
            elif re.search('cmpctblock', line):
                unhanded_lines.append(line)
            else:
                continue
    
            cache.append(entry)
    
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width',1000)  
    pd.set_option('display.float_format', '{:.0f}'.format)
    
    log_df = pd.json_normalize(cache)
    block_df = log_df.groupby('block').min().dropna(subset = ['reconstructed', 'initialized']).sort_values('height').reset_index()
    block_df['lag_micros'] = block_df.apply(lambda x: (x['reconstructed'] - x['initialized']).total_seconds() * 1000000, 1)
    block_df['block_abbr'] = block_df.block.apply(lambda x: x[:4]) + '...' + block_df.block.apply(lambda x: x[-15:])

    print(block_df[['height', 'block_abbr', 'initialized', 'reconstructed', 'prefilled', 'mempool', 'extrapool', 'requested', 'lag_micros']].tail(num_of_blocks).to_string(index=False))

if __name__ == '__main__':
    parse('./debug.log', 50)
