import { createStore, applyMiddleware, combineReducers } from 'redux';
import logger from 'redux-logger';
import createSagaMiddleware from 'redux-saga';
import { routerMiddleware } from 'react-router-redux';
import { connectRouter } from 'connected-react-router';
import { createBrowserHistory } from 'history';

import main from '../reducers/main';
import saga from '../saga/saga';

const Config = process.env.NODE_ENV;
const sagaMiddleware = createSagaMiddleware();

export const history = createBrowserHistory();

export const getStore = () => {
  if (Config === 'development') {
    const store = createStore(
      combineReducers({
        main,
        router: connectRouter(history),
      }),
      applyMiddleware(logger, sagaMiddleware, routerMiddleware(history)),
    );
    sagaMiddleware.run(saga);

    return store;
  } else if (Config === 'production') {
    const store = createStore(
      combineReducers({
        main,
        router: connectRouter(history),
      }),
      applyMiddleware(logger, sagaMiddleware, routerMiddleware(history)),
    );
    sagaMiddleware.run(saga);

    return store;
  }
};


export default getStore;


// create the saga middleware
// mount it on the Store
