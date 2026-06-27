def optimize_trip(flights, hotels, budget):
    best_option = None
    best_price = None

    for f in flights:
        for h in hotels:
            total = f["total_price"] + h["total_price"]

            if total <= budget:
                if best_price is None or total < best_price:
                    best_price = total
                    best_option = {
                        "flight": f,
                        "hotel": h,
                        "total_cost": total
                    }

    return best_option