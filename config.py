from request.get_dates import get_dates
config = get_dates().get("durations")
work_day = 15
amount = []
agree_time = []
featured = []
features = []

for configuration in config:
    amount.append(int(configuration["price"]))
    agree_time.append(configuration['time'])
    featured.append(configuration['featured'])
    features.append(configuration['features'])

print(amount, agree_time, featured, features)

