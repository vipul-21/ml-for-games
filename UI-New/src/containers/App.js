import React from 'react';
import LightTheme from '../components/background/light'
import TokenStorage from '../services/TokenStorage';

import Login from './public/main'

class App extends React.Component {
  render() {
      return(
        <LightTheme>
            <Login />
        </LightTheme>
      )
  }
}

export default App;
