import { useState, useEffect } from 'react';
import background from '/homepage-bg.svg';
import './app.css';
import './RecommendationBox.css';
import RecommendationBox from './RecommendationBox';
import gcloud_logo from '/gcloud.svg';
import alpaca_logo from '/alpaca.svg';
import benzinga_logo from '/benzinga.svg';

// Format of the data we get from the API
type Recommendation = {
  buy: number;
  close_price: number;
  high_price: number;
  hold: number;
  low_price: number;
  open_price: number;
  sell: number;
  time: string;
  volume: number;
}

function App() {

  const [lastUpdated, setLastUpdated] = useState(undefined);
  const [recommendations, setRecommendations] = useState([]);

  useEffect(() => {

    const getRecommendations = async () => {
      const response = await fetch('https://storage.googleapis.com/585_stock_data_bucket/company_data.json', {
        mode: 'cors'
      });
      const data = await response.json();
      setRecommendations(data);
    }

    getRecommendations();

  }, []);

  useEffect(() => console.log(recommendations), [recommendations]);

  return (
    <div className="App">
      <div className="header">
        <img src={background} width="100%" height="100%" id="background-img" />
        <div className="content">
          <h1 id="title">Stock Recommendations</h1>

          <div className="recommendations">
            {Object.entries(recommendations).map(([key, recommendation]: [string, Recommendation], index) => {

              const percentSell = recommendation.sell;
              const percentBuy = recommendation.buy;
              const percentHold = recommendation.hold;

              let recommendationString: string = "HOLD";
              let sentiment: number = percentHold;

              if (percentSell > percentBuy && percentSell > percentHold) {
                recommendationString = "SELL";
                sentiment = percentSell;
              } else if (percentBuy > percentSell && percentBuy > percentHold) {
                recommendationString = "BUY";
                sentiment = percentBuy;
              }

              return (
                <RecommendationBox key={index} symbol={key} currentPrice={recommendation.high_price} recommendation={recommendationString} sentiment={sentiment} />
              );
            })}
          </div>
        </div>
      </div>
      <div className="credits">
        <h3>Powered by:</h3>
        <img src={gcloud_logo} width="150px" height="50px" id="gcloud-logo" />
        <img src={alpaca_logo} width="150px" height="30px" id="alpaca-logo" />
        <img src={benzinga_logo} width="150px" height="50px" id="benzinga-logo" />
        <p>Made with ❤️ by CPS 585 - Group 1: <a href="https://github.com/CJT157/585Project" target="_blank" rel="noopener noreferrer">GitHub</a></p>
      </div>
    </div>
  )
}

export default App
