import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './app'
// import './index.css'

/**
 * Entry point for the application. Renders our App component inside of the div with the id 'root'.
 */
ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
