// In src/App.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Plot from 'react-plotly.js';

function App() {
    const [data, setData] = useState([]);

    useEffect(() => {
        axios.get('http://localhost:8000/api/historical-data/')
            .then(response => setData(response.data))
            .catch(error => console.error(error));
    }, []);

    const plotData = {
        x: data.map(item => item.date),
        y: data.map(item => item.close),
        type: 'scatter',
        mode: 'lines+markers',
        marker: {color: 'red'},
    };

    return (
        <div>
            <h1>Stock Data Visualization</h1>
            <Plot
                data={[plotData]}
                layout={{width: 720, height: 440, title: 'Stock Prices'}}
            />
        </div>
    );
}

export default App;
