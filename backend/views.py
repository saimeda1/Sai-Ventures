from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from Webscraper import get_historical_data, get_multiples


@csrf_exempt
def get_stock_data(request):
    """
    Endpoint: /api/stock?ticker=AAPL
    Returns historical price data and valuation multiples for the given stock ticker.
    """
    ticker = request.GET.get("ticker")
    if not ticker:
        return JsonResponse({"error": "Missing 'ticker' parameter"}, status=400)

    try:
        hist_df = get_historical_data(ticker)
        multiples = get_multiples(ticker)

        hist_json = hist_df[['Date', 'Close']].dropna().to_dict(orient='records')

        return JsonResponse({
            "ticker": ticker,
            "historical_data": hist_json,
            "multiples": multiples
        }, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
