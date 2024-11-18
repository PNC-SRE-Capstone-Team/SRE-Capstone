def build_query(entry):
    if 'Fraud' in entry:
        query = """
        INSERT INTO transaction_summaries (
            created_at,
            card_type, 
            entry_mode, 
            average_amount, 
            transaction_type, 
            merchant_group, 
            transaction_country,
            shipping_address,
            residence_country,
            bank,
            fraud_count
        ) VALUES (
            NOW(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )"""

        data = (
            entry["Type of Card"], 
            entry["Entry Mode"], 
            entry["Average Amount"], 
            entry["Type of Transaction"], 
            entry["Merchant Group"], 
            entry["Country of Transaction"], 
            entry["Shipping Address"], 
            entry["Country of Residence"],
            entry["Bank"],
            entry["Fraud"]
            )
    else:
        query = """
        INSERT INTO fraud_summaries (
            created_at,
            card_type, 
            entry_mode, 
            average_amount, 
            transaction_type, 
            merchant_group, 
            transaction_country,
            shipping_address,
            residence_country,
            bank
        ) VALUES (
            NOW(), %s, %s, %s, %s, %s, %s, %s, %s, %s
        )"""

        data = (
            entry["Type of Card"], 
            entry["Entry Mode"], 
            entry["Average Amount"], 
            entry["Type of Transaction"], 
            entry["Merchant Group"], 
            entry["Country of Transaction"], 
            entry["Shipping Address"], 
            entry["Country of Residence"],
            entry["Bank"]
            )

    return query, data