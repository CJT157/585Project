import { useState, useEffect } from 'react';
import background from '/homepage-bg.svg';
import './app.css';
import './RecommendationBox.css';
import RecommendationBox from './RecommendationBox';
import gcloud_logo from '/gcloud.svg';
import alpaca_logo from '/alpaca.svg';
import benzinga_logo from '/benzinga.svg';
import site_logo from '/logo.svg';

/**
 * Format of the data we get from the API
 * 
 * @param buy The % of analysts who recommend buying this stock
 * @param close_price The price of the stock when the market last closed
 * @param high_price The highest recorded price of the stock today
 * @param hold The % of analysts who recommend holding this stock
 * @param low_price The lowest recorded price of the stock today
 * @param open_price The price of the stock when the market last opened
 * @param sell The % of analysts who recommend selling this stock
 * @param time The time the data was last updated
 * @param volume The total number of shares traded today
 * 
*/
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

              // Calculate the highest percentage recommended and set a string for the recommendation accordingly.
              const percentSell = recommendation.sell;
              const percentBuy = recommendation.buy;
              const percentHold = recommendation.hold;

              // Default to recommend holding the stock
              let recommendationString: string = "HOLD";
              let sentiment: number = percentHold;

              // If the pecent recommended for selling is higher than buying and holding, recommend selling.
              if (percentSell > percentBuy && percentSell > percentHold) {
                recommendationString = "SELL";
                sentiment = percentSell;
              }
              // If the pecent recommended for buying is higher than selling and holding, recommend buying.
              else if (percentBuy > percentSell && percentBuy > percentHold) {
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
