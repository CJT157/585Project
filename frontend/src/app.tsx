import background from '/homepage-bg.svg';
import './app.css';
import './RecommendationBox.css';
import RecommendationBox from './RecommendationBox';
import gcloud_logo from '/gcloud.svg';
import alpaca_logo from '/alpaca.svg';
import benzinga_logo from '/benzinga.svg';

function App() {

  return (
    <div className="App">
      <div className="header">
        <img src={background} width="100%" height="100%" id="background-img" />
        <div className="content">
          <h1 id="title">Stock Recommendations</h1>

          <div className="recommendations">
            <RecommendationBox symbol="AAPL" currentPrice={166.56} recommendation="BUY" accuracy={70} />
            <RecommendationBox symbol="TSLA" currentPrice={184.50} recommendation='SELL' accuracy={50} />
            <RecommendationBox symbol="AMZN" currentPrice={102.72} recommendation='SELL' accuracy={85} />
            <RecommendationBox symbol="GOOGL" currentPrice={105.61} recommendation='BUY' accuracy={100} />
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
