def generate_recommendation(predicted_profit):

    if predicted_profit < 0:
        return (
            "Loss Expected",
            "Reduce discounts, review pricing strategy, and optimize inventory."
        )

    elif predicted_profit < 100:
        return (
            "Low Profit",
            "Increase promotional activities and improve product visibility."
        )

    elif predicted_profit < 500:
        return (
            "Moderate Profit",
            "Maintain the current strategy while monitoring sales trends."
        )

    else:
        return (
            "High Profit",
            "Increase inventory and marketing efforts to maximize revenue."
        )

if __name__ == "__main__":

    profit = 320

    status, recommendation = generate_recommendation(profit)

    print(status)
    print(recommendation)