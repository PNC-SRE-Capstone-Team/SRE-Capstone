import json

def build_summaries(docs):

    all_transactions = {'Type of Card': {},
                 'Entry Mode': {},
                 'Average Amount': [],
                 'Type of Transaction': {},
                 'Merchant Group': {},
                 'Country of Transaction': {},
                 'Shipping Address': {},
                 'Country of Residence': {},
                 'Bank': {},
                 'Fraud': 0}
    
    fraud_transactions = {'Type of Card': {},
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
             count_data(all_transactions, fraud_transactions, doc, True)
        else:
             count_data(all_transactions, fraud_transactions, doc, False)

    #get average amount

    all_transactions['Average Amount'] = get_average_amount(all_transactions['Average Amount'])
    fraud_transactions['Average Amount'] = get_average_amount(fraud_transactions['Average Amount'])

    jsonify(all_transactions, fraud_transactions)

    return [all_transactions, fraud_transactions]


def count_data(all_transactions_dict, fraud_transactions_dict, data_dict, is_fraud):
    categories = ["Type of Card", "Entry Mode", "Type of Transaction", "Merchant Group", "Country of Transaction", "Shipping Address", "Country of Residence", "Bank"]

    for category in categories:
        if data_dict[category] in all_transactions_dict[category]:
                all_transactions_dict[category][data_dict[category]] += 1
        else:
            all_transactions_dict[category].update({data_dict[category]: 1})

        if is_fraud:
            if data_dict[category] in fraud_transactions_dict[category]:
                fraud_transactions_dict[category][data_dict[category]] += 1
            else:
                fraud_transactions_dict[category].update({data_dict[category]: 1})
                

    all_transactions_dict["Average Amount"].append(data_dict["Amount"])

    if is_fraud:
        fraud_transactions_dict["Average Amount"].append(data_dict["Amount"])
        all_transactions_dict["Fraud"] += 1

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