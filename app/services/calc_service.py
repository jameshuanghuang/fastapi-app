import math

def norm_cdf(x):
    return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0

def linspace(start, stop, step):
    values = []
    current = start
    while current <= stop:
        values.append(round(current, 10))
        current += step
    return values

def blsprice(S0, K, T, rfr, q1, sigma):
    if T > 0:
        d1 = (math.log(S0 / K) + (rfr - q1 + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
        d2 = d1 - sigma * math.sqrt(T)
        call_price = S0 * math.exp(-q1 * T) * norm_cdf(d1) - K * math.exp(-rfr * T) * norm_cdf(d2)
        put_price = K * math.exp(-rfr * T) * norm_cdf(-d2) - S0 * math.exp(-q1 * T) * norm_cdf(-d1)
        return call_price, put_price
    return max(S0 - K, 0), max(K - S0, 0)

def calc(S0=5.0, K=10.0, sigma=0.2, rfr=0.05, T=1, q1=0.01, opt_type="call"):
    support = linspace(-4, 4, 0.20)
    drift = rfr - q1 - 0.5 * sigma ** 2
    diffusion = sigma * math.sqrt(T)
    ST = [S0 * math.exp(drift + diffusion * s) for s in support]
    if opt_type == "call":
        exercised = ["Yes" if s > K else "No" for s in ST]
        payoff = [max(s - K, 0) for s in ST]
    else:
        exercised = ["Yes" if s < K else "No" for s in ST]
        payoff = [max(K - s, 0) for s in ST]

    table_data = [
        {
            "Path": i + 1,
            "S0": round(S0, 2),
            "ST": round(ST[i], 2),
            "Exercised": exercised[i],
            "Payoff": round(payoff[i], 2),
        }
        for i in range(len(ST))
    ]

    call_price, put_price = blsprice(S0, K, T, rfr, q1, sigma)
    price = call_price if opt_type == "call" else put_price
    return round(price, 2), table_data

if __name__ == "__main__":
    pass