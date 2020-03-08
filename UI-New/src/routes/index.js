import React, { PropTypes } from 'react';
import { Route, Switch } from 'react-router';
import App from '../containers/App';
import Vote from '../containers/secure/vote';
import MalicousNode from '../containers/secure/MalicousNode';
import Tree from '../containers/secure/Tree';
import Dashboard from '../containers/secure/admin/dashboard';

const getRoutes = () =>
  (
      <Switch>
        <Route exact path="/" component={Dashboard} />
        <Route exact path="/malicious" component={MalicousNode} />
        <Route exact path="/tree" component={Tree} />

      </Switch>
  );

  export default getRoutes;
