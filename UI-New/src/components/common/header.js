import React from 'react';
import ImageProvider from '../ImageProvider'
import './header.css';

const Header = (props) => (
  <div className="header">
      <ImageProvider src={props.logo} className={props.className} />
      <div className="header-label">{props.label}</div>
  </div>
);

export default Header;
