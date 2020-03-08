import React from 'react';
import { render } from 'react-dom';
import { Provider, connect, mapStateToProps, mapDispatchToProps } from 'react-redux';
import { ConnectedRouter } from 'connected-react-router';

// // These imports load individual services into the firebase namespace.
// import 'firebase/auth';
// import 'firebase/database';

import { getStore, history } from './store';
import getRoutes from './routes/index';


// const ReduxApp = connect(mapStateToProps, mapDispatchToProps)(App);
const routes = getRoutes();

render(
  <Provider store={getStore()}>
    <ConnectedRouter history={history}>
      {routes}
    </ConnectedRouter>
  </Provider>,
  document.getElementById('root'),
);
