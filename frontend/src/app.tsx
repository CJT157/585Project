import { useState } from 'react'
import logo from '/logo.svg';

import './App.css'
import { MeshGradientRenderer } from '@johnn-e/react-mesh-gradient'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="App">
      <MeshGradientRenderer
        className="background-gradient"
        colors={[
          "#C3E4FF",
          "#6EC3F4",
          "#EAE2FF",
          "#B9BEFF",
          "#B3B8F9"
        ]}
        wireframe
        speed={0.025}
      >
        <div className="container">
          <div className="title-container">
            <img src={logo} width="100" height="100" />
          </div>
        </div>
      </MeshGradientRenderer>
    </div>
  )
}

export default App
