def build_summaries(docs):

# total of each card type JSON
# total of each entry mode JSON
# average amount float
# total of each transaction type JSON
# total country of transaction JSON
# total shipping address countries  JSON
# total Country of residence JSON
# total of each bank JSON
# fraud count

    all_entry = {'card_type': {},
                 'entry_mode': {},
                 'average_amount': [],
                 'transaction_type': {},
                 'transaction_country': {},
                 'shipping_address_country': {},
                 'residence_country': {},
                 'bank': {},
                 'fraud_count': 0}
    
    fraud_entry = {'card_type': {},
                 'entry_mode': {},
                 'average_amount': [],
                 'transaction_type': {},
                 'transaction_country': {},
                 'shipping_address_country': {},
                 'residence_country': {},
                 'bank': {}}
    
    for doc in docs:

        if doc["fraud"] == 1:
             count_data(fraud_entry, doc, True)
        else:
             count_data(all_entry, doc, False)

    return [all_entry, fraud_entry]


def count_data(all_entry_dict, fraud_entry_dict, data_dict, is_fraud):
    categories = ["card_type", "entry_mode", "transaction_type", "transaction_country", "shippint_address_country", "residence_country", "bank"]

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

    all_entry_dict["average_amount"].append(data_dict["transaction_amount"])

    if is_fraud:
        fraud_entry_dict["average_amount"].append(data_dict["transaction_amount"])
        all_entry_dict["fraud_count"] += 1

