import json

def build_summaries(docs):

# total of each card type JSON
# total of each entry mode JSON
# average amount float
# total of each transaction type JSON
# total country of transaction JSON
# total shipping address countries  JSON
# total Country of residence JSON
# total of each Bank JSON
# fraud count

    all_entry = {'Type of Card': {},
                 'Entry Mode': {},
                 'Average Amount': [],
                 'Type of Transaction': {},
                 'Merchant Group': {},
                 'Country of Transaction': {},
                 'Shipping Address': {},
                 'Country of Residence': {},
                 'Bank': {},
                 'Fraud': 0}
    
    fraud_entry = {'Type of Card': {},
                 'Entry Mode': {},
                 'Average Amount': [],
                 'Type of Transaction': {},
                 'Merchant Group': {},
                 'Country of Transaction': {},
                 'Shipping Address': {},
                 'Country of Residence': {},
                 'Bank': {}}
    
    for doc in docs:

        if doc["Fraud"] == '1':
             count_data(all_entry, fraud_entry, doc, True)
        else:
             count_data(all_entry, fraud_entry, doc, False)

    #get average amount

    all_entry['Average Amount'] = get_average_amount(all_entry['Average Amount'])
    fraud_entry['Average Amount'] = get_average_amount(fraud_entry['Average Amount'])

    jsonify(all_entry, fraud_entry)

    return [all_entry, fraud_entry]


def count_data(all_entry_dict, fraud_entry_dict, data_dict, is_fraud):
    categories = ["Type of Card", "Entry Mode", "Type of Transaction", "Merchant Group", "Country of Transaction", "Shipping Address", "Country of Residence", "Bank"]

    for category in categories:
        if data_dict[category] in all_entry_dict[category]:
                all_entry_dict[category][data_dict[category]] += 1
        else:
            all_entry_dict[category].update({data_dict[category]: 1})

        if is_fraud:
            if data_dict[category] in fraud_entry_dict[category]:
                fraud_entry_dict[category][data_dict[category]] += 1
            else:
                fraud_entry_dict[category].update({data_dict[category]: 1})
                

    all_entry_dict["Average Amount"].append(data_dict["Amount"])

    if is_fraud:
        fraud_entry_dict["Average Amount"].append(data_dict["Amount"])
        all_entry_dict["Fraud"] += 1

def get_average_amount(amounts):
     nums = []
     for amount in amounts:
          nums.append(int(amount[1:]))

     return '£' + str(round(sum(nums) / len(nums), 2))

def jsonify(all, fraud):
     categories = ["Type of Card", "Entry Mode", "Type of Transaction", "Merchant Group", "Country of Transaction", "Shipping Address", "Country of Residence", "Bank"]

     for category in categories:
          all[category] = json.dumps(all[category])
          fraud[category] = json.dumps(fraud[category])