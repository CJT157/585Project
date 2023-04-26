import { useState, useEffect } from 'react';
import background from '/homepage-bg.svg';
import './app.css';
import './RecommendationBox.css';
import RecommendationBox from './RecommendationBox';
import gcloud_logo from '/gcloud.svg';
import alpaca_logo from '/alpaca.svg';
import benzinga_logo from '/benzinga.svg';
import site_logo from '/logo.svg';

// Format of the data we get from the API
type Recommendation = {
  // The % of analysts who recommend buying this stock
  buy: number;
  // The price of the stock when the market last closed
  close_price: number;
  // The highest recorded price of the stock today
  high_price: number;
  // The % of analysts who recommend holding this stock
  hold: number;
  // The lowest recorded price of the stock today
  low_price: number;
  // The price of the stock when the market last opened
  open_price: number;
  // The % of analysts who recommend selling this stock
  sell: number;
  // The time the data was last updated
  time: string;
  // The total number of shares traded today
  volume: number;
}

function App() {

  // The list of recommendations we get from the API
  const [recommendations, setRecommendations] = useState([]);


  // Fetch the recommendations from the API and update the state accordingly
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

  return (
    <div className="App">
      <div className="header">
        <img src={background} width="100%" height="100%" id="background-img" />
        <div className="content">
          <img src={site_logo} width="150px" height="150px" id="site-logo" />
          <h1 id="title">Stock Recommendations</h1>

          <div className="recommendations">
            {/* Iterate through each recommendation, calculate the highest percentage recommended, and render a box with the corresponding recommendation */}
            {Object.entries(recommendations).map(([key, recommendation]: [string, Recommendation], index) => {

              // Skip the lastUpdated key as this is not a stock recommendation
              if (key === "last_updated") return;

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

              if (sentiment === undefined) {
                console.log(sentiment);
                console.log(key);
              }

              return (
                <RecommendationBox key={index} symbol={key} currentPrice={recommendation.high_price} recommendation={recommendationString} sentiment={sentiment} />
              );
            })}
          </div>
        </div>
      </div>
      {/* Credits for resources used */}
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
