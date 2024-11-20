def build_query(summary):
    if 'Fraud' in summary:
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
            summary["Type of Card"], 
            summary["Entry Mode"], 
            summary["Average Amount"], 
            summary["Type of Transaction"], 
            summary["Merchant Group"], 
            summary["Country of Transaction"], 
            summary["Shipping Address"], 
            summary["Country of Residence"],
            summary["Bank"],
            summary["Fraud"]
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
            summary["Type of Card"], 
            summary["Entry Mode"], 
            summary["Average Amount"], 
            summary["Type of Transaction"], 
            summary["Merchant Group"], 
            summary["Country of Transaction"], 
            summary["Shipping Address"], 
            summary["Country of Residence"],
            summary["Bank"]
            )

    return query, data