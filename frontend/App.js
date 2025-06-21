import React, { useState } from "react";

function App() {
  const [ticker, setTicker] = useState("");
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  const fetchStockData = async () => {
    try {
      const response = await fetch(`/api/stock?ticker=${ticker}`);
      if (!response.ok) throw new Error("Failed to fetch data");
      const result = await response.json();
      setData(result);
      setError(null);
    } catch (err) {
      setError(err.message);
      setData(null);
    }
  };

  return (
    <div className="p-4 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Mini Bloomberg Terminal</h1>

      <input
        type="text"
        placeholder="Enter Ticker (e.g., AAPL)"
        value={ticker}
        onChange={(e) => setTicker(e.target.value)}
        className="border p-2 rounded w-full mb-4"
      />

      <button
        onClick={fetchStockData}
        className="bg-blue-600 text-white px-4 py-2 rounded"
      >
        Fetch Data
      </button>

      {error && <p className="text-red-600 mt-4">{error}</p>}

      {data && (
        <div className="mt-6">
          <h2 className="text-xl font-semibold mb-2">{data.ticker} Valuation Multiples</h2>
          <ul className="list-disc list-inside">
            {Object.entries(data.multiples).map(([key, value]) => (
              <li key={key}><strong>{key}:</strong> {value}</li>
            ))}
          </ul>

          <h2 className="text-xl font-semibold mt-6 mb-2">Recent Prices</h2>
          <ul className="text-sm h-60 overflow-y-scroll border rounded p-2">
            {data.historical_data.slice(-30).map((row, idx) => (
              <li key={idx}>{row.Date}: ${row.Close.toFixed(2)}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;

