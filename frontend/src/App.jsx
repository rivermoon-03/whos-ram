import { useState, useEffect, useMemo } from 'react'
import axios from 'axios'
import Highcharts from 'highcharts'
import HighchartsReact from 'highcharts-react-official'
import './index.css'

const isLocal = window.location.hostname === 'localhost';
const API_BASE = import.meta.env.VITE_API_URL || (isLocal ? "http://localhost:8000" : "/api");
const API_KEY = (import.meta.env.VITE_API_KEY || "your-secret-key-here").trim();

const api = axios.create({
  baseURL: API_BASE,
  headers: { 'X-API-KEY': API_KEY }
});

const HighchartsReactComp = HighchartsReact.default || HighchartsReact;

function App() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('');

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      const res = await api.get('products');
      setProducts(res.data);
      if (res.data.length > 0) {
          const has16 = res.data.find(p => p.name.includes('16GB'));
          setActiveTab(has16 ? '16GB' : res.data[0].name.split(' ').pop());
      }
    } catch (err) {
      console.error("데이터 로드 실패:", err);
    } finally {
      setLoading(false);
    }
  };

  const capacities = useMemo(() => {
      const caps = products.map(p => p.name.split(' ').pop());
      return [...new Set(caps)].sort((a, b) => parseInt(a) - parseInt(b));
  }, [products]);

  const activeProduct = useMemo(() => {
      return products.find(p => p.name.includes(activeTab));
  }, [products, activeTab]);

  return (
    <div className="container">
      <header>
        <h1>WHO'S RAM?</h1>
      </header>

      <div className="tabs">
          {capacities.map(cap => (
              <button 
                key={cap} 
                className={activeTab === cap ? 'active' : ''}
                onClick={() => setActiveTab(cap)}
              >
                  {cap}
              </button>
          ))}
      </div>

      <main>
        {loading ? (
          <div className="status">데이터 동기화 중...</div>
        ) : activeProduct ? (
          <ProductDisplay product={activeProduct} />
        ) : (
          <div className="status">등록된 상품이 없습니다.</div>
        )}
      </main>
    </div>
  )
}

function ProductDisplay({ product }) {
  const [range, setRange] = useState('1w'); // 기본 1주일

  const { history, minTime } = useMemo(() => {
      const now = new Date();
      let threshold = new Date();
      
      if (range === '3d') threshold.setDate(now.getDate() - 3);
      else if (range === '1w') threshold.setDate(now.getDate() - 7);
      else if (range === '3w') threshold.setDate(now.getDate() - 21);
      else if (range === '1m') threshold.setMonth(now.getMonth() - 1);
      else if (range === '3m') threshold.setMonth(now.getMonth() - 3);

      const filtered = (product.price_history || [])
        .filter(h => new Date(h.timestamp) >= threshold)
        .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));

      return { history: filtered, minTime: threshold.getTime() };
  }, [product, range]);

  const chartData = useMemo(() => {
      return [...history].map(h => [
          new Date(h.timestamp).getTime(),
          h.price
      ]).sort((a,b) => a[0] - b[0]);
  }, [history]);

  const currentPrice = (product.price_history || []).length > 0 
    ? [...product.price_history].sort((a,b) => new Date(b.timestamp) - new Date(a.timestamp))[0].price 
    : 0;

  const options = {
    title: { text: null },
    chart: { 
        backgroundColor: 'transparent',
        height: 350,
        style: { fontFamily: 'Inter, sans-serif' }
    },
    xAxis: { 
        type: 'datetime',
        min: minTime, // 가로축 시작점 고정
        max: new Date().getTime(), // 가로축 끝점(현재) 고정
        labels: { style: { color: '#8b949e' } },
        lineColor: '#30363d',
        tickColor: '#30363d'
    },
    yAxis: { 
        title: { text: null },
        labels: { 
            style: { color: '#8b949e' },
            formatter: function() { return this.value.toLocaleString() + '원'; }
        },
        gridLineColor: '#30363d'
    },
    series: [{
      name: '가격',
      data: chartData,
      color: '#58a6ff',
      lineWidth: 3,
      marker: {
          enabled: chartData.length < 50,
          radius: 4,
          fillColor: '#58a6ff'
      }
    }],
    tooltip: { 
        backgroundColor: '#161b22',
        style: { color: '#e6edf3' },
        borderWidth: 1,
        borderColor: '#30363d',
        xDateFormat: '%Y년 %m월 %d일 %H:%M',
        valueSuffix: '원'
    },
    credits: { enabled: false },
    legend: { enabled: false }
  };

  return (
    <div className="display-card">
        <div className="display-header">
            <div className="display-info">
                <h2>{product.name}</h2>
                <div className="current-price">
                    {currentPrice.toLocaleString()}<span>원</span>
                </div>
            </div>
        </div>

        <div className="chart-section">
            <HighchartsReactComp highcharts={Highcharts} options={options} />
            
            <div className="range-selector">
                {['3d', '1w', '3w', '1m', '3m'].map(r => (
                    <button 
                        key={r}
                        className={range === r ? 'active' : ''}
                        onClick={() => setRange(r)}
                    >
                        {r.toUpperCase()}
                    </button>
                ))}
            </div>
        </div>
        <div className="history-section">
            <h4>얼마나 비싸짐?</h4>
            <table>
                <thead>
                    <tr>
                        <th>날짜</th>
                        <th>가격</th>
                    </tr>
                </thead>
                <tbody>
                    {history.filter((h, i, self) => 
                        i === self.findIndex(t => 
                            new Date(t.timestamp).toLocaleDateString() === new Date(h.timestamp).toLocaleDateString()
                        )
                    ).map((h, i) => (
                        <tr key={i}>
                            <td className="td-date">{new Date(h.timestamp).toLocaleDateString()}</td>
                            <td className="td-price">{h.price.toLocaleString()}원</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    </div>
  );
}

export default App
