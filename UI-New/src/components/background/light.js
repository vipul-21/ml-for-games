import React from 'react';
import classnames from 'classnames';
import './light.css';

const LightTheme = (props) =>
  (<div className={props.grey ? props.className : "light-wrapper"}>
      {props.children}
    </div>);

export default LightTheme;
